import os
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Request, UploadFile, File, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.repositories.scan_repository import ScanRepository
from app.repositories.event_repository import EventRepository
from app.repositories.result_repository import ResultRepository
from app.services.storage_service import LocalStorageProvider
from app.services.scan_orchestrator import DefaultModuleRouter, ScanOrchestrator
from app.core.scan_lifecycle import ScanStatus
from app.schemas.envelope import ResponseEnvelope, ResponseMeta

router = APIRouter()
storage_provider = LocalStorageProvider()
module_router = DefaultModuleRouter()


@router.post("", response_model=ResponseEnvelope[dict])
@router.post("/upload", response_model=ResponseEnvelope[dict])
async def create_and_execute_scan(
    request: Request,
    scan_type: str = Form(...),
    target_input: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    scan_repo = ScanRepository(db)
    event_repo = EventRepository(db)

    file_path = None
    file_size = None
    sha256_checksum = None
    mime_type = None
    target_str = target_input or "Uploaded Artifact"

    if file:
        # Use Storage Abstraction Service
        stored_filename, full_path, sha256_checksum, mime_type, file_size = (
            await storage_provider.save_file(user_id=current_user.id, file=file)
        )
        file_path = full_path
        target_str = file.filename or target_str

        # Duplicate SHA-256 Check
        if sha256_checksum:
            from sqlalchemy import select
            from app.models.scan_history import ScanHistory
            existing_stmt = select(ScanHistory).where(
                ScanHistory.user_id == current_user.id,
                ScanHistory.sha256_checksum == sha256_checksum,
            )
            existing_res = await db.execute(existing_stmt)
            existing_scan = existing_res.scalar_one_or_none()
            if existing_scan:
                return ResponseEnvelope[dict](
                    success=True,
                    message="Duplicate artifact upload detected. Existing scan record returned.",
                    data={
                        "id": str(existing_scan.id),
                        "target": existing_scan.target,
                        "scan_type": existing_scan.scan_type,
                        "trust_score": existing_scan.trust_score,
                        "status": existing_scan.status,
                        "scanned_at": existing_scan.scanned_at.isoformat(),
                        "summary": existing_scan.summary,
                        "sha256_checksum": existing_scan.sha256_checksum,
                        "module_used": existing_scan.module_used,
                    },
                    meta=ResponseMeta(
                        traceId=getattr(request.state, "trace_id", "trace-id-default"),
                        version="v1",
                    ),
                )

    # Resolve target AI module
    target_module = module_router.resolve_target_module(scan_type, mime_type)

    # Create initial scan record in database with UPLOADED status lifecycle
    scan_record = await scan_repo.create_scan_record(
        user_id=current_user.id,
        target=target_str,
        scan_type=scan_type,
        trust_score=None,
        status=ScanStatus.UPLOADED,
        summary=f"Artifact received and routed to module '{target_module}'.",
        file_path=file_path,
        file_size_bytes=file_size,
        sha256_checksum=sha256_checksum,
        mime_type=mime_type,
        module_used=target_module,
    )

    # Log SCAN_CREATED event
    await event_repo.log_event(
        scan_id=scan_record.id,
        event_type="SCAN_CREATED",
        description=f"Scan record initialized for target '{target_str}'.",
        event_data_json={"scan_type": scan_type, "mime_type": mime_type},
    )

    # Execute Orchestration Pipeline
    orchestrator = ScanOrchestrator(db)
    await orchestrator.execute_pipeline(scan_record.id)

    # Refetch scan record and result findings
    await db.refresh(scan_record)
    result_repo = ResultRepository(db)
    scan_result = await result_repo.get_by_scan_id(scan_record.id)

    return ResponseEnvelope[dict](
        success=True,
        message="Scan executed successfully.",
        data={
            "id": str(scan_record.id),
            "target": scan_record.target,
            "scan_type": scan_record.scan_type,
            "trust_score": scan_record.trust_score,
            "risk_score": scan_record.risk_score,
            "confidence_score": scan_record.confidence_score,
            "status": scan_record.status,
            "scanned_at": scan_record.scanned_at.isoformat(),
            "summary": scan_record.summary,
            "sha256_checksum": scan_record.sha256_checksum,
            "module_used": scan_record.module_used,
            "findings": scan_result.findings_json if scan_result else {},
        },
        meta=ResponseMeta(
            traceId=getattr(request.state, "trace_id", "trace-id-default"),
            version="v1",
        ),
    )



@router.get("/history", response_model=ResponseEnvelope[list[dict]])
async def get_scan_history(
    request: Request,
    scan_type: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    scan_repo = ScanRepository(db)
    scans = await scan_repo.get_user_scans(
        user_id=current_user.id,
        scan_type=scan_type,
        search_query=search,
        limit=50,
    )

    data = [
        {
            "id": str(s.id),
            "target": s.target,
            "scan_type": s.scan_type,
            "trust_score": s.trust_score if s.trust_score is not None else 0,
            "status": s.status,
            "scanned_at": s.scanned_at.isoformat(),
            "summary": s.summary or "Inspection complete.",
            "sha256_checksum": s.sha256_checksum,
            "module_used": s.module_used,
        }
        for s in scans
    ]

    return ResponseEnvelope[list[dict]](
        success=True,
        message="Scan history retrieved.",
        data=data,
        meta=ResponseMeta(
            traceId=getattr(request.state, "trace_id", "trace-id-default"),
            version="v1",
        ),
    )


@router.get("/events/{scan_id}", response_model=ResponseEnvelope[list[dict]])
async def get_scan_events(
    scan_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    event_repo = EventRepository(db)
    events = await event_repo.get_scan_events(scan_id)

    data = [
        {
            "id": str(e.id),
            "scan_id": str(e.scan_id),
            "event_type": e.event_type,
            "description": e.description,
            "event_data": e.event_data_json,
            "created_at": e.created_at.isoformat(),
        }
        for e in events
    ]

    return ResponseEnvelope[list[dict]](
        success=True,
        message="Scan events retrieved.",
        data=data,
        meta=ResponseMeta(
            traceId=getattr(request.state, "trace_id", "trace-id-default"),
            version="v1",
        ),
    )


@router.get("/{scan_id}", response_model=ResponseEnvelope[dict])
async def get_scan_details(
    scan_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from sqlalchemy import select
    from app.models.scan_history import ScanHistory
    stmt = select(ScanHistory).where(ScanHistory.id == scan_id, ScanHistory.user_id == current_user.id)
    res = await db.execute(stmt)
    scan = res.scalar_one_or_none()

    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan record not found.",
        )

    result_repo = ResultRepository(db)
    scan_result = await result_repo.get_by_scan_id(scan_id)

    data = {
        "id": str(scan.id),
        "target": scan.target,
        "scan_type": scan.scan_type,
        "trust_score": scan.trust_score,
        "risk_score": scan.risk_score,
        "confidence_score": scan.confidence_score,
        "status": scan.status,
        "summary": scan.summary,
        "file_size_bytes": scan.file_size_bytes,
        "sha256_checksum": scan.sha256_checksum,
        "mime_type": scan.mime_type,
        "module_used": scan.module_used,
        "scanned_at": scan.scanned_at.isoformat(),
        "findings": scan_result.findings_json if scan_result else {},
    }

    return ResponseEnvelope[dict](
        success=True,
        message="Scan record retrieved.",
        data=data,
        meta=ResponseMeta(
            traceId=getattr(request.state, "trace_id", "trace-id-default"),
            version="v1",
        ),
    )


@router.delete("/{scan_id}", response_model=ResponseEnvelope[dict])
async def delete_scan(
    scan_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from sqlalchemy import select, delete
    from app.models.scan_history import ScanHistory
    stmt = select(ScanHistory).where(ScanHistory.id == scan_id, ScanHistory.user_id == current_user.id)
    res = await db.execute(stmt)
    scan = res.scalar_one_or_none()

    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan record not found.",
        )

    # Delete local file artifact if exists
    if scan.file_path and os.path.exists(scan.file_path):
        try:
            os.remove(scan.file_path)
        except OSError:
            pass

    del_stmt = delete(ScanHistory).where(ScanHistory.id == scan_id)
    await db.execute(del_stmt)
    await db.commit()

    return ResponseEnvelope[dict](
        success=True,
        message="Scan record and stored artifact deleted.",
        data={"id": str(scan_id), "deleted": True},
        meta=ResponseMeta(
            traceId=getattr(request.state, "trace_id", "trace-id-default"),
            version="v1",
        ),
    )
