import socket
import time

from src.common.constants import (
    PacketType, DataType, INITIAL_RTO,
    MAX_PACKET_SIZE,
)
from src.protocol.packet import (
    make_ack_packet, parse_packet, make_packet,
    make_data_body, decode_data_body, decode_packet_header,
)


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
        self.endpoint = endpoint
        self.address = address
        self.session_id = session_id

        self.next_pn = 0
        self.send_base = 0  # first unacked
        self.duplicate_acks_count = 0
        self.unacked_packets = {}
        self.queue_data = []

        self.srtt = None
        self.rttvar = None
        self.rto = INITIAL_RTO
        self.deadline = None

    def send_packet(self):
        if not self.queue_data:
            return

        now = time.monotonic()
        packet = make_packet(PacketType.DATA, self.session_id, self.next_pn, self.queue_data[0])
        self.endpoint.udp_send(packet, self.address)

        self.unacked_packets[self.next_pn] = {
            "packet": packet, "sent_at": now, "retransmitted": False,
        }

        if self.deadline is None:
            self.deadline = now + self.rto

        self.queue_data.pop(0)
        self.next_pn += 1
        

    def add_data(self, message_id, message_length, offset, data, typ=DataType.CHAT):
        body = make_data_body(message_id, message_length, offset, data, typ)
        self.queue_data.append(body)

    def handle_ack(self, next_expected):
        if next_expected < self.send_base:
            return  # omit old ACK
        if next_expected == self.send_base:
            self.duplicate_acks_count += 1
            if self.duplicate_acks_count == 3:  # 3 duplicate ACKs
                self.retransmit_oldest()
            return

        now = time.monotonic()
        sample_rtt = None
        ambiguous = False
        for seq in list(self.unacked_packets):
            if seq < next_expected:
                sent = self.unacked_packets.pop(seq) 
                if sent["retransmitted"] == True:
                    ambiguous = True
                sample_rtt = now - sent["sent_at"]
        # skip this RTT if retransmitted
        if sample_rtt is not None and not ambiguous:
            self.update_rtt(sample_rtt)
        self.send_base = next_expected
        self.duplicate_acks_count= 0
        if self.unacked_packets:
            self.deadline = now + self.rto
        else:
            self.deadline = None

    def update_rtt(self, sample_rtt: float):
        if self.srtt is None or self.rttvar is None:
            self.srtt = sample_rtt
            self.rttvar = sample_rtt / 2
        else:
            self.rttvar = 0.75 * self.rttvar + 0.25 * abs(self.srtt - sample_rtt)
            self.srtt = 0.875 * self.srtt + 0.125 * sample_rtt
        self.rto = max(INITIAL_RTO, self.srtt + 4 * self.rttvar)

    def retransmit_oldest(self):
        if not self.unacked_packets:
            return
        sent = self.unacked_packets[self.send_base]  # only retransmit first missing packet
        self.endpoint.udp_send(sent["packet"], self.address)
        sent["retransmitted"] = True
        self.deadline = time.monotonic() + self.rto

    def check_timeout(self):
        if self.deadline is not None and time.monotonic() >= self.deadline:
            self.rto *= 2
            self.duplicate_acks_count = 0
            self.retransmit_oldest()


class Receiver:
    def __init__(self, endpoint):
        self.endpoint = endpoint
    
        self.next_expected = 0
        self.buffered_packets = {}
        self.ready_packets = []

    def receive_packet(self, packet):
        header, body = parse_packet(packet)
        packet_type, _, _, seq = decode_packet_header(header)
        if packet_type != PacketType.DATA:
            return

        if seq >= self.next_expected:
            if seq not in self.buffered_packets:
                self.buffered_packets[seq] = body
            
        while self.next_expected in self.buffered_packets:
            body = self.buffered_packets.pop(self.next_expected)
            self.ready_packets.append(body)  # move ready queue once filled
            self.next_expected += 1

    def pop_packet(self):
        if not self.ready_packets:
            return
        
        body = self.ready_packets.pop(0)
        return decode_data_body(body)

    def send_ack(self, to, session_id):
        packet = make_ack_packet(session_id, self.next_expected, 0)
        self.endpoint.udp_send(packet, to)


# TODO: route ACK to Sender, DATA to Receiver, then send current ACK.
# Pass only next_expected from decode_ack_body() to Sender.handle_ack().
# Deliver pop_packet() results in connection order.

# TODO: Integrate flow/congestion control later; add scheduling and heartbeat timers.
