from src.common.constants import (
    MAGIC, VERSION, MAX_PACKET_SIZE, SESSION_ID_BYTES, MAX_PACKET_NUMBER,
    MAX_U64, MAX_FRAMES, MAX_ACK_RANGES, FrameType, StreamType,
)
from src.common.errors import PacketError

def parse_packet(raw: bytes):
    frame_list = []
    packet_header = raw[:32]
    raw = raw[32:]
        # reserved: 3 byte (magic number, version, etc currently not use)
        # flags 1 byte
        # length 2 byte
    frame_count = int.from_bytes(packet_header[6:8], "big")
        # ssid 16 byte
        # pn 8 byte
    i = 0;
    while i < count:
        frame_header = raw[0:4]
            # frame_type: 1B
            # flags: 1B
        frame_length= int.from_bytes(frame_header[2:4], "big")
        frame_data = raw[4: 4+frame_length]
        raw = raw[4+frame_length:]

        frame_list = frame_list + [frame_header + frame_data]
        i = i + 1
        
    return packet_header, frame_list

def make_packet_header(flag: int, length:int, frame_count:int, session_id: int, packet_number: int) -> bytes:
    packet = b''
    packet += 0.to_bytes(3, "big") # reserve
    packet += flag.to_bytes(1, "big")   
    packet += length.to_bytes(2, "big")
    packet += frame_count.to_bytes(2, "big")
    packet += session_id.to_bytes(16, "big")
    packet += packet_number.to_bytes(8 , "big")
    return packet
    
    
    
def make_packet(flag: int, ssid: int, pn: int, framelist: dict) -> bytes:
    packet = b''.join(framelist)
    packet = make_packet_header(flag, len(packet), len(frame_list), ssid, pn) + packet
    return packet
    
def make_frame_header(frame_type: int, flag: int, frame: bytes) -> bytes:
    return frame_type.to_bytes(1, "big") + flag.to_bytes(1, "big")  + len(frame).to_bytes(2, "big")

                #data frame: gom 4 byte header + 
                # 8B       8B              8B
def make_data_frame(flag: int, stream_id: int, message_id: int, message_start_offset: int, message_length: int, offset: int, data: bytes, typ: int = StreamType.CHAT) -> bytes:
    frame = b''
    frame += stream_id.to_bytes(8, "big")
    frame += message_id.to_bytes(8, "big")
    frame += message_start_offset.to_bytes(8, "big")
    frame += message_length.to_bytes(8, "big")
    frame += offset.to_bytes(8, "big")
    frame += data
    frame += typ.to_bytes(1, "big")
    
    frame = make_frame_header(FrameType.DATA, flag, frame) + frame
    return frame 
  

def make_ack_frame(flag: int, largest_ack:int , ack_delay:int, ack_count:int, ack_ranges:tuple ) -> bytes:
    frame = b''
    frame += largest_ack.to_bytes(4, "big")
    frame += ack_delay.to_bytes(8, "big")
    frame += ack_count.to_bytes(2, "big")
    i = 0
    for r in ack_ranges:
        frame += r[0].to_bytes(4, "big")
        frame += r[1].to_bytes(4, "big")
        
    frame = make_frame_header(FrameType.ACK, flag, frame) + frame
    return frame

def make_ping_frame(flag: int, ping_id: int) -> bytes:
    frame = b''
    frame += ping_id.to_bytes(8, "big")
    
    frame = make_frame_header(FrameType.PING, flag, frame) + frame
    return frame
    
def make_pong_frame(flag: int, ping_frame: bytes) -> bytes:
    frame = b''
    frame += ping_frame[4:12]
    frame = make_frame_header(FrameType.PONG, flag, frame) + frame
    return frame


# def make_limit_frame


# def encode_frame(frame):


# def decode_frame(kind, flags, body):
    


# def encode_packet(packet):
  


# def decode_packet(data):
  

# def verify_checksum(frame):
   
