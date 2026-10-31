from src.common.constants import (
    MAX_PACKET_SIZE, INITIAL_SSTHRESH, CUBIC_BETA, CUBIC_C, CongestionPhase,
)


def new_congestion():
    cwnd = 10 * MAX_PACKET_SIZE
    return {"max_datagram_size": MAX_PACKET_SIZE, "cwnd": float(cwnd),
            "ssthresh": INITIAL_SSTHRESH, "bytes_in_flight": 0,
            "w_max": float(cwnd), "cwnd_epoch": float(cwnd), "t_epoch": None,
            "k": 0.0, "w_est": float(cwnd), "c_bytes": CUBIC_C * MAX_PACKET_SIZE,
            "beta": CUBIC_BETA, "phase": CongestionPhase.SLOW_START,
            "recovery_start_time": None, "next_send_time": 0.0}


def can_send(state, packet_size, now, ack_only=False):
    if type(packet_size) is not int or not 0 < packet_size <= state["max_datagram_size"]:
        return False
    return ack_only or (now >= state["next_send_time"]
                        and state["bytes_in_flight"] + packet_size <= state["cwnd"])


def on_ack(state, bytes_acked, now, rtt):
    pass


def on_loss(state, now, flight_before_removal, timeout=False):
    pass
