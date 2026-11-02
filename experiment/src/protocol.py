"""A small versioned packet format for the experiment."""

import json
import struct
from enum import IntEnum


MAGIC = b"CN"
VERSION = 1
HEADER = struct.Struct("!2sBBH")
MAX_PACKET_SIZE = 1200
MAX_PAYLOAD_SIZE = min(0xFFFF, MAX_PACKET_SIZE - HEADER.size)


class MessageType(IntEnum):
    HELLO = 1
    HELLO_ACK = 2
    AUTH = 3
    AUTH_RESULT = 4
    USER_LIST = 5
    CHAT = 6
    FILE_START = 7
    FILE_CHUNK = 8
    FILE_END = 9
    ACK = 10
    HEARTBEAT = 11
    LOGOUT = 12
    ERROR = 13


class ProtocolError(ValueError):
    """Raised when a packet is malformed or too large."""


def encode_message(message_type, payload):
    """Encode a message type and JSON object into one packet."""
    try:
        message_type = MessageType(message_type)
    except ValueError as exc:
        raise ProtocolError("Unknown message type") from exc

    if not isinstance(payload, dict):
        raise ProtocolError("Payload must be a JSON object")

    try:
        body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError) as exc:
        raise ProtocolError("Payload is not valid JSON data") from exc

    if len(body) > MAX_PAYLOAD_SIZE:
        raise ProtocolError("Packet is too large")

    return HEADER.pack(MAGIC, VERSION, message_type, len(body)) + body


def decode_message(packet):
    """Decode a packet and return ``(message_type, payload)``."""
    if not isinstance(packet, bytes) or len(packet) < HEADER.size:
        raise ProtocolError("Packet is shorter than its header")
    if len(packet) > MAX_PACKET_SIZE:
        raise ProtocolError("Packet is too large")

    magic, version, raw_type, body_length = HEADER.unpack(packet[:HEADER.size])
    if magic != MAGIC:
        raise ProtocolError("Invalid packet magic")
    if version != VERSION:
        raise ProtocolError("Unsupported protocol version")
    if body_length != len(packet) - HEADER.size:
        raise ProtocolError("Payload length does not match packet")

    try:
        message_type = MessageType(raw_type)
    except ValueError as exc:
        raise ProtocolError("Unknown message type") from exc

    try:
        payload = json.loads(packet[HEADER.size:].decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProtocolError("Payload is not valid UTF-8 JSON") from exc

    if not isinstance(payload, dict):
        raise ProtocolError("Payload must be a JSON object")
    return message_type, payload
