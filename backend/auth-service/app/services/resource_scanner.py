"""Resource Inventory Scanner for AI Android APK Security Engine (Phase 3.7 Part 1A Message 2).

Categorizes archive resources across assets/, res/, META-INF/, kotlin/, lib/, and unknown/ folders.
Calculates size distribution statistics without decoding raw binary assets.
"""

import os
from typing import List, Dict, Any, Tuple
from app.schemas.apk_models import ResourceInventory

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
XML_EXTENSIONS = {".xml", ".arsc"}
FONT_EXTENSIONS = {".ttf", ".otf", ".woff", ".woff2"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".aac", ".m4a"}
VIDEO_EXTENSIONS = {".mp4", ".3gp", ".webm", ".mkv"}
TEXT_EXTENSIONS = {".json", ".txt", ".properties", ".html", ".css", ".js"}
BINARY_EXTENSIONS = {".so", ".dex", ".bin", ".dat"}


class ResourceScanner:
    """Production Resource Asset Inventory Scanner."""

    def scan_archive_resources(self, archive_entries: List[Tuple[str, int, int]]) -> ResourceInventory:
        """Scans list of (filename, compressed_size, uncompressed_size) tuples from ZIP archive."""
        if not archive_entries:
            return ResourceInventory()

        res_cnt = 0
        asset_cnt = 0
        xml_cnt = 0
        img_cnt = 0
        font_cnt = 0
        audio_cnt = 0
        video_cnt = 0
        binary_cnt = 0

        tot_compressed = 0
        tot_uncompressed = 0

        largest_name = None
        largest_size = 0

        for filename, c_size, u_size in archive_entries:
            lower_name = filename.lower()
            ext = os.path.splitext(lower_name)[1]

            tot_compressed += c_size
            tot_uncompressed += u_size

            if u_size > largest_size:
                largest_size = u_size
                largest_name = filename

            if lower_name.startswith("assets/"):
                asset_cnt += 1

            if lower_name.startswith("res/") or lower_name.startswith("assets/"):
                res_cnt += 1

            if ext in IMAGE_EXTENSIONS:
                img_cnt += 1
            elif ext in XML_EXTENSIONS:
                xml_cnt += 1
            elif ext in FONT_EXTENSIONS:
                font_cnt += 1
            elif ext in AUDIO_EXTENSIONS:
                audio_cnt += 1
            elif ext in VIDEO_EXTENSIONS:
                video_cnt += 1
            elif ext in BINARY_EXTENSIONS:
                binary_cnt += 1

        tot_entries = len(archive_entries)
        avg_size = round(tot_uncompressed / tot_entries, 2) if tot_entries > 0 else 0.0

        return ResourceInventory(
            resource_count=res_cnt,
            asset_count=asset_cnt,
            xml_count=xml_cnt,
            image_count=img_cnt,
            font_count=font_cnt,
            audio_count=audio_cnt,
            video_count=video_cnt,
            binary_count=binary_cnt,
            largest_resource_name=largest_name,
            largest_resource_bytes=largest_size,
            average_resource_size_bytes=avg_size,
            total_compressed_bytes=tot_compressed,
            total_uncompressed_bytes=tot_uncompressed,
        )
