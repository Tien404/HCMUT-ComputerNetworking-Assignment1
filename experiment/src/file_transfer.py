"""Small file-transfer helpers; network retry and reassembly come later."""

import hashlib
from pathlib import Path


def read_chunks(path, chunk_size=1024):
    """Yield ``(offset, bytes)`` pairs from a file."""
    if type(chunk_size) is not int or chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")

    offset = 0
    with Path(path).open("rb") as source:
        while chunk := source.read(chunk_size):
            yield offset, chunk
            offset += len(chunk)


def sha256_file(path):
    """Return the lowercase SHA-256 digest of a file."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for chunk in iter(lambda: source.read(64 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_sha256(path, expected_digest):
    """Check a file digest, accepting hexadecimal SHA-256 strings only."""
    if not isinstance(expected_digest, str) or len(expected_digest) != 64:
        raise ValueError("expected_digest must be a 64-character SHA-256 hex string")
    try:
        int(expected_digest, 16)
    except ValueError as exc:
        raise ValueError("expected_digest must be hexadecimal") from exc
    return sha256_file(path).lower() == expected_digest.lower()
