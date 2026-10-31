import struct
from src.common.constants import (
    MAGIC, VERSION, MAX_PACKET_SIZE, SESSION_ID_BYTES, MAX_PACKET_NUMBER,
    MAX_U64, MAX_FRAMES, MAX_ACK_RANGES, FrameType, StreamType,
)
from src.common.errors import PacketError

HEADER = struct.Struct("!2sBBHH16sQ")
FRAME_HEADER = struct.Struct("!BBH")
DATA_BODY = struct.Struct("!QQQQQHH")
STREAM_LIMIT = struct.Struct("!QQ")
CONNECTION_LIMIT = struct.Struct("!Q")


def uint(value, maximum):
    if type(value) is not int or not 0 <= value <= maximum:
        raise PacketError("Unsigned integer is out of range")
    return value


def encode_varint(value):
    # TODO: Encode unsigned 62-bit values using 1, 2, 4 or 8 bytes.
    pass


def decode_varint(data, pos=0):
    # TODO: Read the size prefix, reject truncation, return (value, next_position).
    pass


def make_data(stream_id, message_id, message_start_offset, message_length,
              offset, data, kind=StreamType.CHAT, metadata=b""):
    return {"type": FrameType.DATA, "kind": StreamType(kind),
            "stream_id": stream_id, "message_id": message_id,
            "message_start_offset": message_start_offset, "message_length": message_length,
            "offset": offset, "data": data, "metadata": metadata}


def make_ack(ranges, ack_delay=0):
    return {"type": FrameType.ACK, "ranges": tuple(ranges), "ack_delay": ack_delay}


def make_limit(kind, limit, stream_id=None):
    frame = {"type": FrameType(kind), "limit": limit}
    if stream_id is not None:
        frame["stream_id"] = stream_id
    return frame


def encode_frame(frame):
    # TODO: Encode DATA, ACK, PING/PONG and all four MAX/BLOCKED frames.
    # TODO: DATA flags use StreamType; validate message bounds and file metadata.
    # TODO: ACK body: largest, delay, count, first range, then gap/range pairs.
    pass


def decode_frame(kind, flags, body):
    # TODO: Decode and validate every field, flag, length and ACK gap.
    # TODO: Reject unsupported types, truncated bodies and trailing bytes.
    pass


def encode_packet(packet):
    # TODO: Validate the 16-byte session ID and the connection-wide packet number.
    # TODO: Pack multiple frames, total length and frame count into the v3 layout.
    # TODO: Enforce the datagram size limit, including future security overhead.
    pass


def decode_packet(data):
    # TODO: Validate magic/version/flags, total length, frame count and packet number.
    # TODO: Decode every frame; reject truncated frames and trailing bytes.
    pass


def verify_checksum(frame):
    # TODO: The proposal figure includes a DATA checksum; the original v3 codec does not.
    # TODO: Specify its algorithm, width and coverage before changing the wire layout.
    # TODO: Keep this requirement open rather than silently removing it.
    pass
