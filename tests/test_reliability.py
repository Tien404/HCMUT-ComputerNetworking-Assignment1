import time
import unittest
from src.protocol.reliability import Sender, Receiver


class PlaceholderEndpoint:
    def __init__(self):
        self.sent = []

    def udp_send(self, data, to):
        self.sent.append(data)


class ReliabilityTests(unittest.TestCase):
    def setUp(self):
        self.endpoint = PlaceholderEndpoint()
        self.sender = Sender(self.endpoint, ("127.0.0.1", 9000), 1)
        self.receiver = Receiver(self.endpoint)

    def test_send_and_cumulative_ack(self):
        self.sender.add_data(1, 1, 0, b"a")
        self.sender.send_packet()
        self.sender.add_data(2, 1, 0, b"b")
        self.sender.send_packet()
        self.assertEqual(len(self.endpoint.sent), 2)

        self.sender.handle_ack(2)
        self.assertEqual(self.sender.unacked_packets, {})
        self.assertEqual(self.sender.send_base, 2)
        self.assertIsNone(self.sender.deadline)

    def test_three_duplicate_acks(self):
        self.sender.add_data(1, 1, 0, b"a")
        self.sender.send_packet()
        self.sender.handle_ack(0)
        self.sender.handle_ack(0)
        self.assertEqual(len(self.endpoint.sent), 1)

        self.sender.handle_ack(0)
        self.assertEqual(len(self.endpoint.sent), 2)
        self.assertEqual(self.endpoint.sent[0], self.endpoint.sent[1])

    def test_timeout_retransmits(self):
        self.sender.add_data(1, 1, 0, b"a")
        self.sender.send_packet()
        self.sender.deadline = time.monotonic() - 1
        self.sender.check_timeout()
        self.assertEqual(self.endpoint.sent[0], self.endpoint.sent[1])
        self.assertEqual(self.sender.rto, 2)

        self.sender.handle_ack(1)
        self.assertIsNone(self.sender.srtt)

    def test_first_rtt_sample(self):
        self.sender.update_rtt(0.2)
        self.assertEqual(self.sender.srtt, 0.2)
        self.assertEqual(self.sender.rttvar, 0.1)

    def test_receive_out_of_order(self):
        self.sender.add_data(1, 1, 0, b"a")
        self.sender.send_packet()
        self.sender.add_data(2, 1, 0, b"b")
        self.sender.send_packet()

        self.receiver.receive_packet(self.endpoint.sent[1])
        self.assertIsNone(self.receiver.pop_packet())
        self.receiver.receive_packet(self.endpoint.sent[0])
        first = self.receiver.pop_packet()
        second = self.receiver.pop_packet()
        assert first is not None
        assert second is not None
        self.assertEqual(first[4], b"a")
        self.assertEqual(second[4], b"b")

    def test_receive_duplicate(self):
        self.sender.add_data(1, 1, 0, b"a")
        self.sender.send_packet()
        self.receiver.receive_packet(self.endpoint.sent[0])
        self.receiver.receive_packet(self.endpoint.sent[0])
        packet = self.receiver.pop_packet()
        assert packet is not None
        self.assertEqual(packet[4], b"a")
        self.assertIsNone(self.receiver.pop_packet())
