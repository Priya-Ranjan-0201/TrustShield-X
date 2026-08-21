from enum import Enum
from fastapi import HTTPException, status


class ScanStatus(str, Enum):
    UPLOADED = "UPLOADED"
    VALIDATING = "VALIDATING"
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    ANALYZING = "ANALYZING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


# Valid status transitions map
VALID_TRANSITIONS: dict[ScanStatus, set[ScanStatus]] = {
    ScanStatus.UPLOADED: {ScanStatus.VALIDATING, ScanStatus.QUEUED, ScanStatus.FAILED, ScanStatus.CANCELLED},
    ScanStatus.VALIDATING: {ScanStatus.QUEUED, ScanStatus.FAILED, ScanStatus.CANCELLED},
    ScanStatus.QUEUED: {ScanStatus.PROCESSING, ScanStatus.FAILED, ScanStatus.CANCELLED},
    ScanStatus.PROCESSING: {ScanStatus.ANALYZING, ScanStatus.COMPLETED, ScanStatus.FAILED, ScanStatus.CANCELLED},
    ScanStatus.ANALYZING: {ScanStatus.COMPLETED, ScanStatus.FAILED, ScanStatus.CANCELLED},
    ScanStatus.COMPLETED: set(),
    ScanStatus.FAILED: set(),
    ScanStatus.CANCELLED: set(),
}


def validate_status_transition(current_status: str, target_status: str) -> bool:
    try:
        curr = ScanStatus(current_status)
        target = ScanStatus(target_status)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid scan status value: current='{current_status}', target='{target_status}'.",
        )

    if target not in VALID_TRANSITIONS[curr]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Illegal scan status transition from '{current_status}' to '{target_status}'.",
        )

    return True
