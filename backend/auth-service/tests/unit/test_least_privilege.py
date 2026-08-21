import pytest
from app.services.zero_trust_exposure.privilege_governance_engine import PrivilegeGovernanceEngine

def test_excess_privilege_detection():
    engine = PrivilegeGovernanceEngine()
    res = engine.detect_excess_privilege(
        tenant_id="t1",
        identity_id="USR-EXCESS",
        assigned_roles=["ADMIN", "ANALYST", "OPERATOR"],
        used_roles=["ANALYST"],
        assigned_permissions=["read", "write", "delete", "export"],
        used_permissions=["read"]
    )
    assert res["has_excess_privilege"] is True
    assert "ADMIN" in res["unused_roles"]
    assert "delete" in res["unused_permissions"]
    assert res["finding_type"] == "EXCESS_PRIVILEGE"
