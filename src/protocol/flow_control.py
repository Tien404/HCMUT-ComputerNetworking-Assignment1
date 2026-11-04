from src.common.constants import RECEIVE_WINDOW


def can_send(send_base, next_sequence, receive_window):
    # return next_sequence < send_base + receive_window
    pass


def advertised_window(ready_packets, capacity=RECEIVE_WINDOW):
    # Out-of-order packets already occupy positions inside this sequence window.
    # Subtract only the in-order packets still waiting for the application.
    # return capacity - len(ready_packets)
    pass


def can_receive(next_expected, sequence, receive_window):
    # return next_expected <= sequence < next_expected + receive_window
    pass


# TODO: Probe a zero window periodically; reply with the current ACK/window.
# An ordinary window update may be lost, so the sender must not wait forever.
