"""Production APK Binary Inventory & File Intelligence Engine (Phase 3.7 Part 1A.12).

Enumerates, indexes, classifies, fingerprints, and stores metadata for every file inside an APK.
Zero malware scoring, threat verdicts, or security alerts.
"""

import os
import math
import hashlib
import time
import zipfile
from typing import List, Dict, Any, Optional, Tuple, Set
from app.schemas.apk_binary_inventory_models import (
    FileCategoryEnum,
    BinaryHashDTO,
    BinaryFileEntryDTO,
    BinaryStatisticsDTO,
    APKBinaryInventoryResultDTO,
)


class APKBinaryInventoryService:
    """Master APK Binary Inventory & File Intelligence Engine."""

    def compute_entropy(self, data: bytes) -> float:
        """Computes Shannon entropy (0.0 to 8.0 bits/byte)."""
        if not data:
            return 0.0
        entropy = 0.0
        length = len(data)
        freqs: Dict[int, int] = {}
        for b in data:
            freqs[b] = freqs.get(b, 0) + 1

        for count in freqs.values():
            p = count / length
            entropy -= p * math.log2(p)

        return round(entropy, 4)

    def classify_file(self, file_path: str) -> FileCategoryEnum:
        norm_path = file_path.replace("\\", "/").strip()
        lower_path = norm_path.lower()
        filename = os.path.basename(norm_path).lower()
        ext = os.path.splitext(filename)[1]

        if filename.startswith("classes") and filename.endswith(".dex"):
            return FileCategoryEnum.DEX
        if norm_path.startswith("lib/") and lower_path.endswith(".so"):
            return FileCategoryEnum.NATIVE_LIBRARY
        if norm_path.startswith("META-INF/"):
            if any(lower_path.endswith(s) for s in (".rsa", ".dsa", ".ec", ".sf")):
                return FileCategoryEnum.CERTIFICATE
            return FileCategoryEnum.META_INF
        if filename == "androidmanifest.xml":
            return FileCategoryEnum.MANIFEST

        if ext in (".tflite", ".onnx", ".pb"):
            return FileCategoryEnum.ML_MODEL
        if ext in (".png", ".webp", ".jpg", ".jpeg", ".gif", ".bmp"):
            return FileCategoryEnum.IMAGE
        if ext in (".ttf", ".otf", ".woff", ".woff2"):
            return FileCategoryEnum.FONT
        if ext in (".mp4", ".mkv", ".webm", ".3gp"):
            return FileCategoryEnum.VIDEO
        if ext in (".mp3", ".ogg", ".wav", ".aac", ".flac"):
            return FileCategoryEnum.AUDIO
        if ext in (".json",):
            return FileCategoryEnum.JSON
        if ext in (".xml",):
            return FileCategoryEnum.XML
        if ext in (".db", ".sqlite", ".sqlite3"):
            return FileCategoryEnum.SQLITE
        if ext in (".html", ".htm"):
            return FileCategoryEnum.HTML
        if ext in (".js",):
            return FileCategoryEnum.JAVASCRIPT
        if ext in (".css",):
            return FileCategoryEnum.CSS
        if ext in (".txt", ".md", ".properties"):
            return FileCategoryEnum.TEXT

        if norm_path.startswith("assets/"):
            return FileCategoryEnum.ASSET
        if norm_path.startswith("res/"):
            return FileCategoryEnum.RESOURCE

        return FileCategoryEnum.UNKNOWN_BINARY

    def generate_fingerprints(self, data: bytes, crc_val: int = 0) -> BinaryHashDTO:
        sha256 = hashlib.sha256(data).hexdigest()
        sha1 = hashlib.sha1(data).hexdigest()
        md5 = hashlib.md5(data).hexdigest()
        crc_str = f"{crc_val & 0xFFFFFFFF:08x}"
        entropy = self.compute_entropy(data)

        return BinaryHashDTO(
            sha256=sha256,
            sha1=sha1,
            md5=md5,
            crc32=crc_str,
            entropy=entropy,
            mime_type="application/octet-stream",
        )

    def analyze_zip_entries(
        self,
        zip_file_path: Optional[str] = None,
        raw_zip_bytes: Optional[bytes] = None,
    ) -> APKBinaryInventoryResultDTO:
        start_time = time.time()

        entries: List[BinaryFileEntryDTO] = []
        directories: Set[str] = set()

        stat_files = 0
        stat_size = 0
        stat_compressed = 0
        stat_dex = 0
        stat_native = 0
        stat_assets = 0
        stat_resources = 0
        stat_media = 0
        stat_config = 0
        stat_unknown = 0

        # Process ZIP archive entries passively
        try:
            if zip_file_path and os.path.exists(zip_file_path):
                zf = zipfile.ZipFile(zip_file_path, "r")
            elif raw_zip_bytes:
                import io
                zf = zipfile.ZipFile(io.BytesIO(raw_zip_bytes), "r")
            else:
                zf = None

            if zf:
                for zinfo in zf.infolist():
                    if zinfo.is_dir():
                        directories.add(zinfo.filename)
                        continue

                    fpath = zinfo.filename.replace("\\", "/")
                    fname = os.path.basename(fpath)
                    dir_name = os.path.dirname(fpath)
                    ext = os.path.splitext(fname)[1]
                    if dir_name:
                        directories.add(dir_name)

                    try:
                        content = zf.read(zinfo.filename)
                    except Exception:
                        content = b""

                    category = self.classify_file(fpath)
                    hashes = self.generate_fingerprints(content, zinfo.CRC)

                    # Counters
                    stat_files += 1
                    stat_size += zinfo.file_size
                    stat_compressed += zinfo.compress_size

                    if category == FileCategoryEnum.DEX:
                        stat_dex += 1
                    elif category == FileCategoryEnum.NATIVE_LIBRARY:
                        stat_native += 1
                    elif category == FileCategoryEnum.ASSET or fpath.startswith("assets/"):
                        stat_assets += 1
                    elif category == FileCategoryEnum.RESOURCE or fpath.startswith("res/"):
                        stat_resources += 1
                    elif category in (FileCategoryEnum.IMAGE, FileCategoryEnum.VIDEO, FileCategoryEnum.AUDIO):
                        stat_media += 1
                    elif category in (FileCategoryEnum.JSON, FileCategoryEnum.XML, FileCategoryEnum.CONFIG):
                        stat_config += 1
                    elif category == FileCategoryEnum.UNKNOWN_BINARY:
                        stat_unknown += 1

                    entries.append(
                        BinaryFileEntryDTO(
                            file_path=fpath,
                            filename=fname,
                            directory=dir_name,
                            extension=ext,
                            file_category=category,
                            uncompressed_size=zinfo.file_size,
                            compressed_size=zinfo.compress_size,
                            compression_method=zinfo.compress_type,
                            crc32=hashes.crc32,
                            zip_offset=zinfo.header_offset if hasattr(zinfo, 'header_offset') else 0,
                            hashes=hashes,
                        )
                    )
        except Exception:
            pass

        stats = BinaryStatisticsDTO(
            total_files=stat_files,
            total_directories=len(directories),
            total_size_bytes=stat_size,
            compressed_size_bytes=stat_compressed,
            dex_count=stat_dex,
            native_library_count=stat_native,
            assets_count=stat_assets,
            resources_count=stat_resources,
            media_count=stat_media,
            config_count=stat_config,
            unknown_count=stat_unknown,
        )

        parse_time_ms = int((time.time() - start_time) * 1000)

        return APKBinaryInventoryResultDTO(
            entries=entries,
            statistics=stats,
            inventory_time_ms=parse_time_ms,
        )
