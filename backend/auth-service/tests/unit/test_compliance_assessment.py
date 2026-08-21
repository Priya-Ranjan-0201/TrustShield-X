import pytest
from app.services.governance_fabric.compliance_assessment_engine import ComplianceAssessmentEngine
from app.schemas.governance_fabric_models import GovernanceRequirementDTO, GovernanceEvidenceDTO


def test_compliance_assessment_scenarios():
    engine = ComplianceAssessmentEngine()
    req = GovernanceRequirementDTO(
        requirement_id="req_test_01",
        framework_id="fw_iso_27001",
        control_reference="A.1",
        title="T",
        description="D",
        category="C",
    )

    # 1. No evidence -> NOT_ASSESSED
    res_no_ev = engine.assess_requirement(req, [])
    assert res_no_ev["status"] == "NOT_ASSESSED"

    # 2. Fresh evidence and passed test -> SATISFIED
    ev = GovernanceEvidenceDTO(
        evidence_id="e1",
        control_id="c1",
        source_system="S",
        integrity_hash="h",
        freshness="CURRENT",
    )
    res_sat = engine.assess_requirement(req, [ev], control_test_passed=True)
    assert res_sat["status"] == "SATISFIED"
    assert res_sat["confidence"] >= 0.90

    # 3. Failed test -> NOT_SATISFIED
    res_failed = engine.assess_requirement(req, [ev], control_test_passed=False)
    assert res_failed["status"] == "NOT_SATISFIED"
