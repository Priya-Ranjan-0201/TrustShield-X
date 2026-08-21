import pytest
from app.services.governance_fabric.governance_framework_registry import GovernanceFrameworkRegistry


def test_governance_policy_registry():
    registry = GovernanceFrameworkRegistry()
    frameworks = registry.list_frameworks()

    for f in frameworks:
        assert f.framework_id.startswith("fw_")
        assert f.status == "ACTIVE"
