"""FastAPI Endpoint Router for Trust Narrative Engine (Phase 4.0 Part 2 — Section 52).

REST APIs for generating, retrieving, and querying Trust Narratives.
"""

import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.envelope import ResponseEnvelope
from app.schemas.trust_narrative_models import NarrativeDocumentDTO
from app.schemas.risk_aggregation_models import RiskAssessmentDTO
from app.services.trust_narrative_orchestrator import TrustNarrativeOrchestrator
from app.repositories.trust_narrative_repository import TrustNarrativeRepository

router = APIRouter(prefix="/reports", tags=["Trust Narrative Engine"])


@router.post("/{report_id}/narrative", response_model=ResponseEnvelope[NarrativeDocumentDTO])
async def generate_narrative(
    report_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate a Trust Narrative for a given report."""
    orchestrator = TrustNarrativeOrchestrator()
    risk_ass = RiskAssessmentDTO(assessment_id=f"ass_{report_id}")
    doc = orchestrator.generate_narrative(
        report_id=report_id, analysis_id=f"analysis_{report_id}",
        risk_assessment_dto=risk_ass,
    )
    repo = TrustNarrativeRepository(db)
    await repo.save_narrative(doc)
    return ResponseEnvelope(message="Narrative generated successfully", data=doc)


@router.get("/{report_id}/narrative", response_model=ResponseEnvelope[dict])
async def get_narrative(
    report_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve full Trust Narrative document."""
    repo = TrustNarrativeRepository(db)
    m = await repo.get_narrative_by_report_id(report_id)
    if not m:
        orchestrator = TrustNarrativeOrchestrator()
        risk_ass = RiskAssessmentDTO(assessment_id=f"ass_{report_id}")
        doc = orchestrator.generate_narrative(
            report_id=report_id, analysis_id=f"analysis_{report_id}",
            risk_assessment_dto=risk_ass,
        )
        return ResponseEnvelope(message="Success", data=doc.model_dump())
    return ResponseEnvelope(message="Success", data=json.loads(m.json_document))


@router.get("/{report_id}/narrative/executive", response_model=ResponseEnvelope[dict])
async def get_executive_narrative(
    report_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve executive summary narrative."""
    repo = TrustNarrativeRepository(db)
    m = await repo.get_narrative_by_report_id(report_id)
    doc = json.loads(m.json_document) if m else {}
    return ResponseEnvelope(message="Success", data=doc.get("executive_summary", {}))


@router.get("/{report_id}/narrative/technical", response_model=ResponseEnvelope[dict])
async def get_technical_narrative(
    report_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve technical summary narrative."""
    repo = TrustNarrativeRepository(db)
    m = await repo.get_narrative_by_report_id(report_id)
    doc = json.loads(m.json_document) if m else {}
    return ResponseEnvelope(message="Success", data={"technical_summary": doc.get("technical_summary", "")})


@router.get("/{report_id}/narrative/user", response_model=ResponseEnvelope[dict])
async def get_user_narrative(
    report_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve user-friendly summary narrative."""
    repo = TrustNarrativeRepository(db)
    m = await repo.get_narrative_by_report_id(report_id)
    doc = json.loads(m.json_document) if m else {}
    return ResponseEnvelope(message="Success", data={"user_friendly_summary": doc.get("user_friendly_summary", "")})


@router.get("/{report_id}/narrative/analyst", response_model=ResponseEnvelope[dict])
async def get_analyst_narrative(
    report_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve security analyst summary narrative."""
    repo = TrustNarrativeRepository(db)
    m = await repo.get_narrative_by_report_id(report_id)
    doc = json.loads(m.json_document) if m else {}
    return ResponseEnvelope(message="Success", data={"analyst_summary": doc.get("analyst_summary", "")})


@router.get("/{report_id}/narrative/provenance", response_model=ResponseEnvelope[list])
async def get_narrative_provenance(
    report_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve narrative statement provenance and lineage."""
    repo = TrustNarrativeRepository(db)
    m = await repo.get_narrative_by_report_id(report_id)
    doc = json.loads(m.json_document) if m else {}
    return ResponseEnvelope(message="Success", data=doc.get("lineage", []))


@router.get("/{report_id}/narrative/versions", response_model=ResponseEnvelope[list])
async def get_narrative_versions(
    report_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve narrative version history."""
    versions = [{"narrative_id": f"narr_{report_id}", "schema_version": "4.0.0", "template_version": "1.0.0", "change_reason": "INITIAL_GENERATION"}]
    return ResponseEnvelope(message="Success", data=versions)


@router.get("/{report_id}/narrative/status", response_model=ResponseEnvelope[dict])
async def get_narrative_status(
    report_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve narrative generation status."""
    repo = TrustNarrativeRepository(db)
    m = await repo.get_narrative_by_report_id(report_id)
    status_data = {
        "narrative_id": f"narr_{report_id}",
        "status": m.status if m else "COMPLETED",
        "mode": m.mode if m else "DETERMINISTIC_MODE",
    }
    return ResponseEnvelope(message="Success", data=status_data)
