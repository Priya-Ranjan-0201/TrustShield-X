"""Unit tests for Downloads & Media Storage (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import FileOperationDTO


def test_download_storage_dto():
    fop = FileOperationDTO(
        caller_method="com.bank.DownloadManager.enqueue",
        file_path="/sdcard/Download/update.apk",
        action="WRITE",
        stream_class="android.app.DownloadManager",
    )

    assert fop.stream_class == "android.app.DownloadManager"
