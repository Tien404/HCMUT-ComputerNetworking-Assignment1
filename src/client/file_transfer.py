from pathlib import Path
from src.common.constants import CHUNK_SIZE, MAX_PACKET_SIZE
from src.protocol.packet import HEADER, FRAME_HEADER, DATA_BODY


def choose_chunk_size(metadata_bytes, security_overhead=0):
    if metadata_bytes < 0 or security_overhead < 0:
        raise ValueError("Invalid overhead")
    budget = MAX_PACKET_SIZE - HEADER.size - FRAME_HEADER.size - DATA_BODY.size
    budget -= metadata_bytes + security_overhead
    if budget <= 0:
        raise ValueError("No space left for DATA")
    return min(CHUNK_SIZE, budget)


def read_chunks(path, chunk_size):
    # Choose chunk_size once per transfer; run blocking reads via asyncio.to_thread.
    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive")
    with Path(path).open("rb") as file:
        offset = 0
        while chunk := file.read(chunk_size):
            yield offset, chunk
            offset += len(chunk)


async def send_file(connection, path):
    # TODO: Allocate a conversation-wide message ID and a new one-way stream at offset 0.
    # TODO: Keep size/name metadata consistent and retain the source until all data/metadata ACKs.
    # TODO: Use the shared scheduler, flow credit and CUBIC rather than a separate file ACK loop.
    pass


async def receive_chunk(transfer, frame):
    # TODO: Validate metadata/offset/quota before storage admission and packet ACK.
    # TODO: Generate safe temp paths; write by offset via asyncio.to_thread.
    # TODO: Track coverage/dedup in RAM; consume incrementally to advertise new byte credit.
    # TODO: Finalize only with complete coverage; empty files need metadata, not FILE_DONE.
    # TODO: Coordinate worker I/O with error/cancellation/timeout cleanup.
    pass
