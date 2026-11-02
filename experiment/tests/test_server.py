import unittest

from src.protocol import MessageType, decode_message
from src.server import ChatServer


class FakeTransport:
    def __init__(self):
        self.sent = []

    def sendto(self, packet, address):
        self.sent.append((decode_message(packet), address))


class ChatServerTests(unittest.TestCase):
    def setUp(self):
        self.server = ChatServer()
        self.transport = FakeTransport()
        self.server.connection_made(self.transport)
        self.alice = ("127.0.0.1", 10001)
        self.bob = ("127.0.0.1", 10002)
        self.server.login({"username": "alice"}, self.alice)
        self.server.login({"username": "bob"}, self.bob)
        self.transport.sent.clear()

    def test_private_chat_is_relayed_with_sender_name(self):
        self.server.handle_message(
            MessageType.CHAT,
            {"to": "bob", "text": "hello"},
            self.alice,
        )

        bob_messages = [message for message, address in self.transport.sent
                        if address == self.bob]
        self.assertIn(
            (MessageType.CHAT, {"from": "alice", "text": "hello"}),
            bob_messages,
        )
        self.assertIn(
            (MessageType.ACK, {"for": "chat"}),
            [message for message, address in self.transport.sent if address == self.alice],
        )

    def test_duplicate_username_is_rejected(self):
        self.server.login({"username": "alice"}, ("127.0.0.1", 10003))
        message, address = self.transport.sent[-1]
        self.assertEqual(message, (
            MessageType.AUTH_RESULT,
            {"ok": False, "error": "username is already online"},
        ))
        self.assertEqual(address, ("127.0.0.1", 10003))


if __name__ == "__main__":
    unittest.main()
