"""Native Library Scanner for AI Android APK Security Engine (Phase 3.7 Part 1A Message 2).

Extracts and inventories native ELF libraries (.so files) across target architectures:
- armeabi
- armeabi-v7a
- arm64-v8a
- x86
- x86_64
- riscv64

Performs passive inventory only — NEVER executes machine code or inspects assembly instructions.
"""

import os
import hashlib
from typing import List, Tuple
from app.schemas.apk_models import NativeLibraryMetadata, NativeLibrarySummary

SUPPORTED_ARCHITECTURES = ("armeabi", "armeabi-v7a", "arm64-v8a", "x86", "x86_64", "riscv64")


class NativeLibraryScanner:
    """Production Native ELF Library Inventory Scanner."""

    def scan_native_libraries(self, lib_entries: List[Tuple[str, bytes]]) -> NativeLibrarySummary:
        """Scans list of (filename_path, content_bytes) tuples representing .so files under lib/."""
        if not lib_entries:
            return NativeLibrarySummary()

        libraries: List[NativeLibraryMetadata] = []
        archs_found = set()
        tot_size = 0
        largest_name = None
        largest_size = 0

        for path, content in lib_entries:
            lower_path = path.lower()
            if not lower_path.startswith("lib/") or not lower_path.endswith(".so"):
                continue

            parts = path.split("/")
            # Expected format: lib/<architecture>/<library_name>.so
            arch = "unknown"
            if len(parts) >= 3:
                arch = parts[1]

            if arch in SUPPORTED_ARCHITECTURES:
                archs_found.add(arch)

            lib_name = os.path.basename(path)
            size = len(content)
            sha256 = hashlib.sha256(content).hexdigest()
            tot_size += size

            if size > largest_size:
                largest_size = size
                largest_name = lib_name

            libraries.append(
                NativeLibraryMetadata(
                    library_name=lib_name,
                    architecture=arch,
                    size=size,
                    sha256=sha256,
                    path=path,
                )
            )

        count = len(libraries)
        avg_size = round(tot_size / count, 2) if count > 0 else 0.0

        return NativeLibrarySummary(
            library_count=count,
            architectures_present=sorted(list(archs_found)),
            largest_library_name=largest_name,
            largest_library_bytes=largest_size,
            average_library_size_bytes=avg_size,
            libraries=libraries,
        )
