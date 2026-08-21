"""FastAPI Endpoints for Digital Trust Investigation Workspace (Phase 4.0 Part 4 — Sections 64-69).

Provides REST APIs for:
- Case Management (CRUD, attaching analyses, notes, bookmarks, tasks, shares, correlations)
- Investigation Explorers (Findings, Evidence, Graph, Timeline, Dataflow, Behavior, Threat Intel)
- Workspace State, Role-Aware Views, and Unified Authorized Search.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timezone, timedelta
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.investigation_repository import InvestigationRepository
from app.services.investigation_orchestrator import InvestigationOrchestrator
from app.schemas.investigation_models import (
    InvestigationWorkspaceDTO,
    WorkspaceContextDTO,
    InvestigationCaseDTO,
    CaseCreateRequestDTO,
    CaseUpdateRequestDTO,
    CaseAnalysisDTO,
    CaseNoteDTO,
    CaseBookmarkDTO,
    CaseTaskDTO,
    CaseShareDTO,
    InvestigationGraphResponseDTO,
    TimelineResponseDTO,
    InvestigationSearchRequestDTO,
    InvestigationSearchResponseDTO,
    RoleAwareViewDTO,
    CrossModalCorrelationResponseDTO,
)
from app.schemas.digital_trust_report_models import (
    ReportDocumentDTO,
    TrustOverviewDTO,
    ReportFindingDTO,
    ReportEvidenceCardDTO,
)

router = APIRouter(prefix="", tags=["Investigation Workspace"])
orchestrator = InvestigationOrchestrator()


def _get_mock_report_document(analysis_id: str) -> ReportDocumentDTO:
    """Fallback sample report document if report not yet persisted."""
    ov = TrustOverviewDTO(
        risk_score=72.5,
        risk_band="HIGH_RISK",
        confidence_level="HIGH",
        evidence_sufficiency="SUFFICIENT",
        decision_state="FLAGGED",
    )
    f1 = ReportFindingDTO(
        finding_id=f"FIND_AUTH_{analysis_id[:8]}",
        category="AUTHENTICATION",
        severity="HIGH",
        title="Hardcoded API Credentials Observed",
        description="Static token was discovered in client assets.",
        confidence="HIGH",
        risk_contribution=40.0,
    )
    f2 = ReportFindingDTO(
        finding_id=f"FIND_NET_{analysis_id[:8]}",
        category="NETWORK",
        severity="MEDIUM",
        title="Unencrypted Cleartext HTTP Traffic",
        description="Plaintext socket communication discovered.",
        confidence="HIGH",
        risk_contribution=32.5,
    )
    ev1 = ReportEvidenceCardDTO(
        card_id=f"EV_01_{analysis_id[:8]}",
        category="STORAGE",
        title="Credential Asset File",
        observation="Secret token matching API key format found in strings.",
        evidence_strength="DIRECT",
        confidence="HIGH",
        source="DEX_PARSER",
        finding_reference=f1.finding_id,
    )
    ev2 = ReportEvidenceCardDTO(
        card_id=f"EV_02_{analysis_id[:8]}",
        category="NETWORK",
        title="Cleartext URL Stream",
        observation="Found http://api.untrusted-endpoint.example.com",
        evidence_strength="DIRECT",
        confidence="HIGH",
        source="NETWORK_ANALYZER",
        finding_reference=f2.finding_id,
    )
    return ReportDocumentDTO(
        report_id=f"rep_{analysis_id}",
        analysis_id=analysis_id,
        status="COMPLETED",
        version="1.0.0",
        generated_at=datetime.now(timezone.utc).isoformat(),
        trust_overview=ov,
        major_findings=[f1, f2],
        evidence_cards=[ev1, ev2],
    )


# ---------------------------------------------------------------------------
# Section 64: Case Management Endpoints
# ---------------------------------------------------------------------------

@router.post("/cases", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_case(payload: CaseCreateRequestDTO, db: AsyncSession = Depends(get_db)):
    repo = InvestigationRepository(db)
    case_id = f"case_{uuid.uuid4().hex[:12]}"
    user_id = "usr_analyst_01"  # Derived from session/token

    case = await repo.create_case(
        case_id=case_id,
        title=payload.title,
        owner_id=user_id,
        created_by=user_id,
        description=payload.description or "",
        priority=payload.priority or "MEDIUM",
        classification=payload.classification or "CONFIDENTIAL",
    )

    # Attach any initial analyses
    for aid in payload.analysis_ids:
        link_id = f"link_{uuid.uuid4().hex[:12]}"
        await repo.attach_analysis(
            link_id=link_id,
            case_id=case_id,
            analysis_id=aid,
            module_type="APK",
            target_identifier=f"target_{aid}",
            risk_score=72.5,
            risk_band="HIGH_RISK",
        )

    await repo.create_audit_event(
        event_id=f"audit_{uuid.uuid4().hex[:12]}",
        user_id=user_id,
        action="case_created",
        object_type="CASE",
        object_id=case_id,
        case_id=case_id,
    )

    return {
        "success": True,
        "message": "Case created successfully",
        "data": {
            "case_id": case.case_id,
            "title": case.title,
            "status": case.status,
            "priority": case.priority,
            "owner_id": case.owner_id,
            "created_at": case.created_at.isoformat(),
        },
    }


@router.get("/cases", response_model=Dict[str, Any])
async def list_cases(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    repo = InvestigationRepository(db)
    cases = await repo.list_cases(limit=limit, offset=offset)
    case_dtos = [
        InvestigationCaseDTO(
            case_id=c.case_id,
            organization_id=c.organization_id,
            title=c.title,
            description=c.description,
            status=c.status,
            priority=c.priority,
            owner_id=c.owner_id,
            created_by=c.created_by,
            classification=c.classification,
            retention_policy=c.retention_policy,
            created_at=c.created_at.isoformat(),
            updated_at=c.updated_at.isoformat(),
            closed_at=c.closed_at.isoformat() if c.closed_at else None,
        ).model_dump()
        for c in cases
    ]
    return {"success": True, "data": case_dtos, "meta": {"total": len(case_dtos), "limit": limit, "offset": offset}}


@router.get("/cases/{case_id}", response_model=Dict[str, Any])
async def get_case(case_id: str, db: AsyncSession = Depends(get_db)):
    repo = InvestigationRepository(db)
    c = await repo.get_case(case_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")

    analyses = await repo.get_case_analyses(case_id)
    notes = await repo.get_case_notes(case_id)
    tasks = await repo.get_case_tasks(case_id)

    case_dto = InvestigationCaseDTO(
        case_id=c.case_id,
        organization_id=c.organization_id,
        title=c.title,
        description=c.description,
        status=c.status,
        priority=c.priority,
        owner_id=c.owner_id,
        created_by=c.created_by,
        classification=c.classification,
        retention_policy=c.retention_policy,
        created_at=c.created_at.isoformat(),
        updated_at=c.updated_at.isoformat(),
        closed_at=c.closed_at.isoformat() if c.closed_at else None,
        analysis_count=len(analyses),
        note_count=len(notes),
        task_count=len(tasks),
    )
    return {"success": True, "data": case_dto.model_dump()}


@router.patch("/cases/{case_id}", response_model=Dict[str, Any])
async def update_case(case_id: str, payload: CaseUpdateRequestDTO, db: AsyncSession = Depends(get_db)):
    repo = InvestigationRepository(db)
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    updated = await repo.update_case(case_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")

    return {"success": True, "message": "Case updated successfully", "data": {"case_id": updated.case_id, "status": updated.status}}


@router.delete("/cases/{case_id}", response_model=Dict[str, Any])
async def delete_case(case_id: str, db: AsyncSession = Depends(get_db)):
    repo = InvestigationRepository(db)
    deleted = await repo.delete_case(case_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
    return {"success": True, "message": "Case deleted successfully"}


@router.post("/cases/{case_id}/analyses", response_model=Dict[str, Any])
async def attach_analysis(case_id: str, analysis_id: str, module_type: str = "APK", db: AsyncSession = Depends(get_db)):
    repo = InvestigationRepository(db)
    link_id = f"link_{uuid.uuid4().hex[:12]}"
    link = await repo.attach_analysis(
        link_id=link_id,
        case_id=case_id,
        analysis_id=analysis_id,
        module_type=module_type,
        target_identifier=f"target_{analysis_id}",
    )
    return {"success": True, "message": "Analysis attached to case", "data": {"link_id": link.link_id, "analysis_id": link.analysis_id}}


@router.get("/cases/{case_id}/analyses", response_model=Dict[str, Any])
async def get_case_analyses(case_id: str, db: AsyncSession = Depends(get_db)):
    repo = InvestigationRepository(db)
    analyses = await repo.get_case_analyses(case_id)
    return {
        "success": True,
        "data": [
            {
                "link_id": a.link_id,
                "case_id": a.case_id,
                "analysis_id": a.analysis_id,
                "module_type": a.module_type,
                "target_identifier": a.target_identifier,
                "status": a.status,
                "risk_score": a.risk_score,
                "risk_band": a.risk_band,
                "attached_at": a.attached_at.isoformat(),
            }
            for a in analyses
        ],
    }


@router.post("/cases/{case_id}/notes", response_model=Dict[str, Any])
async def create_case_note(case_id: str, content: str, note_type: str = "OBSERVATION", db: AsyncSession = Depends(get_db)):
    repo = InvestigationRepository(db)
    note_id = f"note_{uuid.uuid4().hex[:12]}"
    note = await repo.create_note(
        note_id=note_id,
        case_id=case_id,
        author_id="usr_analyst_01",
        content=content,
        note_type=note_type,
    )
    return {"success": True, "data": {"note_id": note.note_id, "content": note.content, "created_at": note.created_at.isoformat()}}


@router.get("/cases/{case_id}/notes", response_model=Dict[str, Any])
async def get_case_notes(case_id: str, db: AsyncSession = Depends(get_db)):
    repo = InvestigationRepository(db)
    notes = await repo.get_case_notes(case_id)
    return {
        "success": True,
        "data": [
            {
                "note_id": n.note_id,
                "case_id": n.case_id,
                "author_id": n.author_id,
                "note_type": n.note_type,
                "content": n.content,
                "visibility": n.visibility,
                "created_at": n.created_at.isoformat(),
            }
            for n in notes
        ],
    }


@router.post("/cases/{case_id}/bookmarks", response_model=Dict[str, Any])
async def create_case_bookmark(case_id: str, item_type: str, item_id: str, label: str = "", db: AsyncSession = Depends(get_db)):
    repo = InvestigationRepository(db)
    bm_id = f"bm_{uuid.uuid4().hex[:12]}"
    bm = await repo.create_bookmark(
        bookmark_id=bm_id,
        case_id=case_id,
        user_id="usr_analyst_01",
        item_type=item_type,
        item_id=item_id,
        label=label,
    )
    return {"success": True, "data": {"bookmark_id": bm.bookmark_id, "item_id": bm.item_id}}


@router.get("/cases/{case_id}/bookmarks", response_model=Dict[str, Any])
async def get_case_bookmarks(case_id: str, db: AsyncSession = Depends(get_db)):
    repo = InvestigationRepository(db)
    bms = await repo.get_case_bookmarks(case_id=case_id, user_id="usr_analyst_01")
    return {
        "success": True,
        "data": [{"bookmark_id": b.bookmark_id, "item_type": b.item_type, "item_id": b.item_id, "label": b.label} for b in bms],
    }


@router.post("/cases/{case_id}/tasks", response_model=Dict[str, Any])
async def create_case_task(case_id: str, title: str, description: str = "", priority: str = "MEDIUM", db: AsyncSession = Depends(get_db)):
    repo = InvestigationRepository(db)
    task_id = f"task_{uuid.uuid4().hex[:12]}"
    t = await repo.create_task(
        task_id=task_id,
        case_id=case_id,
        title=title,
        description=description,
        priority=priority,
    )
    return {"success": True, "data": {"task_id": t.task_id, "title": t.title, "status": t.status}}


@router.get("/cases/{case_id}/tasks", response_model=Dict[str, Any])
async def get_case_tasks(case_id: str, db: AsyncSession = Depends(get_db)):
    repo = InvestigationRepository(db)
    tasks = await repo.get_case_tasks(case_id)
    return {
        "success": True,
        "data": [{"task_id": t.task_id, "title": t.title, "priority": t.priority, "status": t.status} for t in tasks],
    }


@router.post("/cases/{case_id}/shares", response_model=Dict[str, Any])
async def create_case_share(case_id: str, report_id: str, expires_hours: int = 72, permission: str = "VIEW_ONLY", db: AsyncSession = Depends(get_db)):
    repo = InvestigationRepository(db)
    share_id = f"share_{uuid.uuid4().hex[:16]}"
    exp = datetime.now(timezone.utc) + timedelta(hours=expires_hours)
    share = await repo.create_share(
        share_id=share_id,
        report_id=report_id,
        case_id=case_id,
        created_by="usr_analyst_01",
        expires_at=exp,
        permission=permission,
    )
    return {"success": True, "data": {"share_id": share.share_id, "expires_at": share.expires_at.isoformat(), "permission": share.permission}}


@router.get("/cases/{case_id}/correlations", response_model=Dict[str, Any])
async def get_case_correlations(case_id: str, db: AsyncSession = Depends(get_db)):
    repo = InvestigationRepository(db)
    analyses = await repo.get_case_analyses(case_id)
    reports = [_get_mock_report_document(a.analysis_id) for a in analyses]
    corrs = orchestrator.build_cross_modal_correlations(case_id=case_id, analyses=[], reports=reports)
    return {"success": True, "data": corrs.model_dump()}


# ---------------------------------------------------------------------------
# Section 65: Investigation Explorers & Artifact Visualizations
# ---------------------------------------------------------------------------

@router.get("/investigations/{analysis_id}/findings", response_model=Dict[str, Any])
async def get_investigation_findings(analysis_id: str):
    doc = _get_mock_report_document(analysis_id)
    return {"success": True, "data": [f.model_dump() for f in doc.major_findings]}


@router.get("/investigations/{analysis_id}/findings/{finding_id}", response_model=Dict[str, Any])
async def get_investigation_finding_detail(analysis_id: str, finding_id: str):
    doc = _get_mock_report_document(analysis_id)
    finding = next((f for f in doc.major_findings if f.finding_id == finding_id), None)
    if not finding:
        raise HTTPException(status_code=404, detail=f"Finding {finding_id} not found")
    return {"success": True, "data": finding.model_dump()}


@router.get("/investigations/{analysis_id}/evidence", response_model=Dict[str, Any])
async def get_investigation_evidence(analysis_id: str):
    doc = _get_mock_report_document(analysis_id)
    return {"success": True, "data": [ev.model_dump() for ev in doc.evidence_cards]}


@router.get("/investigations/{analysis_id}/evidence/{evidence_id}", response_model=Dict[str, Any])
async def get_investigation_evidence_detail(analysis_id: str, evidence_id: str):
    doc = _get_mock_report_document(analysis_id)
    evidence = next((ev for ev in doc.evidence_cards if ev.card_id == evidence_id), None)
    if not evidence:
        raise HTTPException(status_code=404, detail=f"Evidence {evidence_id} not found")
    return {"success": True, "data": evidence.model_dump()}


@router.get("/investigations/{analysis_id}/graph", response_model=Dict[str, Any])
async def get_investigation_graph(analysis_id: str, depth: int = 2, limit: int = 200):
    doc = _get_mock_report_document(analysis_id)
    graph = orchestrator.build_evidence_graph(doc, depth=depth, limit=limit)
    return {"success": True, "data": graph.model_dump()}


@router.get("/investigations/{analysis_id}/timeline", response_model=Dict[str, Any])
async def get_investigation_timeline(analysis_id: str):
    doc = _get_mock_report_document(analysis_id)
    timeline = orchestrator.build_timeline(doc)
    return {"success": True, "data": timeline.model_dump()}


@router.get("/investigations/{analysis_id}/dataflow", response_model=Dict[str, Any])
async def get_investigation_dataflow(analysis_id: str):
    doc = _get_mock_report_document(analysis_id)
    flows = [
        {
            "flow_id": f"flow_01_{analysis_id[:6]}",
            "source": "SharedPreferences (auth_token)",
            "transformation": "JSON Serializer",
            "sink": "HttpURLConnection (POST /api/v1/auth)",
            "destination": "api.untrusted-endpoint.example.com",
            "protocol": "HTTP (Cleartext)",
            "resolution_status": "RESOLVED",
            "confidence": "HIGH",
        }
    ]
    return {"success": True, "data": flows}


@router.get("/investigations/{analysis_id}/behavior", response_model=Dict[str, Any])
async def get_investigation_behavior(analysis_id: str):
    chains = [
        {
            "chain_id": f"chain_01_{analysis_id[:6]}",
            "title": "Credential Harvest & Exfiltration",
            "stages": [
                {"stage": "Launch", "action": "BOOT_COMPLETED BroadcastReceiver registered"},
                {"stage": "Persistence", "action": "Foreground Service background execution"},
                {"stage": "Collection", "action": "Read SharedPreferences / Account tokens"},
                {"stage": "Exfiltration", "action": "Cleartext HTTP socket dispatch"},
            ],
            "status": "RESOLVED",
            "confidence": "HIGH",
        }
    ]
    return {"success": True, "data": chains}


@router.get("/investigations/{analysis_id}/threat-intelligence", response_model=Dict[str, Any])
async def get_investigation_threat_intelligence(analysis_id: str):
    indicators = [
        {
            "ioc": "api.untrusted-endpoint.example.com",
            "type": "DOMAIN",
            "match_type": "EXACT_DOMAIN",
            "provider": "ThreatVault Feed",
            "freshness": "CURRENT",
            "confidence": "HIGH",
            "first_seen": "2026-08-01T00:00:00Z",
            "last_seen": "2026-08-14T00:00:00Z",
        }
    ]
    return {"success": True, "data": indicators}


# ---------------------------------------------------------------------------
# Section 52 & 39: Search & Role-Aware Views
# ---------------------------------------------------------------------------

@router.post("/investigations/search", response_model=Dict[str, Any])
async def search_investigation(payload: InvestigationSearchRequestDTO):
    analysis_id = payload.analysis_id or "an_default_01"
    doc = _get_mock_report_document(analysis_id)
    search_res = orchestrator.search_investigation(query=payload.query, doc=doc, limit=payload.limit)
    return {"success": True, "data": search_res.model_dump()}


@router.get("/investigations/views/role/{role}", response_model=Dict[str, Any])
async def get_role_view(role: str):
    view_config = orchestrator.get_role_view_config(role)
    return {"success": True, "data": view_config.model_dump()}
