"""Artifact Storage Provider Abstraction (Phase 4.0 Part 3 — Sections 48-49).

Provides pluggable storage provider interface (Local, S3, Azure, GCP) with safe
path handling and traversal protection.
"""

import os
import re
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal and unsafe characters (Section 47)."""
    # Remove directory separators and null bytes
    cleaned = os.path.basename(filename)
    cleaned = re.sub(r'[\x00-\x1f\x7f<>:"/\\|?*]', '_', cleaned)
    if not cleaned or cleaned.startswith('.'):
        cleaned = f"report_artifact_{cleaned}"
    return cleaned


class ArtifactStorageProvider(ABC):
    """Abstract interface for storing and retrieving rendered report artifacts."""

    @abstractmethod
    def put(self, key: str, data: bytes, content_type: str = "application/octet-stream") -> str:
        """Store artifact data and return storage location reference."""
        pass

    @abstractmethod
    def get(self, key: str) -> Optional[bytes]:
        """Retrieve artifact bytes by key."""
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete an artifact by key."""
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if an artifact exists."""
        pass

    @abstractmethod
    def metadata(self, key: str) -> Optional[Dict[str, Any]]:
        """Return artifact metadata (size, mime type, etc.)."""
        pass


class LocalStorageProvider(ArtifactStorageProvider):
    """Local filesystem storage provider with path isolation and directory creation."""

    def __init__(self, base_dir: str = "storage/artifacts"):
        self.base_dir = os.path.abspath(base_dir)
        os.makedirs(self.base_dir, exist_ok=True)

    def _resolve_path(self, key: str) -> str:
        safe_key = sanitize_filename(key)
        resolved = os.path.abspath(os.path.join(self.base_dir, safe_key))
        # Enforce path isolation — prevent directory traversal
        if not resolved.startswith(self.base_dir):
            raise ValueError(f"TSX-REPORT-601: Path traversal attempt detected: '{key}'.")
        return resolved

    def put(self, key: str, data: bytes, content_type: str = "application/octet-stream") -> str:
        path = self._resolve_path(key)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)
        return path

    def get(self, key: str) -> Optional[bytes]:
        path = self._resolve_path(key)
        if not os.path.exists(path):
            return None
        with open(path, "rb") as f:
            return f.read()

    def delete(self, key: str) -> bool:
        path = self._resolve_path(key)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False

    def exists(self, key: str) -> bool:
        path = self._resolve_path(key)
        return os.path.exists(path)

    def metadata(self, key: str) -> Optional[Dict[str, Any]]:
        path = self._resolve_path(key)
        if not os.path.exists(path):
            return None
        stat = os.stat(path)
        return {
            "size_bytes": stat.st_size,
            "modified_time": stat.st_mtime,
            "path": path,
        }
