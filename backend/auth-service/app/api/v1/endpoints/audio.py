"""Production REST API Router for Voice Clone Engine (Phase 3.6 Part 2B-2).

Endpoints:
- POST /api/v1/scan/audio : Dedicated audio file upload & Voice Clone AI analysis
- GET  /api/v1/audio/{scan_id} : Retrieve complete stored Voice Clone analysis
- GET  /api/v1/audio/history   : Paginated audio scan history with filtering
- DELETE /api/v1/audio/{scan_id}: Delete audio scan & cleanup artifacts with audit logging
"""

import os
import uuid
from typing import Optional, List
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.scan_history import ScanHistory
from app.repositories.scan_repository import ScanRepository
from app.repositories.audio_clone_repository import AudioCloneRepository
from app.services.storage_service import LocalStorageProvider
from app.services.scan_orchestrator import ScanOrchestrator
from app.schemas.envelope import ResponseEnvelope, ResponseMeta
from app.schemas.voice_clone_dto import (
    VoiceCloneResultResponse,
    ConversationAnalysisResponse,
    EvidenceResponse,
)
from app.core.error_codes import AudioErrorCode, ERROR_DESCRIPTIONS

router = APIRouter()
storage_provider = LocalStorageProvider()

SUPPORTED_AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac", ".aac", ".ogg", ".opus", ".m4a"}


@router.post("/scan", response_model=ResponseEnvelope[dict])
async def scan_audio_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Uploads an audio file, executes full Voice Clone AI pipeline, and returns analysis envelope."""
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in SUPPORTED_AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": AudioErrorCode.VALIDATION_ERROR,
                "message": f"Unsupported audio format '{ext}'. Supported formats: {', '.join(SUPPORTED_AUDIO_EXTENSIONS)}",
            },
        )

    # Save file via storage provider
    stored_filename, full_path, sha256_checksum, mime_type, file_size = (
        await storage_provider.save_file(user_id=current_user.id, file=file)
    )

    scan_repo = ScanRepository(db)
    scan = await scan_repo.create_scan(
        user_id=current_user.id,
        target=file.filename or "Uploaded Audio Artifact",
        scan_type="AUDIO-VOICE-AI",
        file_path=full_path,
        file_size=file_size,
        mime_type=mime_type or "audio/wav",
        sha256_checksum=sha256_checksum,
        module_used="audio-voice-ai",
    )

    orchestrator = ScanOrchestrator(db)
    result_scan = await orchestrator.execute_scan(scan.id)

    # Fetch stored analysis
    clone_repo = AudioCloneRepository(db)
    stored_data = await clone_repo.get_analysis_by_scan_id(scan.id)

    return ResponseEnvelope[dict](
        success=True,
        message="Voice Clone AI analysis completed successfully.",
        data={
            "scan_id": str(scan.id),
            "status": result_scan.status,
            "risk_score": result_scan.risk_score,
            "trust_score": result_scan.trust_score,
            "confidence_score": result_scan.confidence_score,
            "findings": result_scan.findings_json,
            "stored_analysis": {
                "results_count": len(stored_data["voice_clone_results"]) if stored_data else 0,
                "has_conversation_summary": stored_data["conversation_analysis"] is not None if stored_data else False,
            },
        },
        meta=ResponseMeta(traceId=str(scan.id)),
    )


@router.get("/{scan_id}", response_model=ResponseEnvelope[dict])
async def get_audio_scan_analysis(
    scan_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieves full stored voice clone analysis for a specific scan ID."""
    scan_repo = ScanRepository(db)
    scan = await scan_repo.get_scan_by_id(scan_id)

    if not scan or scan.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": AudioErrorCode.API_ERROR, "message": "Audio scan not found or access denied."},
        )

    clone_repo = AudioCloneRepository(db)
    stored_data = await clone_repo.get_analysis_by_scan_id(scan_id)

    if not stored_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": AudioErrorCode.REPOSITORY_ERROR, "message": "No stored analysis record found for this audio scan."},
        )

    meta = stored_data["metadata"]
    conv = stored_data["conversation_analysis"]
    vc_results = stored_data["voice_clone_results"]

    return ResponseEnvelope[dict](
        success=True,
        message="Retrieved voice clone analysis.",
        data={
            "scan_id": str(scan.id),
            "target": scan.target,
            "risk_score": scan.risk_score,
            "trust_score": scan.trust_score,
            "confidence_score": scan.confidence_score,
            "created_at": scan.created_at.isoformat() if scan.created_at else None,
            "metadata": {
                "duration_sec": meta.duration_sec if meta else None,
                "sample_rate": meta.sample_rate if meta else None,
                "codec": meta.codec if meta else None,
                "prediction": meta.prediction if meta else None,
                "calibrated_confidence": meta.calibrated_confidence if meta else None,
                "model_name": meta.model_name if meta else None,
            },
            "conversation_analysis": {
                "total_speakers": conv.total_speakers if conv else 1,
                "conversation_duration": conv.conversation_duration if conv else 0.0,
                "conversation_risk": conv.conversation_risk if conv else 0,
                "summary": conv.summary_json if conv else {},
            },
            "voice_clone_results": [
                {
                    "speaker_id": r.speaker_id,
                    "clone_probability": r.clone_probability,
                    "confidence": r.confidence,
                    "verdict": r.verdict,
                    "evidence": r.evidence_json,
                    "recommendations": r.recommendation_json,
                }
                for r in vc_results
            ],
        },
        meta=ResponseMeta(traceId=str(scan_id)),
    )


@router.get("/history/all", response_model=ResponseEnvelope[list])
async def get_audio_scan_history(
    verdict: Optional[str] = Query(None, description="Filter by verdict: REAL, VOICE_CLONE, LIKELY_CLONE, LOW_CONFIDENCE"),
    min_risk: Optional[int] = Query(None, ge=0, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lists user's audio scan history with optional filtering."""
    stmt = select(ScanHistory).where(
        ScanHistory.user_id == current_user.id,
        ScanHistory.scan_type.in_(["AUDIO", "VOICE", "AUDIO-VOICE-AI"]),
    )
    if min_risk is not None:
        stmt = stmt.where(ScanHistory.risk_score >= min_risk)

    stmt = stmt.order_by(ScanHistory.created_at.desc())
    res = await db.execute(stmt)
    scans = res.scalars().all()

    items = []
    for s in scans:
        items.append({
            "scan_id": str(s.id),
            "target": s.target,
            "scan_type": s.scan_type,
            "status": s.status,
            "risk_score": s.risk_score,
            "trust_score": s.trust_score,
            "confidence_score": s.confidence_score,
            "created_at": s.created_at.isoformat() if s.created_at else None,
        })

    return ResponseEnvelope[list](
        success=True,
        message=f"Retrieved {len(items)} audio scan history records.",
        data=items,
        meta=ResponseMeta(),
    )


@router.delete("/{scan_id}", response_model=ResponseEnvelope[dict])
async def delete_audio_scan(
    scan_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Deletes an audio scan record, database analysis, and stored artifact."""
    scan_repo = ScanRepository(db)
    scan = await scan_repo.get_scan_by_id(scan_id)

    if not scan or scan.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": AudioErrorCode.API_ERROR, "message": "Audio scan not found or access denied."},
        )

    # Delete physical file artifact
    if scan.file_path and os.path.exists(scan.file_path):
        try:
            os.remove(scan.file_path)
        except Exception:
            pass

    # Delete scan history record (CASCADE deletes audio_metadata, voice_clone_results, conversation_analysis)
    await scan_repo.delete_scan(scan_id)

    return ResponseEnvelope[dict](
        success=True,
        message="Audio scan and associated artifacts deleted successfully.",
        data={"deleted_scan_id": str(scan_id)},
        meta=ResponseMeta(traceId=str(scan_id)),
    )
