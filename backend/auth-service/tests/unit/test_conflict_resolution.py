import pytest
from app.services.knowledge.security_reasoning_engine import SecurityReasoningEngine
from app.services.knowledge.knowledge_fabric_service import KnowledgeFabricService


def test_conflict_detection_and_precedence_resolution():
    fabric = KnowledgeFabricService()
    reasoning = SecurityReasoningEngine(fabric)

    # 1. Detect conflict when claiming CRITICAL severity with only 0.20 confidence evidence
    conflict = reasoning.detect_conflicts(
        entity_reference="domain:uncertain-target.com",
        claimed_verdict="CRITICAL",
        supporting_confidence=0.20,
        tenant_id="tenant_conf",
    )
    assert conflict is not None
    assert conflict.conflict_type == "CONFIDENCE_SEVERITY_MISMATCH"
    assert conflict.resolution_status == "UNRESOLVED"

    # 2. Resolve conflict by evidence precedence
    resolved = reasoning.resolve_conflict_by_precedence(
        conflict_id=conflict.conflict_id,
        direct_verified=True,
        is_recent=True,
        source_trusted=True,
        tenant_id="tenant_conf",
    )
    assert resolved.resolution_status == "RESOLVED_PRECEDENCE"
    assert "Direct verified" in resolved.resolution_rationale
