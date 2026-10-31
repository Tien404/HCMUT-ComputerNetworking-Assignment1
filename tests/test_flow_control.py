import unittest
from src.protocol.flow_control import new_sender_flow, add_sender_stream, on_max_data, on_max_stream_data


class BasicFlowControlTests(unittest.TestCase):
    def test_limits_only_increase(self):
        flow = new_sender_flow(1000)
        add_sender_stream(flow, 1, 500)
        on_max_data(flow, 900)
        on_max_stream_data(flow, 1, 400)
        self.assertEqual(flow["max_data"], 1000)
        self.assertEqual(flow["streams"][1]["max_stream_data"], 500)
        on_max_data(flow, 2000)
        self.assertEqual(flow["max_data"], 2000)

    def test_stream_id_cannot_be_reused(self):
        flow = new_sender_flow(1000)
        add_sender_stream(flow, 1, 500)
        del flow["streams"][1]
        with self.assertRaises(ValueError):
            add_sender_stream(flow, 1, 500)


class FlowControlTests(unittest.TestCase):
    def test_both_limits_and_atomic_packet(self):
        # TODO: A rejected packet must not partially update any stream/connection credit.
        pass

    def test_retransmission_consumes_no_new_credit(self):
        # TODO: Retry an old byte range; total_committed_data must stay unchanged.
        # ACK must not return credit; retired stream credit must remain accounted for.
        pass

    def test_receiver_gap_duplicate_and_consumption(self):
        # TODO: Check high-watermark accounting, duplicates and incremental consumption.
        # MAX_STREAM_DATA/MAX_DATA must increase only when data is actually consumed.
        pass

    def test_blocked_frames_keep_both_scopes(self):
        # TODO: Check connection/stream BLOCKED limits and lost MAX updates.
        pass
