import unittest
from src.common.constants import PacketType, DataType
from src.protocol.packet import (
    make_packet, parse_packet, decode_packet_header, make_data_body,
    make_ack_packet, decode_ack_body, decode_data_body, make_ping_packet, make_pong_packet,
)


class ProtocolTests(unittest.TestCase):
    def test_data_packet(self):
        body = make_data_body(1, 5, 0, b"hello", DataType.CHAT)
        packet = make_packet(PacketType.DATA, 1, 0, body)
        header, body = parse_packet(packet)
        self.assertEqual(decode_packet_header(header), (PacketType.DATA, len(packet), 1, 0))
        self.assertEqual(decode_data_body(body), (1, 5, 0, DataType.CHAT, b"hello"))

    def test_ack_packet(self):
        packet = make_ack_packet(1, 3, 0)
        header, body = parse_packet(packet)
        self.assertEqual(decode_packet_header(header)[0], PacketType.ACK)
        self.assertEqual(decode_ack_body(body), (3, 0))

    def test_ping_pong(self):
        ping = make_ping_packet(1, 10)
        header, body = parse_packet(ping)
        self.assertEqual(decode_packet_header(header)[0], PacketType.PING)
        pong = make_pong_packet(1, int.from_bytes(body, "big"))
        header, body = parse_packet(pong)
        self.assertEqual(decode_packet_header(header)[0], PacketType.PONG)
        self.assertEqual(int.from_bytes(body, "big"), 10)
