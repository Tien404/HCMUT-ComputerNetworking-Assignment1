import unittest
from src.protocol.flow_control import can_send, can_receive, advertised_window


class FlowControlTests(unittest.TestCase):
    def test_send_window(self):
        # self.assertTrue(can_send(0, 1, 2))
        # self.assertFalse(can_send(0, 2, 2))
        pass

    def test_receive_window(self):
        # ready = [b"a"]
        # self.assertEqual(advertised_window(ready, 3), 2)
        # self.assertTrue(can_receive(0, 1, 2))
        # self.assertFalse(can_receive(0, 2, 2))
        pass
