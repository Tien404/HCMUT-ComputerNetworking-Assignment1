from enum import IntEnum


class PacketType(IntEnum):
    DATA = 1
    ACK = 2
    PING = 3
    PONG = 4


class DataType(IntEnum):
    CHAT = 0
    FILE = 1


# application messages
class MessageType(IntEnum):
    AUTH = 1
    AUTH_RESULT = 2
    USER_LIST = 3
    PRESENCE = 4
    LOGOUT = 5


class ConnectionState(IntEnum):
    NEW = 0
    HANDSHAKING = 1
    ESTABLISHED = 2
    CLOSING = 3
    CLOSED = 4


class CongestionPhase(IntEnum):
    SLOW_START = 0
    AVOIDANCE = 1
    RECOVERY = 2


SERVER_PORT = 9000
CLIENT_PORT = 9100
HTTP_PORT = 8080

MAGIC = b"AB"
VERSION = 0

MAX_PACKET_SIZE = 1200
PACKET_HEADER_SIZE = 30
DATA_BODY_SIZE = 25
CHUNK_SIZE = 1000

INITIAL_RTO = 1.0
RECEIVE_WINDOW = 32  # Packet slots
INITIAL_SSTHRESH = 64 * 1024
CUBIC_BETA = 0.7
CUBIC_C = 0.4
HEARTBEAT_INTERVAL = 5.0
SESSION_TIMEOUT = 30.0
