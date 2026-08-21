"""Unit tests for Async Workspace Repository (Phase 3.7 Part 1A.4)."""

import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.repositories.workspace_repository import WorkspaceRepository
from app.services.apk_workspace_manager import APKWorkspaceResult, APKExtractionResult, WorkspaceInventory
from app.services.apk_inventory_builder import FileInventoryEntry


@pytest.mark.asyncio
async def test_workspace_repository_save_and_retrieve():
    db_mock = AsyncMock()
    repo = WorkspaceRepository(db_mock)
    scan_id = uuid.uuid4()

    ws_res = APKWorkspaceResult(
        workspace_id=str(uuid.uuid4()),
        scan_id=str(scan_id),
        workspace_path=f"workspace/apk/{scan_id}",
        apk_sha256="a" * 64,
        extraction_result=APKExtractionResult(extracted_files_count=1),
        inventory=WorkspaceInventory(
            total_files=1,
            total_directories=0,
            categories_summary={"DEX": 1},
            entries=[
                FileInventoryEntry(
                    relative_path="classes.dex",
                    file_name="classes.dex",
                    extension=".dex",
                    mime_type="application/octet-stream",
                    size=100,
                    compressed_size=100,
                    sha256="b" * 64,
                    sha1="c" * 40,
                    md5="d" * 32,
                    crc32="12345678",
                    entropy=4.5,
                    is_executable=True,
                    is_archive=False,
                    is_binary=True,
                    created_timestamp=1000.0,
                    modified_timestamp=1000.0,
                    compression_ratio=1.0,
                    category="DEX",
                )
            ],
        ),
        manifest_dict={"status": "SUCCESS"},
    )

    root_model = await repo.save_full_workspace(scan_id, ws_res)
    assert root_model.scan_id == scan_id
    assert db_mock.add.called
    assert db_mock.commit.called
