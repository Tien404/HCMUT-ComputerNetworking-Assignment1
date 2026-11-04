import unittest
from src.client.main import ClientProtocol, new_client_state
from src.server import ServerProtocol


class NetworkTests(unittest.TestCase):
    def test_client_receives_datagram(self):
        # state = new_client_state()
        # client = ClientProtocol(state["network_events"])
        # client.datagram_received(b"hello", ("127.0.0.1", 9000))
        # self.assertEqual(state["network_events"].get_nowait(),
        #                  ("datagram", b"hello", ("127.0.0.1", 9000)))
        pass

    def test_server_receives_datagram(self):
        # server = ServerProtocol()
        # server.datagram_received(b"hello", ("127.0.0.1", 9100))
        # self.assertEqual(server.events.get_nowait(),
        #                  ("datagram", b"hello", ("127.0.0.1", 9100)))
        pass
