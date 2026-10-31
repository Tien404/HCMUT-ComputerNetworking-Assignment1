from src.common.constants import MAX_U64, FrameType
from src.protocol.packet import make_limit


def check_end(offset, length=0):
    if any(type(value) is not int or value < 0 for value in (offset, length)):
        raise ValueError("Invalid offset or length")
    if offset + length > MAX_U64:
        raise ValueError("Offset overflow")
    return offset + length


def new_sender_flow(max_data):
    return {"max_data": check_end(max_data), "total_committed_data": 0,
            "streams": {}, "used_stream_ids": set()}


def add_sender_stream(flow, stream_id, max_stream_data):
    check_end(stream_id)
    if stream_id in flow["used_stream_ids"]:
        raise ValueError("Stream IDs must not be reused")
    flow["streams"][stream_id] = {"max_stream_data": check_end(max_stream_data),
                                  "highest_sent_offset": 0}
    flow["used_stream_ids"].add(stream_id)


def stage_send(flow, ranges):
    # TODO: Stage the maximum end offset per stream across all DATA frames.
    # TODO: Check stream limits and total_committed_data + additional_credit <= max_data.
    # TODO: Additional credit is max(0, end - highest_sent_offset); retries use no new credit.
    # TODO: Return (staged_offsets, extra_credit) without mutating state.
    pass


def can_send(flow, ranges):
    # TODO: Check the whole packet through stage_send; do not change flow state.
    pass


def commit_sent(flow, ranges):
    # TODO: Commit staged offsets/credit after the local socket accepts the datagram.
    # TODO: Keep historical credit after a completed stream is removed.
    pass


def on_max_data(flow, limit):
    flow["max_data"] = max(flow["max_data"], check_end(limit))


def on_max_stream_data(flow, stream_id, limit):
    stream = flow["streams"][stream_id]
    stream["max_stream_data"] = max(stream["max_stream_data"], check_end(limit))


def new_receiver_flow(connection_capacity):
    capacity = check_end(connection_capacity)
    return {"connection_receive_capacity": capacity, "advertised_max_data": capacity,
            "total_consumed_data": 0, "received_total": 0, "streams": {}}


def add_receiver_stream(flow, stream_id, receive_capacity):
    check_end(stream_id)
    if stream_id in flow["streams"]:
        raise ValueError("Stream already exists")
    capacity = check_end(receive_capacity)
    flow["streams"][stream_id] = {
        "receive_capacity": capacity, "advertised_max_stream_data": capacity,
        "highest_received_offset": 0, "consumed_offset": 0,
    }


def accept_packet(flow, ranges):
    # TODO: Stage all received offsets; check both advertised limits before mutation.
    # TODO: The caller must validate metadata and reserve/store every DATA frame first.
    # TODO: Duplicates consume no additional credit; flow acceptance alone does not allow ACK.
    pass


def on_contiguous_consumed(flow, stream_id, new_offset):
    # TODO: Count newly consumed contiguous bytes exactly once.
    # TODO: Stream limit = consumed_offset + receive_capacity.
    # TODO: Connection limit = total_consumed_data + connection_receive_capacity.
    # TODO: Return MAX_STREAM_DATA and MAX_DATA frames; limits only increase.
    pass


def blocked_frames(flow, stream_id, offset, length):
    # TODO: Return STREAM_DATA_BLOCKED and/or DATA_BLOCKED with current limits.
    # TODO: Coalesce repeated notifications and handle lost MAX updates.
    pass
