"""Unit tests for APK Workspace Manager Engine (Phase 3.7 Part 1A.4)."""

import os
import uuid
import zipfile
import pytest
from app.services.apk_workspace_manager import APKWorkspaceManager


@pytest.fixture
def dummy_apk(tmp_path):
    apk_path = os.path.join(tmp_path, "dummy.apk")
    with zipfile.ZipFile(apk_path, "w") as zf:
        zf.writestr("AndroidManifest.xml", b"<manifest package='com.example.app'></manifest>")
        zf.writestr("classes.dex", b"dex\n035\x00" + b"\x00" * 40)
    return apk_path


def test_create_workspace(dummy_apk, tmp_path):
    mgr = APKWorkspaceManager(base_dir=str(tmp_path / "workspaces"))
    scan_id = uuid.uuid4()

    res = mgr.create_workspace(scan_id, dummy_apk, package_name="com.example.app")

    assert res.status == "READY_FOR_STATIC_ANALYSIS"
    assert res.inventory.total_files == 2
    assert os.path.exists(os.path.join(res.workspace_path, "manifest.json"))
    assert os.path.exists(os.path.join(res.workspace_path, "inventory.json"))

    cleaned = mgr.cleanup_workspace(res.workspace_path, force=True)
    assert cleaned is True
    assert not os.path.exists(res.workspace_path)
