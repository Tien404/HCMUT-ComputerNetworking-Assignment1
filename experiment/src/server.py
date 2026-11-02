"""Async TCP handshake and UDP login/chat relay."""

import argparse
import asyncio
import time

from src.protocol import MessageType, ProtocolError, decode_message, encode_message


SESSION_TIMEOUT = 30


class ChatServer:
    def __init__(self):
        self.transport = None
        self.users = {}

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, address):
        try:
            message_type, payload = decode_message(data)
            self.handle_message(message_type, payload, address)
        except ProtocolError:
            self.send(MessageType.ERROR, {"error": "invalid packet"}, address)

    def error_received(self, exc):
        print(f"UDP socket error: {exc}")

    def connection_lost(self, exc):
        if exc is not None:
            print(f"UDP socket closed with error: {exc}")

    def send(self, message_type, payload, address):
        if self.transport is not None:
            try:
                self.transport.sendto(encode_message(message_type, payload), address)
            except (OSError, ProtocolError) as exc:
                print(f"Could not send UDP response to {address}: {exc}")

    def handle_message(self, message_type, payload, address):
        if message_type == MessageType.AUTH:
            self.login(payload, address)
            return

        user = self.users.get(address)
        if user is None:
            self.send(MessageType.ERROR, {"error": "login required"}, address)
            return

        self.users[address]["last_seen"] = time.monotonic()
        username = user["username"]
        if message_type == MessageType.HEARTBEAT:
            self.send(MessageType.ACK, {"for": "heartbeat"}, address)
        elif message_type == MessageType.CHAT:
            self.relay_chat(username, payload, address)
        elif message_type == MessageType.LOGOUT:
            self.logout(address)
        else:
            self.send(MessageType.ERROR, {"error": "unsupported message"}, address)

    def login(self, payload, address):
        username = payload.get("username")
        if (not isinstance(username, str) or not username.strip()
                or len(username) > 24 or not username.isprintable()):
            self.send(MessageType.AUTH_RESULT, {"ok": False, "error": "invalid username"}, address)
            return

        username = username.strip()
        current = self.users.get(address)
        if current and current["username"] != username:
            self.send(MessageType.AUTH_RESULT, {"ok": False, "error": "address already logged in"}, address)
            return
        if any(user["username"] == username and peer != address
               for peer, user in self.users.items()):
            self.send(MessageType.AUTH_RESULT, {"ok": False, "error": "username is already online"}, address)
            return

        self.users[address] = {"username": username, "last_seen": time.monotonic()}
        self.send(MessageType.AUTH_RESULT, {"ok": True, "username": username}, address)
        self.broadcast_user_list()

    def relay_chat(self, sender, payload, sender_address):
        text = payload.get("text")
        recipient = payload.get("to")
        if not isinstance(text, str) or not text.strip() or len(text.encode("utf-8")) > 1000:
            self.send(MessageType.ERROR, {"error": "message must be 1-1000 UTF-8 bytes"}, sender_address)
            return
        if recipient is not None and not isinstance(recipient, str):
            self.send(MessageType.ERROR, {"error": "recipient must be a username"}, sender_address)
            return

        message = {"from": sender, "text": text}
        if recipient is None:
            for address in self.users:
                self.send(MessageType.CHAT, message, address)
        else:
            destination = next((address for address, user in self.users.items()
                                if user["username"] == recipient), None)
            if destination is None:
                self.send(MessageType.ERROR, {"error": "recipient is not online"}, sender_address)
            else:
                self.send(MessageType.CHAT, message, destination)
        self.send(MessageType.ACK, {"for": "chat"}, sender_address)

    def logout(self, address):
        if self.users.pop(address, None) is not None:
            self.broadcast_user_list()

    def broadcast_user_list(self):
        names = sorted(user["username"] for user in self.users.values())
        for address in self.users:
            self.send(MessageType.USER_LIST, {"users": names}, address)

    async def remove_expired_users(self):
        while True:
            await asyncio.sleep(5)
            now = time.monotonic()
            expired = [address for address, user in self.users.items()
                       if now - user["last_seen"] >= SESSION_TIMEOUT]
            for address in expired:
                self.logout(address)


async def handle_tcp_client(reader, writer):
    """Accept one simple TCP HELLO and return an ACK before closing."""
    try:
        request = await asyncio.wait_for(reader.readline(), timeout=5)
        if request == b"HELLO\n":
            writer.write(b"ACK\n")
        else:
            writer.write(b"ERROR\n")
        await writer.drain()
    except (asyncio.TimeoutError, ConnectionError) as exc:
        print(f"TCP handshake ended: {exc}")
    finally:
        writer.close()
        await writer.wait_closed()


async def run(host, port):
    loop = asyncio.get_running_loop()
    server = ChatServer()
    transport, _ = await loop.create_datagram_endpoint(
        lambda: server, local_addr=(host, port)
    )
    tcp_server = await asyncio.start_server(handle_tcp_client, host, port)
    timeout_task = asyncio.create_task(server.remove_expired_users())
    print(f"Server listening on {host}:{port} (TCP and UDP)")

    try:
        async with tcp_server:
            await tcp_server.serve_forever()
    finally:
        timeout_task.cancel()
        await asyncio.gather(timeout_task, return_exceptions=True)
        transport.close()


def main():
    parser = argparse.ArgumentParser(description="Run the collaboration experiment server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9000)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    try:
        asyncio.run(run(args.host, args.port))
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    main()
