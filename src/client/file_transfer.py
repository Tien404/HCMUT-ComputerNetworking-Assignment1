from pathlib import Path
from src.common.constants import (
    CHUNK_SIZE, MAX_PACKET_SIZE, PACKET_HEADER_SIZE, DATA_BODY_SIZE,
)


def choose_chunk_size(security_overhead=0):
    # budget = MAX_PACKET_SIZE - PACKET_HEADER_SIZE - DATA_BODY_SIZE
    # budget -= security_overhead
    # if budget <= 0:
    #     raise ValueError("No space left for DATA")
    # return min(CHUNK_SIZE, budget)
    pass


def read_chunks(path, chunk_size):
    # Choose chunk_size once per transfer; run blocking reads via asyncio.to_thread.
    # with Path(path).open("rb") as file:
    #     offset = 0
    #     chunk = file.read(chunk_size)
    #     while chunk:
    #         yield offset, chunk
    #         offset += len(chunk)
    #         chunk = file.read(chunk_size)
    pass


async def send_file(connection, path):
    # TODO: Queue file metadata and chunks, keeping the file until cumulatively ACKed.
    # TODO: Alternate file/chat chunks; use the connection's shared sequence, rwnd and CUBIC.
    # TODO: Allocate one message_id from the same counter used for chat.
    # All chunks of this file keep that ID; their offset starts at zero.
    pass


async def receive_chunk(transfer, chunk):
    # TODO: Consume chunks from Receiver.pop_packet() in connection order and write to disk.
    # TODO: Send a window update after consuming packets; include metadata for empty files.
    # TODO: Check final size/hash, report completion and clean up temporary files.
    pass
