"""Structured Logger for AI Android APK Security Engine (Phase 3.7 Part 1A).

Logs JSON events for upload, validation, unpacking, and storage events.
Never logs binary payloads or secrets.
"""

import logging
import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional

logger = logging.getLogger("truthshield.apk")


class APKLogger:
    """Structured JSON Logger for APK Pipeline Events."""

    @staticmethod
    def _log_event(event_name: str, level: str, data: Dict[str, Any], trace_id: Optional[str] = None):
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event_name,
            "level": level.upper(),
            "module": "apk-security-ai",
            "trace_id": trace_id,
            "data": data,
        }
        msg = json.dumps(payload)
        if level.upper() == "ERROR":
            logger.error(msg)
        elif level.upper() == "WARNING":
            logger.warning(msg)
        else:
            logger.info(msg)

    @classmethod
    def log_upload_start(cls, filename: str, file_size: int, trace_id: Optional[str] = None):
        cls._log_event(
            "APK_UPLOAD_STARTED",
            "INFO",
            {"filename": filename, "file_size_bytes": file_size},
            trace_id=trace_id,
        )

    @classmethod
    def log_validation_result(cls, valid: bool, apk_size: int, sha256: str, duration_ms: int, errors: list, trace_id: Optional[str] = None):
        level = "INFO" if valid else "WARNING"
        cls._log_event(
            "APK_VALIDATION_COMPLETED",
            level,
            {
                "valid": valid,
                "apk_size_bytes": apk_size,
                "sha256": sha256,
                "validation_time_ms": duration_ms,
                "errors_count": len(errors),
                "errors": errors,
            },
            trace_id=trace_id,
        )

    @classmethod
    def log_storage_success(cls, storage_path: str, sha256: str, trace_id: Optional[str] = None):
        cls._log_event(
            "APK_STORAGE_SUCCESS",
            "INFO",
            {"storage_path": storage_path, "sha256": sha256},
            trace_id=trace_id,
        )

    @classmethod
    def log_error(cls, error_code: str, message: str, trace_id: Optional[str] = None):
        cls._log_event(
            "APK_ERROR",
            "ERROR",
            {"error_code": error_code, "message": message},
            trace_id=trace_id,
        )
