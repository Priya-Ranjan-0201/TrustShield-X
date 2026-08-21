"""
TruthShield X — Cyber Security Knowledge Fabric API Endpoints (Phase 19).

REST API endpoints for Knowledge Objects, Search, Lineage, Evidence Graph, Contradictions,
Reasoning Traces, Hypotheses, Knowledge Gaps, Security Memory, Lessons Learned, and AI Assistant.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Query, HTTPException, status, Body
from app.schemas.cyber_knowledge_fabric_models import (
    KnowledgeObjectDTO,
    KnowledgeRelationshipDTO,
    KnowledgeLineageDTO,
    TemporalKnowledgeDTO,
    KnowledgeImpactDTO,
    EvidenceGraphDTO,
    EvidenceGraphNodeDTO,
    EvidenceContradictionDTO,
    ReasoningTraceDTO,
    SecurityHypothesisDTO,
    KnowledgeGapDTO,
    SecurityMemoryRecordDTO,
    LessonsLearnedDTO,
    SecurityKnowledgeAssistantResponseDTO,
    CyberKnowledgeFabricSummaryDTO,
)
from app.services.knowledge_fabric.cyber_security_knowledge_fabric import CyberSecurityKnowledgeFabric

router = APIRouter(tags=["Cyber Security Knowledge Fabric"])
fabric_service = CyberSecurityKnowledgeFabric()


@router.get("/knowledge/summary", response_model=CyberKnowledgeFabricSummaryDTO)
def get_fabric_summary(tenant_id: str = Query("default_tenant")):
    """Returns aggregated executive summary of the Knowledge Fabric."""
    return fabric_service.get_summary(tenant_id)


@router.get("/knowledge", response_model=List[KnowledgeObjectDTO])
def list_knowledge_objects(
    tenant_id: str = Query("default_tenant"),
    object_type: Optional[str] = Query(None),
):
    """Lists knowledge objects for a tenant, optionally filtered by type."""
    return fabric_service.objects.list_objects(tenant_id, object_type)


@router.get("/knowledge/search", response_model=List[KnowledgeObjectDTO])
def search_knowledge(
    query: str = Query(...),
    tenant_id: str = Query("default_tenant"),
):
    """Searches knowledge objects by canonical identifier or id."""
    objs = fabric_service.objects.list_objects(tenant_id)
    q_lower = query.lower()
    return [o for o in objs if q_lower in o.canonical_identifier.lower() or q_lower in o.object_id.lower()]


@router.get("/knowledge/graph", response_model=List[KnowledgeRelationshipDTO])
def get_knowledge_graph(include_revoked: bool = Query(False)):
    """Returns all relationships in the knowledge graph."""
    return fabric_service.relationships.list_all(include_revoked)


@router.get("/knowledge/{id}", response_model=KnowledgeObjectDTO)
def get_knowledge_object(id: str, tenant_id: str = Query("default_tenant")):
    """Retrieves a specific knowledge object."""
    obj = fabric_service.objects.get_object(id, tenant_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Knowledge object not found.")
    return obj


@router.get("/knowledge/{id}/lineage", response_model=Optional[KnowledgeLineageDTO])
def get_knowledge_lineage(id: str):
    """Returns full provenance and transformation lineage for a conclusion or object."""
    lineage = fabric_service.lineage.get_lineage(id)
    if not lineage:
        # Generate default empty lineage structure if not found
        return KnowledgeLineageDTO(
            conclusion_id=id,
            created_by_model="KnowledgeLineageEngine",
            source_data=[id],
            supporting_evidence=[],
            transformations=["DIRECT_LOOKUP"],
            models_used=["SYSTEM_FABRIC"],
            dependent_conclusions=[],
        )
    return lineage


@router.get("/knowledge/{id}/history", response_model=List[KnowledgeObjectDTO])
def get_knowledge_history(id: str, tenant_id: str = Query("default_tenant")):
    """Returns immutable version history for a knowledge object."""
    return fabric_service.objects.get_object_history(id, tenant_id)


@router.get("/knowledge/{id}/impact", response_model=Optional[KnowledgeImpactDTO])
def get_knowledge_impact(id: str):
    """Returns revocation impact and downstream affected artifacts."""
    return fabric_service.revocations.get_revocation_impact(id)


@router.get("/evidence/graph", response_model=EvidenceGraphDTO)
def get_evidence_graph():
    """Returns full evidence graph with supporting/contradicting edges."""
    return fabric_service.evidence_graph.build_graph()


@router.get("/evidence/{id}/support", response_model=List[EvidenceGraphNodeDTO])
def get_supporting_evidence(id: str):
    """Returns evidence nodes that support the specified assertion or entity."""
    return fabric_service.evidence_graph.get_supporting_evidence(id)


@router.get("/evidence/{id}/contradictions", response_model=List[EvidenceContradictionDTO])
def get_contradictions(id: str):
    """Returns recorded contradictions for an entity."""
    return fabric_service.contradictions.get_contradictions_for_entity(id)


@router.get("/reasoning/{id}", response_model=ReasoningTraceDTO)
def get_reasoning_trace(id: str):
    """Retrieves a reasoning trace for a conclusion."""
    trace = fabric_service.reasoning.get_trace(id)
    if not trace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reasoning trace not found.")
    return trace


@router.post("/reasoning/query", response_model=SecurityKnowledgeAssistantResponseDTO)
def query_knowledge_assistant(
    payload: Dict[str, Any] = Body(...),
    tenant_id: str = Query("default_tenant"),
):
    """Queries the AI Security Knowledge Assistant with strict answer contracts."""
    query = payload.get("query", "")
    return fabric_service.assistant.answer_query(query, tenant_id)


@router.get("/hypotheses", response_model=List[SecurityHypothesisDTO])
def list_hypotheses():
    """Lists competing hypotheses ranked by evidence corroboration."""
    return fabric_service.hypotheses.list_hypotheses()


@router.get("/knowledge-gaps", response_model=List[KnowledgeGapDTO])
def list_knowledge_gaps():
    """Lists detected security blind spots and missing knowledge gaps."""
    return fabric_service.gaps.list_gaps()


@router.get("/security-memory", response_model=List[SecurityMemoryRecordDTO])
def list_security_memory(tenant_id: str = Query("default_tenant")):
    """Lists persistent organizational memory strictly filtered by tenant."""
    return fabric_service.memory.list_memories(tenant_id)


@router.get("/lessons-learned", response_model=List[LessonsLearnedDTO])
def list_lessons_learned():
    """Lists lessons learned from past incident responses and defenses."""
    return fabric_service.analogs.list_lessons_learned()
