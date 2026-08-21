"""File Classification Engine for Extracted APK Artifacts (Phase 3.7 Part 1A.4).

Categorizes extracted APK files into standard FileCategory types using file extension,
relative workspace path, magic header bytes, and MIME classification.
"""

import os
from enum import Enum
from typing import Optional


class FileCategory(str, Enum):
    DEX = "DEX"
    NATIVE_LIBRARY = "NATIVE_LIBRARY"
    MANIFEST = "MANIFEST"
    CERTIFICATE = "CERTIFICATE"
    XML = "XML"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"
    JSON = "JSON"
    BINARY = "BINARY"
    DATABASE = "DATABASE"
    UNKNOWN = "UNKNOWN"


class FileClassifier:
    """Classifies extracted files based on relative path, magic header bytes, and extension."""

    @staticmethod
    def classify_file(
        relative_path: str,
        header_bytes: Optional[bytes] = None,
        mime_type: Optional[str] = None,
    ) -> FileCategory:
        path_lower = relative_path.lower().replace("\\", "/")
        filename = os.path.basename(path_lower)
        ext = os.path.splitext(filename)[1]

        # 1. Android Specific File Checks
        if filename == "androidmanifest.xml":
            return FileCategory.MANIFEST

        if filename.startswith("classes") and ext == ".dex":
            return FileCategory.DEX

        if header_bytes and header_bytes.startswith(b"dex\n"):
            return FileCategory.DEX

        if ext == ".so" or path_lower.startswith("lib/"):
            return FileCategory.NATIVE_LIBRARY

        if header_bytes and header_bytes.startswith(b"\x7fELF"):
            return FileCategory.NATIVE_LIBRARY

        if path_lower.startswith("meta-inf/") and (
            ext in (".rsa", ".dsa", ".ec", ".sf", ".mf") or "cert" in filename
        ):
            return FileCategory.CERTIFICATE

        # 2. Document & Data Formats
        if ext == ".xml":
            return FileCategory.XML

        if ext == ".json":
            return FileCategory.JSON

        if ext in (".db", ".sqlite", ".sqlite3") or (header_bytes and header_bytes.startswith(b"SQLite format 3")):
            return FileCategory.DATABASE

        # 3. Media Formats
        if ext in (".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".ico", ".svg"):
            return FileCategory.IMAGE

        if ext in (".ogg", ".mp3", ".wav", ".aac", ".flac", ".m4a"):
            return FileCategory.AUDIO

        if ext in (".mp4", ".mkv", ".webm", ".3gp", ".avi"):
            return FileCategory.VIDEO

        # 4. Binary & Executable Check
        if ext in (".arsc", ".bin", ".dat", ".class", ".jar"):
            return FileCategory.BINARY

        if mime_type and "octet-stream" in mime_type.lower():
            return FileCategory.BINARY

        return FileCategory.UNKNOWN
