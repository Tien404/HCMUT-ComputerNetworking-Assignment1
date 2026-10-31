import tempfile
import unittest
from pathlib import Path
from src.client.file_transfer import choose_chunk_size, read_chunks
from src.common.constants import MAX_PACKET_SIZE
from src.protocol.packet import HEADER, FRAME_HEADER, DATA_BODY


class FileTransferTests(unittest.TestCase):
    def test_chunk_budget_counts_metadata_and_security(self):
        chunk = choose_chunk_size(200, 16)
        self.assertLessEqual(HEADER.size + FRAME_HEADER.size + DATA_BODY.size + 200 + 16 + chunk,
                             MAX_PACKET_SIZE)
        with self.assertRaises(ValueError):
            choose_chunk_size(MAX_PACKET_SIZE)

    def test_chunk_offsets_and_empty_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.bin"
            path.write_bytes(b"abcdefgh")
            self.assertEqual(list(read_chunks(path, 3)), [(0, b"abc"), (3, b"def"), (6, b"gh")])
            path.write_bytes(b"")
            self.assertEqual(list(read_chunks(path, 3)), [])
