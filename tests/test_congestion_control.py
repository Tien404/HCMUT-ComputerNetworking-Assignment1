import unittest
from src.protocol.congestion_control import new_congestion, can_send


class BasicCongestionGateTests(unittest.TestCase):
    def test_cwnd_pacing_and_ack_only(self):
        state = new_congestion()
        state["bytes_in_flight"] = state["cwnd"]
        self.assertFalse(can_send(state, 100, 0))
        self.assertTrue(can_send(state, 100, 0, ack_only=True))
        self.assertFalse(can_send(state, 1201, 0, ack_only=True))
        state["bytes_in_flight"] = 0
        state["next_send_time"] = 1
        self.assertFalse(can_send(state, 100, 0))
        self.assertTrue(can_send(state, 100, 1))


class CongestionControlTests(unittest.TestCase):
    def test_slow_start_and_three_avoidance_regions(self):
        # TODO: Check eligible byte growth, Reno-friendly/concave/convex targets and recovery exit.
        pass

    def test_loss_once_per_recovery_and_timeout_slow_start(self):
        # TODO: Check one beta reduction per recovery, then RTO cwnd=2M and slow start.
        pass
