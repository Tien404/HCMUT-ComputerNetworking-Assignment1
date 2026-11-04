import unittest
from src.protocol.congestion_control import new_congestion, can_send


class CongestionControlTests(unittest.TestCase):
    def test_send_limit(self):
        # state = new_congestion()
        # self.assertTrue(can_send(state, 100, 0))
        # state["bytes_in_flight"] = state["cwnd"]
        # self.assertFalse(can_send(state, 100, 0))
        pass
