import pytest
from app.services.governance_fabric.governance_evidence_collector import GovernanceEvidenceCollector


def test_ai_governance_registry():
    collector = GovernanceEvidenceCollector()

    ev = collector.record_evidence(
        control_id="ctrl_ai_01",
        source_system="AI_GOVERNANCE_REGISTRY",
        payload={"model_id": "security_copilot_v2", "risk_level": "LOW", "human_oversight_required": True},
    )

    assert ev.payload["human_oversight_required"] is True
