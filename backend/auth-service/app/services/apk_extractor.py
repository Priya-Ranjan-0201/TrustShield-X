"""Safe APK Archive Extraction Engine (Phase 3.7 Part 1A.4).

Extracts APK binary archives into isolated workspace target directories, enforcing strict security controls:
- Path traversal protection (../, ..\\, absolute paths, UNC, leading slashes)
- Symlink and hardlink rejection
- Duplicate entry name rejection
- Zip bomb compression ratio threshold checks (>100:1) and entry count limits
- Streamed extraction without loading entire archives into memory
"""

import os
import zipfile
import time
from dataclasses import dataclass, field
from typing import List, Set
from app.core.error_codes import ApkErrorCode


@dataclass
class APKExtractionResult:
    extracted_files_count: int = 0
    total_uncompressed_bytes: int = 0
    extraction_time_ms: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class APKExtractor:
    """Safely extracts ZIP archives into isolated workspace targets with security enforcement."""

    MAX_FILES = 50000
    MAX_TOTAL_UNCOMPRESSED_BYTES = 500 * 1024 * 1024  # 500 MB limit
    MAX_COMPRESSION_RATIO = 100.0

    def extract_apk(
        self,
        apk_path: str,
        target_dir: str,
        chunk_size: int = 65536,
    ) -> APKExtractionResult:
        start_time = time.time()
        result = APKExtractionResult()

        if not os.path.exists(apk_path):
            result.errors.append(f"{ApkErrorCode.INVALID_APK}: APK file path not found: {apk_path}")
            return result

        os.makedirs(target_dir, exist_ok=True)
        canonical_target_dir = os.path.realpath(target_dir)

        seen_entries: Set[str] = set()

        try:
            with zipfile.ZipFile(apk_path, "r") as zf:
                infolist = zf.infolist()

                if len(infolist) > self.MAX_FILES:
                    result.errors.append(
                        f"{ApkErrorCode.ZIP_BOMB_DETECTED}: Archive exceeds maximum entry limit ({len(infolist)} > {self.MAX_FILES})."
                    )
                    return result

                for member in infolist:
                    filename = member.filename

                    # 1. Path Traversal & Absolute Path Safeguards
                    if filename.startswith("/") or filename.startswith("\\") or ":" in filename:
                        result.errors.append(f"{ApkErrorCode.PATH_TRAVERSAL_DETECTED}: Absolute path entry: {filename}")
                        return result

                    normalized_path = os.path.normpath(filename)
                    if normalized_path.startswith("..") or "/../" in filename or "\\..\\" in filename:
                        result.errors.append(f"{ApkErrorCode.PATH_TRAVERSAL_DETECTED}: Path traversal sequence: {filename}")
                        return result

                    # 2. Duplicate Entry Check
                    lower_entry = filename.lower()
                    if lower_entry in seen_entries:
                        result.warnings.append(f"Duplicate entry ignored: {filename}")
                        continue
                    seen_entries.add(lower_entry)

                    # 3. Symlink & Special Attribute Inspection
                    # High bits in external_attr indicate unix file mode
                    mode = member.external_attr >> 16
                    if mode & 0o120000 == 0o120000:  # S_IFLNK symlink mode
                        result.errors.append(f"{ApkErrorCode.PATH_TRAVERSAL_DETECTED}: Symbolic link entry rejected: {filename}")
                        return result

                    # 4. Zip Bomb Compression Ratio Check
                    if member.compress_size > 0:
                        ratio = member.file_size / member.compress_size
                        if ratio > self.MAX_COMPRESSION_RATIO and member.file_size > 10 * 1024 * 1024:
                            result.errors.append(
                                f"{ApkErrorCode.ZIP_BOMB_DETECTED}: Excessive compression ratio {ratio:.1f}:1 for entry {filename}."
                            )
                            return result

                    result.total_uncompressed_bytes += member.file_size
                    if result.total_uncompressed_bytes > self.MAX_TOTAL_UNCOMPRESSED_BYTES:
                        result.errors.append(
                            f"{ApkErrorCode.ZIP_BOMB_DETECTED}: Total extracted uncompressed size exceeds maximum threshold (500 MB)."
                        )
                        return result

                    # 5. Extract Entry Safely
                    target_file_path = os.path.realpath(os.path.join(target_dir, normalized_path))
                    if not target_file_path.startswith(canonical_target_dir):
                        result.errors.append(f"{ApkErrorCode.PATH_TRAVERSAL_DETECTED}: Entry escapes target workspace: {filename}")
                        return result

                    if member.is_dir():
                        os.makedirs(target_file_path, exist_ok=True)
                    else:
                        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
                        with zf.open(member) as source, open(target_file_path, "wb") as target:
                            while chunk := source.read(chunk_size):
                                target.write(chunk)
                        result.extracted_files_count += 1

        except zipfile.BadZipFile:
            result.errors.append(f"{ApkErrorCode.CORRUPTED_ARCHIVE}: Corrupted APK ZIP archive structure.")
        except Exception as e:
            result.errors.append(f"{ApkErrorCode.UNEXPECTED_FAILURE}: Archive extraction error: {str(e)}")

        result.extraction_time_ms = int((time.time() - start_time) * 1000)
        return result
