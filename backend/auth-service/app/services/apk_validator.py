r"""APK Validation Engine for AI Android APK Security Engine (Phase 3.7 Part 1A).

Single entry point before any APK is unpacked or processed:
1. Extension Validation (.apk only; .xapk/.apkm/.aab flagged as unsupported variant)
2. MIME Type Validation
3. File Size Capping (100 MB max) & Empty File Check
4. ZIP Integrity & Central Directory Check
5. CRC-32 Checksum Validation
6. Duplicate Entry Filename Detection
7. Path Traversal Protection (../, ..\, UNC, leading slashes)
8. ZIP Bomb Protection (compression ratio > 100:1, file count > 50,000)
9. Nested Archive Safeguard
10. Streaming SHA-256 Digest Calculation

Treats every APK as a passive archive — NEVER executes Dalvik bytecode or ART runtime.
"""

import os
import zipfile
import hashlib
import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Union, Tuple
from app.core.error_codes import ApkErrorCode


@dataclass
class APKValidationResult:
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    error_code: str = ""
    apk_size: int = 0
    sha256: str = ""
    mime_type: str = "application/vnd.android.package-archive"
    archive_entries: int = 0
    validation_time_ms: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "error_code": self.error_code,
            "apk_size": self.apk_size,
            "sha256": self.sha256,
            "mime_type": self.mime_type,
            "archive_entries": self.archive_entries,
            "validation_time_ms": self.validation_time_ms,
        }


MAX_APK_SIZE_BYTES = 100 * 1024 * 1024  # 100 MB
MAX_ZIP_COMPRESSION_RATIO = 100.0  # 100:1
MAX_ARCHIVE_ENTRIES = 50000
ALLOWED_EXTENSIONS = {".apk"}
UNSUPPORTED_VARIANTS = {".xapk", ".apkm", ".aab"}
ALLOWED_MIMES = {
    "application/vnd.android.package-archive",
    "application/zip",
    "application/x-zip-compressed",
    "application/octet-stream",
}


class APKValidator:
    """Production APK Security Validation Engine."""

    def validate_apk_file(self, file_path: str, filename: str = "", mime_type: str = "") -> APKValidationResult:
        """Validates an APK file on disk."""
        start_time = time.time()
        errors: List[str] = []
        warnings: List[str] = []
        error_code = ""

        ext = os.path.splitext(filename or file_path)[1].lower()

        # 1. Extension Check
        if ext in UNSUPPORTED_VARIANTS:
            return APKValidationResult(
                valid=False,
                errors=[f"APK variant '{ext}' is not supported yet."],
                error_code=ApkErrorCode.UNSUPPORTED_APK_VARIANT,
                validation_time_ms=int((time.time() - start_time) * 1000),
            )

        if ext not in ALLOWED_EXTENSIONS:
            return APKValidationResult(
                valid=False,
                errors=[f"Invalid file extension '{ext}'. Only .apk files are supported."],
                error_code=ApkErrorCode.INVALID_APK,
                validation_time_ms=int((time.time() - start_time) * 1000),
            )

        # 2. File Exists & Size Check
        if not os.path.exists(file_path):
            return APKValidationResult(
                valid=False,
                errors=["APK file does not exist on target storage path."],
                error_code=ApkErrorCode.INVALID_APK,
                validation_time_ms=int((time.time() - start_time) * 1000),
            )

        file_size = os.path.getsize(file_path)
        if file_size == 0:
            return APKValidationResult(
                valid=False,
                errors=["APK file is empty (0 bytes)."],
                error_code=ApkErrorCode.INVALID_APK,
                validation_time_ms=int((time.time() - start_time) * 1000),
            )

        if file_size > MAX_APK_SIZE_BYTES:
            return APKValidationResult(
                valid=False,
                errors=[f"APK file size ({file_size / (1024*1024):.1f} MB) exceeds maximum allowed size of 100 MB."],
                error_code=ApkErrorCode.APK_TOO_LARGE,
                apk_size=file_size,
                validation_time_ms=int((time.time() - start_time) * 1000),
            )

        # 3. MIME Validation
        effective_mime = mime_type.lower() if mime_type else "application/vnd.android.package-archive"
        if effective_mime not in ALLOWED_MIMES:
            return APKValidationResult(
                valid=False,
                errors=[f"Invalid MIME type '{effective_mime}'. Expected application/vnd.android.package-archive or application/zip."],
                error_code=ApkErrorCode.INVALID_MIME,
                apk_size=file_size,
                validation_time_ms=int((time.time() - start_time) * 1000),
            )

        # 4. Streaming SHA-256
        sha256_hash = self._compute_sha256(file_path)

        # 5. ZIP Integrity, Path Traversal, CRC, and ZIP Bomb Inspection
        try:

            if not zipfile.is_zipfile(file_path):
                return APKValidationResult(
                    valid=False,
                    errors=["File is not a valid ZIP archive structure."],
                    error_code=ApkErrorCode.CORRUPTED_ARCHIVE,
                    apk_size=file_size,
                    sha256=sha256_hash,
                    validation_time_ms=int((time.time() - start_time) * 1000),
                )

            with zipfile.ZipFile(file_path, "r") as zf:
                infolist = zf.infolist()
                entry_count = len(infolist)

                if entry_count == 0:
                    return APKValidationResult(
                        valid=False,
                        errors=["APK ZIP archive contains zero entries."],
                        error_code=ApkErrorCode.CORRUPTED_ARCHIVE,
                        apk_size=file_size,
                        sha256=sha256_hash,
                        validation_time_ms=int((time.time() - start_time) * 1000),
                    )

                if entry_count > MAX_ARCHIVE_ENTRIES:
                    return APKValidationResult(
                        valid=False,
                        errors=[f"APK contains excessive entries ({entry_count} > {MAX_ARCHIVE_ENTRIES}). Potential ZIP bomb."],
                        error_code=ApkErrorCode.ZIP_BOMB_DETECTED,
                        apk_size=file_size,
                        sha256=sha256_hash,
                        archive_entries=entry_count,
                        validation_time_ms=int((time.time() - start_time) * 1000),
                    )

                seen_names = set()
                total_compressed = 0
                total_uncompressed = 0

                for info in infolist:
                    name = info.filename

                    # Path Traversal Check
                    if ".." in name or name.startswith("/") or name.startswith("\\") or ":" in name:
                        return APKValidationResult(
                            valid=False,
                            errors=[f"Malicious path traversal sequence detected in entry '{name}'."],
                            error_code=ApkErrorCode.PATH_TRAVERSAL_DETECTED,
                            apk_size=file_size,
                            sha256=sha256_hash,
                            archive_entries=entry_count,
                            validation_time_ms=int((time.time() - start_time) * 1000),
                        )

                    # Duplicate Entry Check
                    if name in seen_names:
                        return APKValidationResult(
                            valid=False,
                            errors=[f"Duplicate entry filename detected in ZIP archive: '{name}'."],
                            error_code=ApkErrorCode.MALFORMED_ZIP,
                            apk_size=file_size,
                            sha256=sha256_hash,
                            archive_entries=entry_count,
                            validation_time_ms=int((time.time() - start_time) * 1000),
                        )
                    seen_names.add(name)

                    # ZIP Bomb Accumulation
                    total_compressed += info.compress_size
                    total_uncompressed += info.file_size

                    # Nesting Safeguard (nested apk/zip/jar outside assets/lib)
                    lower_name = name.lower()
                    if lower_name.endswith((".apk", ".zip", ".jar")):
                        if not (lower_name.startswith("assets/") or lower_name.startswith("lib/")):
                            warnings.append(f"Nested archive found outside assets/lib directory: '{name}'.")

                # Compression ratio check
                if total_compressed > 0:
                    ratio = total_uncompressed / float(total_compressed)
                    if ratio > MAX_ZIP_COMPRESSION_RATIO:
                        return APKValidationResult(
                            valid=False,
                            errors=[f"ZIP bomb detected: compression ratio ({ratio:.1f}:1) exceeds threshold ({MAX_ZIP_COMPRESSION_RATIO:.0f}:1)."],
                            error_code=ApkErrorCode.ZIP_BOMB_DETECTED,
                            apk_size=file_size,
                            sha256=sha256_hash,
                            archive_entries=entry_count,
                            validation_time_ms=int((time.time() - start_time) * 1000),
                        )

                # Test archive CRC integrity
                corrupt_file = zf.testzip()
                if corrupt_file is not None:
                    return APKValidationResult(
                        valid=False,
                        errors=[f"CRC-32 checksum mismatch in entry '{corrupt_file}'."],
                        error_code=ApkErrorCode.CRC_FAILURE,
                        apk_size=file_size,
                        sha256=sha256_hash,
                        archive_entries=entry_count,
                        validation_time_ms=int((time.time() - start_time) * 1000),
                    )

        except zipfile.BadZipFile:
            return APKValidationResult(
                valid=False,
                errors=["Malformed ZIP archive or unreadable header structure."],
                error_code=ApkErrorCode.MALFORMED_ZIP,
                apk_size=file_size,
                sha256=sha256_hash,
                validation_time_ms=int((time.time() - start_time) * 1000),
            )
        except Exception as e:
            return APKValidationResult(
                valid=False,
                errors=[f"Unexpected failure during APK archive inspection: {str(e)}"],
                error_code=ApkErrorCode.UNEXPECTED_FAILURE,
                apk_size=file_size,
                sha256=sha256_hash,
                validation_time_ms=int((time.time() - start_time) * 1000),
            )

        duration_ms = int((time.time() - start_time) * 1000)
        return APKValidationResult(
            valid=True,
            errors=[],
            warnings=warnings,
            apk_size=file_size,
            sha256=sha256_hash,
            mime_type=effective_mime,
            archive_entries=entry_count,
            validation_time_ms=duration_ms,
        )

    def _compute_sha256(self, file_path: str) -> str:
        """Computes SHA-256 digest in 64KB streaming chunks to preserve memory."""
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()
