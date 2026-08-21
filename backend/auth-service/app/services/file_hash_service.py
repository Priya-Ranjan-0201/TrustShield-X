"""Cryptographic File Hashing Service for APK Workspace Artifacts (Phase 3.7 Part 1A.4).

Computes SHA256, SHA1, MD5, and CRC32 digests via 64KB chunked streaming reads,
maintaining an internal cache to prevent redundant recalculations.
"""

import os
import hashlib
import zlib
from dataclasses import dataclass
from typing import Dict, Tuple, Optional


@dataclass
class FileHashResult:
    sha256: str
    sha1: str
    md5: str
    crc32: str


class FileHashService:
    """Computes streaming digests for files with internal path-based hash caching."""

    def __init__(self, chunk_size: int = 65536):
        self.chunk_size = chunk_size
        self._hash_cache: Dict[Tuple[str, int, float], FileHashResult] = {}

    def compute_file_hashes(self, file_path: str) -> FileHashResult:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found for hashing: {file_path}")

        stat = os.stat(file_path)
        cache_key = (file_path, stat.st_size, stat.st_mtime)
        if cache_key in self._hash_cache:
            return self._hash_cache[cache_key]

        sha256_hash = hashlib.sha256()
        sha1_hash = hashlib.sha1()
        md5_hash = hashlib.md5()
        crc32_val = 0

        with open(file_path, "rb") as f:
            while chunk := f.read(self.chunk_size):
                sha256_hash.update(chunk)
                sha1_hash.update(chunk)
                md5_hash.update(chunk)
                crc32_val = zlib.crc32(chunk, crc32_val)

        result = FileHashResult(
            sha256=sha256_hash.hexdigest(),
            sha1=sha1_hash.hexdigest(),
            md5=md5_hash.hexdigest(),
            crc32=f"{crc32_val & 0xFFFFFFFF:08x}",
        )

        self._hash_cache[cache_key] = result
        return result

    def compute_bytes_hashes(self, data: bytes) -> FileHashResult:
        sha256 = hashlib.sha256(data).hexdigest()
        sha1 = hashlib.sha1(data).hexdigest()
        md5 = hashlib.md5(data).hexdigest()
        crc32 = f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"
        return FileHashResult(sha256=sha256, sha1=sha1, md5=md5, crc32=crc32)
