import argparse
import asyncio


from src.common.constants import SERVER_PORT, SESSION_TIMEOUT, MAX_PACKET_SIZE


class ServerProtocol(asyncio.DatagramProtocol):
    # def __init__(self):
    #     self.events = asyncio.Queue()
    #     self.transport = None
    #     self.dropped_events = 0

    # def connection_made(self, transport):
    #     self.transport = transport

    # def enqueue(self, kind, value, address=None):
    #     self.events.put_nowait((kind, value, address))

    # def datagram_received(self, data, address):
    #     if len(data) > MAX_PACKET_SIZE:
    #         self.dropped_events += 1
    #         return
    #     self.enqueue("datagram", data, address)

    # def error_received(self, exc):
    #     self.enqueue("socket_error", exc)

    # def connection_lost(self, exc):
    #     self.enqueue("socket_closed", exc)
    pass


def verify(username, password):
    # TODO: Choose account storage and verify password hashes using a standard library.
    pass


def unicast(sender, recipient, message, users):
    # TODO: Look up the online recipient and enqueue data on its output queue.
    # TODO: Receive in connection order, then queue payload on the recipient's session.
    # TODO: A server ACK does not prove delivery to the final recipient.
    pass


def broadcast(sender, message, users):
    # TODO: Call unicast for each online user except the sender.
    # TODO: Use independent queues/ACK tracking so a slow user does not block everyone.
    pass


def add_user(users, username, address, session_id, now):
    # if username in users:
    #     raise ValueError("User is already online")
    # users[username] = {"address": address, "session_id": session_id, "last_received_at": now}
    pass


def expired_users(users, now):
    # return [name for name, user in users.items()
    #         if now - user["last_received_at"] >= SESSION_TIMEOUT]
    pass


async def process_events(server, users):
    # TODO: Use one owner task: verify -> decode -> session/auth/presence/routing.
    # TODO: Process queued events; do not spawn a task for every datagram.
    pass


async def expire_users(users):
    # TODO: Refresh last_received_at only after accepting valid traffic.
    # TODO: Remove expired users, close their sessions and notify online clients.
    pass


async def run(host, port):
    # TODO: Implement the rubric TCP handshake and concurrent UDP login/user-list/presence/forwarding.
    # TODO: Bind a UDP session to the TCP login; one Sender/Receiver pair per client.
    # Each hop has its own sequence/window/CUBIC, not one connection per file.
    # TODO: Handle 10-20 clients, socket exceptions, timeouts and graceful asyncio cleanup.
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog='Server',
                        description='Start the server')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=SERVER_PORT)
    args = parser.parse_args()
    host = args.host
    port = args.port

    asyncio.run(run(host, port))
