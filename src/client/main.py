import argparse
import asyncio


from src.common.constants import SERVER_PORT, CLIENT_PORT, HTTP_PORT, MAX_PACKET_SIZE


class ClientProtocol(asyncio.DatagramProtocol):
    # def __init__(self, events):
    #     self.events = events
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


def new_client_state():
    # return {"connection": None, "network_events": asyncio.Queue(),
    #         "ui_events": asyncio.Queue(), "closing": False}
    pass


def announce(sock, broadcast_address, presence):
    # TODO: Broadcast LAN presence; a discovered address is not an authenticated identity.
    pass


async def connect_server(state, address):
    # TODO: Connect to server via TCP for the rubric handshake/login, then bind a UDP session.
    # TODO: Set up one Sender/Receiver pair with a shared DATA sequence/window per direction.
    pass


async def send_private(state, recipient, text):
    # TODO: Allocate a message_id from the chat/file counter and queue the message.
    # Include recipient in the application message for server forwarding.
    pass


async def send_broadcast(state, text):
    # TODO: Send a global-chat command to the server; it queues a copy per recipient.
    # A server ACK only confirms the first hop, not final recipient delivery.
    pass


async def process_events(state):
    # TODO: Dispatch ACK to Sender, DATA to Receiver, PING/PONG to heartbeat handling.
    # TODO: ACK DATA including duplicates; consume ready packets in connection order.
    # TODO: Alternate queued chat/file chunks and call send_packet()/check_timeout().
    pass


async def run(server_host, server_port, udp_port, http_port):
    # TODO: TCP handshake, UDP session/discovery, heartbeat and raw HTTP UI.
    # TODO: Adapt the UDP endpoint to udp_send; do not block asyncio on recvfrom.
    # TODO: Forward messages/files through the server; close tasks/sockets on exit.
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog='Client',
                        description='Connect to server',)
    parser.add_argument('--server-ip', default='127.0.0.1')
    parser.add_argument('--server-port', type=int, default=SERVER_PORT)
    parser.add_argument('--udp-port', type=int, default=CLIENT_PORT)
    parser.add_argument('--http-port', type=int, default=HTTP_PORT)
    args = parser.parse_args()
    host = args.server_ip
    port = args.server_port
    udp_port = args.udp_port
    http_port = args.http_port

    asyncio.run(run(host, port, udp_port, http_port))
