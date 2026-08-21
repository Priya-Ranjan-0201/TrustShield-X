"""APK Workspace Manager Engine (Phase 3.7 Part 1A.4).

Orchestrates isolated workspace creation at workspace/apk/{scan_id}/, safe archive extraction,
file inventory generation, manifest.json writing, and workspace cleanup lifecycle.
"""

import os
import json
import uuid
import shutil
import time
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List
from app.services.apk_extractor import APKExtractor, APKExtractionResult
from app.services.apk_inventory_builder import APKInventoryBuilder, WorkspaceInventory
from app.services.file_hash_service import FileHashService
from app.services.file_classifier import FileCategory


@dataclass
class APKWorkspaceResult:
    workspace_id: str
    scan_id: str
    workspace_path: str
    apk_sha256: str
    extraction_result: APKExtractionResult
    inventory: WorkspaceInventory
    manifest_dict: Dict[str, Any]
    status: str = "READY_FOR_STATIC_ANALYSIS"
    total_time_ms: int = 0
    errors: List[str] = field(default_factory=list)


class APKWorkspaceManager:
    """Manages isolated workspace allocation, extraction, manifest creation, and cleanup."""

    BASE_WORKSPACE_DIR = os.path.join("workspace", "apk")

    def __init__(self, base_dir: Optional[str] = None):
        self.base_workspace_dir = base_dir or self.BASE_WORKSPACE_DIR
        self.extractor = APKExtractor()
        self.inventory_builder = APKInventoryBuilder()
        self.hash_service = FileHashService()

    def create_workspace(
        self,
        scan_id: uuid.UUID,
        apk_file_path: str,
        package_name: Optional[str] = None,
        version_name: Optional[str] = None,
    ) -> APKWorkspaceResult:
        start_time = time.time()
        workspace_id = str(uuid.uuid4())
        scan_id_str = str(scan_id)
        target_workspace_path = os.path.join(self.base_workspace_dir, scan_id_str)

        if not os.path.exists(apk_file_path):
            return APKWorkspaceResult(
                workspace_id=workspace_id,
                scan_id=scan_id_str,
                workspace_path=target_workspace_path,
                apk_sha256="",
                extraction_result=APKExtractionResult(errors=[f"APK file path not found: {apk_file_path}"]),
                inventory=WorkspaceInventory(),
                manifest_dict={},
                status="FAILED",
                errors=[f"APK file path not found: {apk_file_path}"],
            )

        # 1. Compute original APK SHA256
        apk_hashes = self.hash_service.compute_file_hashes(apk_file_path)

        # 2. Safely extract APK
        extraction_res = self.extractor.extract_apk(apk_file_path, target_workspace_path)
        if extraction_res.errors:
            return APKWorkspaceResult(
                workspace_id=workspace_id,
                scan_id=scan_id_str,
                workspace_path=target_workspace_path,
                apk_sha256=apk_hashes.sha256,
                extraction_result=extraction_res,
                inventory=WorkspaceInventory(),
                manifest_dict={},
                status="FAILED",
                errors=extraction_res.errors,
            )

        # 3. Build Inventory & Calculate Entropy
        inventory = self.inventory_builder.build_inventory(target_workspace_path)

        # 4. Generate manifest.json
        manifest_present = any(e.file_name.lower() == "androidmanifest.xml" for e in inventory.entries)
        dex_count = inventory.categories_summary.get(FileCategory.DEX.value, 0)
        lib_count = inventory.categories_summary.get(FileCategory.NATIVE_LIBRARY.value, 0)
        cert_count = inventory.categories_summary.get(FileCategory.CERTIFICATE.value, 0)

        manifest_dict = {
            "scan_id": scan_id_str,
            "workspace_id": workspace_id,
            "apk_sha256": apk_hashes.sha256,
            "package_name": package_name or "unknown.package",
            "version_name": version_name or "1.0",
            "extraction_time_ms": extraction_res.extraction_time_ms,
            "total_files": inventory.total_files,
            "total_directories": inventory.total_directories,
            "dex_count": dex_count,
            "native_library_count": lib_count,
            "certificate_count": cert_count,
            "manifest_present": manifest_present,
            "extraction_status": "SUCCESS",
            "processing_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "truthshield_version": "v1.0-Phase3.7",
        }

        manifest_file_path = os.path.join(target_workspace_path, "manifest.json")
        with open(manifest_file_path, "w", encoding="utf-8") as f:
            json.dump(manifest_dict, f, indent=2)

        total_time_ms = int((time.time() - start_time) * 1000)

        return APKWorkspaceResult(
            workspace_id=workspace_id,
            scan_id=scan_id_str,
            workspace_path=target_workspace_path,
            apk_sha256=apk_hashes.sha256,
            extraction_result=extraction_res,
            inventory=inventory,
            manifest_dict=manifest_dict,
            status="READY_FOR_STATIC_ANALYSIS",
            total_time_ms=total_time_ms,
        )

    def cleanup_workspace(self, workspace_path: str, force: bool = False) -> bool:
        keep_debug = os.getenv("DEBUG_KEEP_WORKSPACE", "false").lower() in ("true", "1")
        if keep_debug and not force:
            return False

        if os.path.exists(workspace_path):
            shutil.rmtree(workspace_path, ignore_errors=True)
            return True
        return False
