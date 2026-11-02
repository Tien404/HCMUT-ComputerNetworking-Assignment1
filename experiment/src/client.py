"""A small CLI client for the UDP chat relay."""

import argparse
import asyncio
import contextlib

from src.protocol import MessageType, ProtocolError, decode_message, encode_message


class ClientProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        self.transport = None
        self.messages = asyncio.Queue()

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, address):
        try:
            self.messages.put_nowait(decode_message(data))
        except ProtocolError as exc:
            print(f"Ignored malformed server packet: {exc}")

    def error_received(self, exc):
        print(f"UDP socket error: {exc}")


async def tcp_handshake(host, port):
    reader, writer = await asyncio.open_connection(host, port)
    try:
        writer.write(b"HELLO\n")
        await writer.drain()
        response = await asyncio.wait_for(reader.readline(), timeout=5)
        if response != b"ACK\n":
            raise ConnectionError("Server did not acknowledge the handshake")
    finally:
        writer.close()
        await writer.wait_closed()


async def receive_messages(protocol):
    while True:
        message_type, payload = await protocol.messages.get()
        if message_type == MessageType.CHAT:
            print(f"\n{payload.get('from', '?')}: {payload.get('text', '')}")
        elif message_type == MessageType.USER_LIST:
            print(f"\nOnline: {', '.join(payload.get('users', []))}")
        elif message_type == MessageType.ERROR:
            print(f"\nServer error: {payload.get('error', 'unknown error')}")


async def run(server, port, username):
    await tcp_handshake(server, port)
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        ClientProtocol, local_addr=("0.0.0.0", 0)
    )
    receiver = None
    try:
        transport.sendto(encode_message(MessageType.AUTH, {"username": username}),
                         (server, port))
        message_type, result = await asyncio.wait_for(protocol.messages.get(), timeout=5)
        if message_type != MessageType.AUTH_RESULT or not result.get("ok"):
            raise ConnectionError(result.get("error", "Login failed"))
        print(f"Logged in as {username}. Type a message; /quit exits.")
        receiver = asyncio.create_task(receive_messages(protocol))

        while True:
            text = await asyncio.to_thread(input, "> ")
            if text == "/quit":
                break
            if text.startswith("/msg "):
                try:
                    _, recipient, body = text.split(" ", 2)
                except ValueError:
                    print("Usage: /msg USER message")
                    continue
                payload = {"to": recipient, "text": body}
            else:
                payload = {"text": text}
            transport.sendto(encode_message(MessageType.CHAT, payload), (server, port))
    finally:
        transport.sendto(encode_message(MessageType.LOGOUT, {}), (server, port))
        if receiver is not None:
            receiver.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await receiver
        transport.close()


def main():
    parser = argparse.ArgumentParser(description="Connect to the collaboration experiment")
    parser.add_argument("--server", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9000)
    parser.add_argument("--username", required=True)
    args = parser.parse_args()
    try:
        asyncio.run(run(args.server, args.port, args.username))
    except (ConnectionError, OSError, asyncio.TimeoutError) as exc:
        parser.exit(1, f"Connection failed: {exc}\n")
    except KeyboardInterrupt:
        print("\nClient stopped.")


if __name__ == "__main__":
    main()
