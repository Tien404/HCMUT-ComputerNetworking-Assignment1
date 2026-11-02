import tempfile
import unittest
from pathlib import Path

from src.file_transfer import read_chunks, sha256_file, verify_sha256


class FileTransferHelperTests(unittest.TestCase):
    def test_chunks_have_contiguous_offsets(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.bin"
            path.write_bytes(b"abcdefgh")
            self.assertEqual(list(read_chunks(path, 3)),
                             [(0, b"abc"), (3, b"def"), (6, b"gh")])

    def test_empty_file_and_checksum(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.bin"
            path.write_bytes(b"")
            digest = sha256_file(path)
            self.assertEqual(list(read_chunks(path, 10)), [])
            self.assertTrue(verify_sha256(path, digest))
            self.assertFalse(verify_sha256(path, "0" * 64))

    def test_chunk_size_must_be_positive(self):
        with self.assertRaises(ValueError):
            list(read_chunks("unused", 0))


if __name__ == "__main__":
    unittest.main()
