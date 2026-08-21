"""Secure APK Upload Pipeline for AI Android APK Security Engine (Phase 3.7 Part 1A).

Responsibilities:
- Receives uploaded APK file stream or temp file
- Allocates unique UUIDv4 target path under storage/uploads/apk/{user_id}/{uuid}/
- Executes APKValidator security pipeline
- Manages temp file lifecycle & automatic cleanup on failure
- Returns structured APKUploadResult DTO
"""

import os
import uuid
import tempfile
import shutil
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Dict, Any, Optional

from app.services.apk_validator import APKValidator, APKValidationResult
from app.services.apk_logger import APKLogger


@dataclass
class APKUploadResult:
    scan_id: str
    upload_id: str
    storage_path: str
    sha256: str
    size: int
    received_at: str
    validated: bool
    validation_result: APKValidationResult

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scan_id": self.scan_id,
            "upload_id": self.upload_id,
            "storage_path": self.storage_path,
            "sha256": self.sha256,
            "size": self.size,
            "received_at": self.received_at,
            "validated": self.validated,
            "validation_result": self.validation_result.to_dict(),
        }


class APKUploadService:
    """Production Secure APK Upload & Ingestion Pipeline."""

    def __init__(self, base_storage_dir: str = "storage/uploads/apk"):
        self.base_storage_dir = base_storage_dir
        self.validator = APKValidator()

    async def process_upload(
        self,
        user_id: uuid.UUID,
        file_bytes: bytes,
        original_filename: str,
        mime_type: str = "",
        trace_id: Optional[str] = None,
    ) -> APKUploadResult:
        """Processes an incoming APK file upload through validation & secure storage."""

        upload_id = str(uuid.uuid4())
        scan_id = str(uuid.uuid4())
        received_at = datetime.now(timezone.utc).isoformat()

        # Sanitize filename
        safe_filename = os.path.basename(original_filename or "app.apk").replace("..", "").strip()
        if not safe_filename.lower().endswith(".apk"):
            safe_filename += ".apk"

        APKLogger.log_upload_start(safe_filename, len(file_bytes), trace_id=trace_id)

        # 1. Write file to temporary directory for streaming validation
        temp_dir = tempfile.mkdtemp(prefix="tsx_apk_")
        temp_file_path = os.path.join(temp_dir, safe_filename)

        try:
            with open(temp_file_path, "wb") as f:
                f.write(file_bytes)

            # 2. Run APK Validation Engine
            val_result = self.validator.validate_apk_file(
                file_path=temp_file_path,
                filename=safe_filename,
                mime_type=mime_type,
            )

            APKLogger.log_validation_result(
                valid=val_result.valid,
                apk_size=val_result.apk_size,
                sha256=val_result.sha256,
                duration_ms=val_result.validation_time_ms,
                errors=val_result.errors,
                trace_id=trace_id,
            )

            if not val_result.valid:
                # Cleanup temp directory on validation failure
                shutil.rmtree(temp_dir, ignore_errors=True)
                return APKUploadResult(
                    scan_id=scan_id,
                    upload_id=upload_id,
                    storage_path="",
                    sha256=val_result.sha256,
                    size=len(file_bytes),
                    received_at=received_at,
                    validated=False,
                    validation_result=val_result,
                )

            # 3. Move validated file to permanent storage under storage/uploads/apk/{user_id}/{uuid}/
            target_user_dir = os.path.join(self.base_storage_dir, str(user_id), upload_id)
            os.makedirs(target_user_dir, exist_ok=True)
            target_file_path = os.path.join(target_user_dir, safe_filename)

            shutil.copy2(temp_file_path, target_file_path)
            APKLogger.log_storage_success(target_file_path, val_result.sha256, trace_id=trace_id)

            return APKUploadResult(
                scan_id=scan_id,
                upload_id=upload_id,
                storage_path=target_file_path,
                sha256=val_result.sha256,
                size=val_result.apk_size,
                received_at=received_at,
                validated=True,
                validation_result=val_result,
            )

        finally:
            # Always cleanup temp buffer
            shutil.rmtree(temp_dir, ignore_errors=True)
