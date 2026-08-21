import pytest
from app.services.governance_fabric.governance_framework_registry import GovernanceFrameworkRegistry


def test_governance_requirements():
    registry = GovernanceFrameworkRegistry()
    reqs = registry.list_requirements("fw_dpdp_2023")

    assert len(reqs) >= 1
    dpdp_req = reqs[0]
    assert dpdp_req.requirement_id == "req_dpdp_sec8"
    assert dpdp_req.status == "SATISFIED"
