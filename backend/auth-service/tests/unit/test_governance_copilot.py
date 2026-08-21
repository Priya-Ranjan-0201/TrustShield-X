import pytest
from app.services.governance_fabric.compliance_assessment_engine import ComplianceAssessmentEngine
from app.schemas.governance_fabric_models import GovernanceRequirementDTO, GovernanceEvidenceDTO


def test_governance_copilot_evidence_grounding():
    engine = ComplianceAssessmentEngine()
    req = GovernanceRequirementDTO(
        requirement_id="req_grounding_01",
        framework_id="fw_dpdp_2023",
        control_reference="Sec. 8",
        title="Data Protection Safeguards",
        description="D",
        category="C",
    )

    ev = GovernanceEvidenceDTO(
        evidence_id="evi_ground_01",
        control_id="ctrl_audit_01",
        source_system="AUDIT_SERVICE",
        integrity_hash="sha256_mock",
        freshness="CURRENT",
    )

    res = engine.assess_requirement(req, [ev], control_test_passed=True)
    # Invariant: Copilot assessment is grounded on verifiable evidence and confidence
    assert res["status"] == "SATISFIED"
    assert res["confidence"] >= 0.90
    assert len(res["reason"]) > 0
