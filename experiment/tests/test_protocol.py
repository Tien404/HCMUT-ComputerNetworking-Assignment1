import unittest

from src.protocol import (
    MAX_PACKET_SIZE,
    MessageType,
    ProtocolError,
    decode_message,
    encode_message,
)


class ProtocolTests(unittest.TestCase):
    def test_round_trip(self):
        packet = encode_message(MessageType.CHAT, {"text": "xin chào", "to": "Lan"})
        self.assertEqual(
            decode_message(packet),
            (MessageType.CHAT, {"text": "xin chào", "to": "Lan"}),
        )

    def test_rejects_bad_header_and_length(self):
        packet = encode_message(MessageType.HEARTBEAT, {})
        for malformed in (b"", b"XX" + packet[2:], packet[:-1]):
            with self.subTest(packet=malformed), self.assertRaises(ProtocolError):
                decode_message(malformed)

    def test_rejects_oversized_packet(self):
        with self.assertRaises(ProtocolError):
            encode_message(MessageType.CHAT, {"text": "x" * MAX_PACKET_SIZE})

    def test_payload_must_be_object(self):
        with self.assertRaises(ProtocolError):
            encode_message(MessageType.CHAT, ["not", "an", "object"])


if __name__ == "__main__":
    unittest.main()
