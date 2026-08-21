import pytest
from app.schemas.governance_fabric_models import GovernanceRemediationDTO


def test_governance_remediation_lifecycle():
    rem = GovernanceRemediationDTO(
        remediation_id="rem_01",
        finding_title="Enable MFA on secondary administration roles",
        requirement_id="req_iso_a9_4",
        owner="secops_engineer",
        priority="HIGH",
        due_date="2026-09-01",
        action_plan="Deploy FIDO2 WebAuthn keys for secondary tier accounts",
        status="OPEN",
    )

    assert rem.status == "OPEN"
    assert rem.priority == "HIGH"
