import unittest
from src.common.constants import ConnectionState
from src.protocol.reliability import new_connection, heartbeat_due, idle_expired


class BasicStateTests(unittest.TestCase):
    def test_connections_do_not_share_mutable_state(self):
        first, second = new_connection(), new_connection()
        first["sent_packets"][1] = {}
        first["tx_flow"]["streams"][1] = {}
        self.assertEqual(second["sent_packets"], {})
        self.assertEqual(second["tx_flow"]["streams"], {})

    def test_sending_ping_does_not_refresh_receive_idle(self):
        connection = new_connection()
        connection["state"] = ConnectionState.ESTABLISHED
        self.assertTrue(heartbeat_due(connection, 5))
        connection["last_ping_submitted"] = 5
        self.assertFalse(heartbeat_due(connection, 6))
        self.assertTrue(idle_expired(connection, 30))



class ReliabilityTests(unittest.TestCase):
    def test_coverage_and_selective_missing_ranges(self):
        # TODO: Merge out-of-order/duplicate ranges and return only missing subranges.
        pass

    def test_empty_message_requires_metadata_ack(self):
        # TODO: Empty content is complete only after its metadata packet is acknowledged.
        pass

    def test_rtt_ack_delay_loss_threshold_and_rto(self):
        # TODO: Check eligible RTT samples, ACK-delay adjustment, loss delay and RTO backoff.
        pass

    def test_heartbeat_does_not_confirm_data(self):
        # TODO: PING gets PONG; PONG gets no PONG; neither acknowledges DATA.
        pass

    def test_ack_blocks_retry_and_late_ack(self):
        # TODO: Retry only uncovered data with fresh PNs; late ACKs cancel redundant retries.
        # In-flight bytes and completion must each be retired/reported exactly once.
        pass

    def test_loss_threshold_before_rto(self):
        # TODO: Require later-ACK evidence; prefer packet/time-threshold loss over RTO.
        pass

    def test_send_only_stream_cannot_receive(self):
        # TODO: An awaitable receive must reject a send-only stream.
        # A blocked file stream must not block a separate chat stream.
        pass
