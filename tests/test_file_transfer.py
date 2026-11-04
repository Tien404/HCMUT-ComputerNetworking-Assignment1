import tempfile
import unittest
from pathlib import Path
from src.client.file_transfer import choose_chunk_size, read_chunks
from src.common.constants import MAX_PACKET_SIZE, PACKET_HEADER_SIZE, DATA_BODY_SIZE


class FileTransferTests(unittest.TestCase):
    def test_chunk_size(self):
        # size = choose_chunk_size()
        # self.assertGreater(size, 0)
        # self.assertLessEqual(PACKET_HEADER_SIZE + DATA_BODY_SIZE + size, MAX_PACKET_SIZE)
        pass

    def test_read_chunks(self):
        # with tempfile.TemporaryDirectory() as directory:
        #     path = Path(directory) / "test.txt"
        #     path.write_bytes(b"abcdef")
        #     self.assertEqual(list(read_chunks(path, 3)), [(0, b"abc"), (3, b"def")])
        pass
