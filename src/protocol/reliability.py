import socket
import time

from src.common.constants import (
    FrameType,    INITIAL_RTT, MAX_ACK_DELAY, ACK_DELAY_EXPONENT,
    INITIAL_RECEIVE_CAPACITY, HEARTBEAT_INTERVAL, SESSION_TIMEOUT,
    StreamType, ConnectionState,
)
from src.protocol.packet import (make_ack_frame, parse_packet, decode_frame, make_packet, make_data_frame, decode_packet_header)
# from src.protocol.flow_control import new_sender_flow, new_receiver_flow
# from src.protocol.congestion_control import new_congestion

class UnReliableSocket:
    def __init__(self, address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(address)

    def udp_send(self, data, to):
        self.sock.sendto(data, to)

    def udp_receive(self, bufsize=4096):
        data, addr = self.sock.recvfrom(bufsize)
        return data, addr


class Sender:

    def __init__(self, endpoint, address, session_id):
        self.endpoint = UnReliableSocket(address)
        self.address = address
        self.session_id = session_id

        self.next_packet_number = 0
        self.unacked_packets = {}
        self.buffered_frames = []

    def send_packet(self):
        if not self.buffered_frames:
            return

        packet = make_packet(0, self.session_id, self.next_packet_number, self.buffered_frames)
        self.unacked_packets[self.next_packet_number] = packet
        self.endpoint.udp_send(packet, self.address)

        self.next_packet_number += 1
        self.buffered_frames = []

    def add_data_frame(self, stream_id, message_id, message_start_offset, message_length, offset, data):
        frame = make_data_frame(0, stream_id, message_id, message_start_offset, message_length, offset, data)
        self.buffered_frames.append(frame)
        return 

    def handle_ack_frame(self, ack_frame):
        _ , _ , _ , ack_ranges = decode_frame(FrameType.ACK, ack_frame)
        for range_ in ack_ranges:
            start, end = range_
            for pn in list(self.unacked_packets.keys()):
                if start <= pn <= end:
                    del self.unacked_packets[pn]



    def retransmit_unacked_packets(self):
        for packet_number, packet in self.unacked_packets.items():
            self.endpoint.udp_send(packet, self.address)
     

class Receiver:

    def __init__(self, address):
        self.endpoint = UnReliableSocket(address)
        self.buffered_frames = {}
        self.largest_acked = None
        self.ranges_count = 0
        self.received_ranges = set()
        self.ack_delay = 0

    def receive_packet(self, packet):
        packet_header , frame_list = parse_packet(packet)

        packet_number = decode_packet_header(packet_header)[4]
        if packet_number in self.received_ranges:
            return  # Duplicate packet, ignore
        
        for frame in frame_list:
            frame_type, _ , frame_data = decode_frame(frame[0], frame[1:])
            if frame_type == FrameType.DATA:
                self.handle_data_frame(frame_data)

        self.update_ack(packet_number)  

    def update_ack(self, packet_number):
       self.received_ranges.add(packet_number)

    def get_ack_ranges(self):
        
        ranges = []

        for pn in sorted(self.received_ranges):
            if ranges and pn == ranges[-1][1] + 1:
                ranges[-1][1] = pn
            else:
                ranges.append([pn, pn])
        return ranges
    
    
    def handle_data_frame(self, frame_data):
        stream_id, message_id, message_start_offset, message_length, offset, data, typ = frame_data
        # Process the received data frame (e.g., store it, update state, etc.)
    
    def send_ack_frame(self, to):
        ack_ranges = self.get_ack_ranges()
        ack_frame = make_ack_frame(0, self.largest_acked, self.ack_delay, len(ack_ranges), ack_ranges)

    
    
        



# def new_rtt():
#     return {"srtt": INITIAL_RTT, "rttvar": INITIAL_RTT / 2,
#             "latest_rtt": INITIAL_RTT, "min_rtt": None}


# def update_rtt(rtt, latest, ack_delay=0.0, max_ack_delay=MAX_ACK_DELAY):
#     # TODO: Only sample a newly ACKed largest PN when a newly ACKed packet is ack-eliciting.
#     # TODO: Track latest/minimum/smoothed RTT and variation using the proposal formulas.
#     # TODO: Clamp peer ACK delay after handshake; never adjust below the raw minimum RTT.
#     pass


# def loss_delay(rtt):
#     # TODO: Return max(9/8 * max(srtt, latest_rtt), time_granularity).
#     pass


# def custom_timeout(rtt, timeout_count, max_ack_delay=MAX_ACK_DELAY):
#     # TODO: Return (srtt + max(4*rttvar, granularity) + max_ack_delay) * 2**timeout_count.
#     pass


# def new_connection(session_id=b"\0" * 16, peer_id=None, peer_addr=None):
#     return {
#         "session_id": session_id, "peer_id": peer_id, "peer_addr": peer_addr,
#         "state": ConnectionState.NEW, "next_packet_number": 0,
#         "next_message_id": 0,  # Shared chat/file order in the conversation, not per stream.
#         "sent_packets": {}, "events": {}, "received_packet_ranges": [],
#         "streams": {}, "control_queue": [], "retry_queue": [],
#         "tx_flow": new_sender_flow(0),  # Handshake supplies initial flow limits.
#         "rx_flow": new_receiver_flow(INITIAL_RECEIVE_CAPACITY),
#         "rtt": new_rtt(), "congestion": new_congestion(),
#         "ack_delay_exponent": ACK_DELAY_EXPONENT, "max_ack_delay": MAX_ACK_DELAY,
#         "ack_deadline": None, "loss_time": None, "rto_deadline": None,
#         "largest_acknowledged": None, "timeout_count": 0,
#         "last_authenticated_receive": 0.0, "last_ping_submitted": 0.0,
#         "generation": 0,
#     }


# def new_sent_packet(pn, now, size, ack_eliciting, data_refs=(), control_refs=()):
#     # data_refs: (stream_id, message_id, start, end, confirms_empty_metadata).
#     return {"packet_number": pn, "sent_at": now, "packet_size": size,
#             "ack_eliciting": ack_eliciting, "data_refs": tuple(data_refs),
#             "control_refs": tuple(control_refs), "counted_in_flight": False,
#             "acknowledged": False, "declared_lost": False}


# def new_event(stream_id, message_id, message_start_offset, message_length):
#     return {"stream_id": stream_id, "message_id": message_id,
#             "message_start_offset": message_start_offset, "message_length": message_length,
#             "acked_ranges": [], "empty_metadata_acked": False, "completion_reported": False}


# def new_stream(kind, local_sends=True):
#     return {"kind": StreamType(kind), "local_sends": local_sends,
#             "next_offset": 0, "messages": {}, "queue": [],
#             "received_ranges": [], "consumed_offset": 0}


# def enqueue_message(connection, stream_id, content, metadata=b""):
#     # TODO: Allocate message IDs across chat/file within the conversation.
#     # TODO: Enforce one-way streams and bounded admission; each file starts at offset 0.
#     # TODO: Chunking a file must not block chat admission.
#     pass


# async def recv_stream(stream):
#     # TODO: Reject send-only streams; await this stream's inbox without blocking other streams.
#     pass


# def add_range(ranges, start, end):
#     # TODO: Merge overlapping/adjacent half-open byte ranges; ignore duplicates and empty ranges.
#     pass


# def missing_ranges(ranges, start, end):
#     # TODO: Return only uncovered portions of [start, end) from normalized byte ranges.
#     pass


# def is_complete(ranges, start, size):
#     # TODO: Check full byte coverage, not just the largest received offset.
#     pass


# def all_data_acked(event):
#     # TODO: Check the event's complete byte coverage; empty messages need a metadata ACK.
#     pass


# def heartbeat_due(connection, now):
#     latest = max(connection["last_authenticated_receive"], connection["last_ping_submitted"])
#     return (connection["state"] == ConnectionState.ESTABLISHED
#             and not idle_expired(connection, now) and now - latest >= HEARTBEAT_INTERVAL)


# def idle_expired(connection, now):
#     return now - connection["last_authenticated_receive"] >= SESSION_TIMEOUT


# def on_authenticated_heartbeat(connection, kind, now):
#     # TODO: Accept only validated PING/PONG on established sessions.
#     # TODO: Refresh receive-idle; reply PONG only to PING, never to PONG.
#     # TODO: PONG does not ACK DATA or advance message completion.
#     pass


# def close_connection(connection):
#     # TODO: Mark closing and advance generation to invalidate old callbacks.
#     # TODO: Cancel/await owned tasks and timers, close transport, clean streams/temp files.
#     pass


# def next_packet(connection, now):
#     # TODO: Prioritize control/ACK, fairly select streams and pack multiple frames within MTU.
#     # TODO: DATA/retries obey both flow credits, cwnd and pacing; ACK-only bypasses cwnd.
#     # TODO: Allocate fresh connection-wide PNs; retries retain stream/message/offset.
#     pass


# def on_ack(connection, frame, now):
#     # TODO: Validate all ranges against actual sent history before any state mutation.
#     # TODO: Map every PN to all DATA/control references; union acknowledged coverage.
#     # TODO: Retire in-flight bytes and report completion once; late ACKs cancel unnecessary retries.
#     # TODO: Decode ACK delay units into seconds; apply RTT eligibility rules.
#     # TODO: ACKs do not return flow credit; evaluate loss/recovery before CUBIC growth.
#     pass


# def check_timeouts(connection, now):
#     # TODO: A lost packet is unacknowledged/in flight and has later-ACK evidence.
#     # TODO: Use distance >= 3 or elapsed >= loss_delay; one loss timer per session.
#     # TODO: Prefer loss_time; arm custom RTO/backoff only if there is no loss_time.
#     # TODO: Requeue only unconfirmed data/control with fresh PNs; retain history for late ACKs.
#     # TODO: Retries consume congestion budget, not additional byte-flow credit.
#     pass


# def receive_packet(connection, packet, now):
#     # TODO: Verify/decrypt before decoding or mutating session state; check session/address.
#     # TODO: Stage all frames, metadata, quota/storage and checksum requirements before ACK.
#     # TODO: Dispatch DATA, ACK, MAX, BLOCKED and PING/PONG independently.
#     # TODO: Track received PN ranges and delayed ACKs; piggyback ACKs when possible.
#     # TODO: ACK-only must not trigger an ACK loop; only valid traffic refreshes liveness.
#     pass


# async def run_timers(connection):
#     # TODO: Schedule loss/RTO, ACK delay, pacing, heartbeat and receive-idle timers with asyncio.
#     # TODO: Use monotonic time and recheck state/generation before each callback.
#     pass
