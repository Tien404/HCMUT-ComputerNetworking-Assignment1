from src.common.constants import MAGIC, VERSION, PACKET_HEADER_SIZE, PacketType, DataType


def parse_packet(raw: bytes):
    # header: 30 byte
    header = raw[:PACKET_HEADER_SIZE]
    body = raw[PACKET_HEADER_SIZE:]
    return header, body


def make_packet_header(packet_type: int, length: int, session_id: int, sequence: int):
    # 2B magic + 1B version + 1B type + 2B length + 16B session + 8B sequence
    header = b''
    header += MAGIC
    header += VERSION.to_bytes(1, "big")
    header += packet_type.to_bytes(1, "big")
    header += length.to_bytes(2, "big")
    header += session_id.to_bytes(16, "big")
    header += sequence.to_bytes(8, "big")
    return header


def make_packet(packet_type: int, session_id: int, sequence: int, body: bytes):
    length = PACKET_HEADER_SIZE + len(body)
    return make_packet_header(packet_type, length, session_id, sequence) + body


def decode_packet_header(header: bytes):
    packet_type = int.from_bytes(header[3:4], "big")
    length = int.from_bytes(header[4:6], "big")
    session_id = int.from_bytes(header[6:22], "big")
    sequence = int.from_bytes(header[22:30], "big")
    return packet_type, length, session_id, sequence


def make_data_body(message_id: int, message_length: int, offset: int,
                   data: bytes, typ=DataType.CHAT):
    # 8B message_id + 8B length + 8B offset + 1B type + data
    body = b''
    body += message_id.to_bytes(8, "big")
    body += message_length.to_bytes(8, "big")
    body += offset.to_bytes(8, "big") # begins from message/file start
    body += typ.to_bytes(1, "big")
    body += data
    return body


def decode_data_body(body: bytes):
    message_id = int.from_bytes(body[0:8], "big")
    message_length = int.from_bytes(body[8:16], "big")
    offset = int.from_bytes(body[16:24], "big")
    typ = DataType(int.from_bytes(body[24:25], "big"))
    data = body[25:]
    return message_id, message_length, offset, typ, data


def make_ack_packet(session_id: int, next_expected: int, receive_window: int):
    body = b''
    body += next_expected.to_bytes(8, "big")
    body += receive_window.to_bytes(2, "big")

    return make_packet(PacketType.ACK, session_id, 0, body)


def decode_ack_body(body: bytes):
    next_expected = int.from_bytes(body[0:8], "big")
    receive_window = int.from_bytes(body[8:10], "big")
    return next_expected, receive_window


def make_ping_packet(session_id: int, ping_id: int):
    body = ping_id.to_bytes(8, "big")
    return make_packet(PacketType.PING, session_id, 0, body)


def make_pong_packet(session_id: int, ping_id: int):
    body = ping_id.to_bytes(8, "big")
    return make_packet(PacketType.PONG, session_id, 0, body)
