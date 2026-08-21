import pytest
from app.services.governance_fabric.compliance_assessment_engine import ComplianceAssessmentEngine
from app.schemas.governance_fabric_models import GovernanceRequirementDTO, GovernanceEvidenceDTO


def test_compliance_gap_identification():
    engine = ComplianceAssessmentEngine()
    req = GovernanceRequirementDTO(
        requirement_id="req_test_gap",
        framework_id="fw_soc2",
        control_reference="CC1",
        title="T",
        description="D",
        category="C",
    )

    ev_stale = GovernanceEvidenceDTO(
        evidence_id="e_stale",
        control_id="c1",
        source_system="S",
        integrity_hash="h",
        freshness="EXPIRED",
    )

    res = engine.assess_requirement(req, [ev_stale])
    assert "STALE_EVIDENCE" in res["gaps"]
    assert res["status"] == "PARTIALLY_SATISFIED"
