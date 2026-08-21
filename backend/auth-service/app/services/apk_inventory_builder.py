"""APK Workspace File Inventory Builder Engine (Phase 3.7 Part 1A.4).

Scans workspace files, computes Shannon file entropy, determines MIME types,
invokes FileClassifier & FileHashService, and generates structured inventory.json.
"""

import os
import math
import json
import mimetypes
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from app.services.file_classifier import FileClassifier, FileCategory
from app.services.file_hash_service import FileHashService, FileHashResult


@dataclass
class FileInventoryEntry:
    relative_path: str
    file_name: str
    extension: str
    mime_type: str
    size: int
    compressed_size: int
    sha256: str
    sha1: str
    md5: str
    crc32: str
    entropy: float
    is_executable: bool
    is_archive: bool
    is_binary: bool
    created_timestamp: float
    modified_timestamp: float
    compression_ratio: float
    category: str


@dataclass
class WorkspaceInventory:
    total_files: int = 0
    total_directories: int = 0
    total_bytes: int = 0
    categories_summary: Dict[str, int] = field(default_factory=dict)
    entries: List[FileInventoryEntry] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_files": self.total_files,
            "total_directories": self.total_directories,
            "total_bytes": self.total_bytes,
            "categories_summary": self.categories_summary,
            "entries": [asdict(e) for e in self.entries],
        }


class APKInventoryBuilder:
    """Scans extracted workspace files and builds comprehensive inventory metadata."""

    def __init__(self, hash_service: Optional[FileHashService] = None):
        self.hash_service = hash_service or FileHashService()

    @staticmethod
    def calculate_shannon_entropy(file_path: str) -> float:
        """Calculates Shannon entropy in bits per byte (0.0 to 8.0)."""
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            return 0.0

        byte_counts = [0] * 256
        total_bytes = 0

        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                total_bytes += len(chunk)
                for b in chunk:
                    byte_counts[b] += 1

        if total_bytes == 0:
            return 0.0

        entropy = 0.0
        for count in byte_counts:
            if count > 0:
                p = count / total_bytes
                entropy -= p * math.log2(p)

        return round(entropy, 4)

    def build_inventory(self, workspace_dir: str) -> WorkspaceInventory:
        inventory = WorkspaceInventory()
        cat_counts: Dict[str, int] = {cat.value: 0 for cat in FileCategory}

        if not os.path.exists(workspace_dir):
            return inventory

        canonical_workspace = os.path.realpath(workspace_dir)

        for root, dirs, files in os.walk(workspace_dir):
            inventory.total_directories += len(dirs)

            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, canonical_workspace).replace("\\", "/")

                if rel_path in ("inventory.json", "manifest.json"):
                    continue

                stat = os.stat(full_path)
                ext = os.path.splitext(file)[1].lower()
                mime, _ = mimetypes.guess_type(full_path)
                mime = mime or "application/octet-stream"

                header_bytes = b""
                try:
                    with open(full_path, "rb") as f:
                        header_bytes = f.read(512)
                except Exception:
                    pass

                category = FileClassifier.classify_file(rel_path, header_bytes, mime)
                hashes = self.hash_service.compute_file_hashes(full_path)
                entropy = self.calculate_shannon_entropy(full_path)

                is_exe = category in (FileCategory.DEX, FileCategory.NATIVE_LIBRARY) or ext in (".so", ".dex", ".exe", ".elf")
                is_arch = ext in (".zip", ".apk", ".jar", ".tar", ".gz")
                is_bin = category in (FileCategory.DEX, FileCategory.NATIVE_LIBRARY, FileCategory.BINARY, FileCategory.IMAGE)

                entry = FileInventoryEntry(
                    relative_path=rel_path,
                    file_name=file,
                    extension=ext,
                    mime_type=mime,
                    size=stat.st_size,
                    compressed_size=stat.st_size,
                    sha256=hashes.sha256,
                    sha1=hashes.sha1,
                    md5=hashes.md5,
                    crc32=hashes.crc32,
                    entropy=entropy,
                    is_executable=is_exe,
                    is_archive=is_arch,
                    is_binary=is_bin,
                    created_timestamp=stat.st_ctime,
                    modified_timestamp=stat.st_mtime,
                    compression_ratio=1.0,
                    category=category.value,
                )

                inventory.entries.append(entry)
                inventory.total_files += 1
                inventory.total_bytes += stat.st_size
                cat_counts[category.value] = cat_counts.get(category.value, 0) + 1

        inventory.categories_summary = cat_counts

        # Write inventory.json into workspace root
        inventory_file_path = os.path.join(workspace_dir, "inventory.json")
        with open(inventory_file_path, "w", encoding="utf-8") as f:
            json.dump(inventory.to_dict(), f, indent=2)

        return inventory
