import unittest
from src.common.constants import MAX_U64, StreamType
from src.common.errors import PacketError
from src.protocol.packet import HEADER, FRAME_HEADER, DATA_BODY, make_data, uint


class BasicProtocolTests(unittest.TestCase):
    def test_layout_sizes_match_design(self):
        self.assertEqual(HEADER.size, 32)
        self.assertEqual(FRAME_HEADER.size + DATA_BODY.size, 48)

    def test_unsigned_integer_bounds(self):
        self.assertEqual(uint(0, MAX_U64), 0)
        self.assertEqual(uint(MAX_U64, MAX_U64), MAX_U64)
        for value in (-1, MAX_U64 + 1, True):
            with self.subTest(value=value), self.assertRaises(PacketError):
                uint(value, MAX_U64)


class ProtocolTests(unittest.TestCase):
    def test_mixed_frames_and_ack_gap(self):
        # TODO: Round-trip DATA + ACK ranges + MAX_DATA + PONG in one packet.
        # ACK [97,100] and [90,92] must not acknowledge PN 95.
        pass

    def test_ack_wire_matches_original_v3(self):
        # TODO: Compare ACK blocks against the original v3 wire bytes.
        pass

    def test_file_metadata_and_raw_bytes(self):
        # TODO: Round-trip binary file bytes and UTF-8 filename metadata.
        pass

    def test_all_flow_control_frames(self):
        # TODO: Round-trip MAX_DATA, MAX_STREAM_DATA and both BLOCKED frames.
        pass

    def test_varint_boundaries(self):
        # TODO: Check the 1/2/4/8-byte transitions and truncated input.
        pass

    def test_invalid_and_oversize_packet(self):
        # TODO: Reject invalid magic/version/count/length/type/flags and oversized packets.
        pass
