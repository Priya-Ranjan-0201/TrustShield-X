import pytest
from app.services.governance_fabric.governance_framework_registry import GovernanceFrameworkRegistry


def test_governance_framework_registry():
    registry = GovernanceFrameworkRegistry()
    frameworks = registry.list_frameworks()

    assert len(frameworks) >= 4
    fw_names = [f.name for f in frameworks]
    assert any("DPDP" in name for name in fw_names)
    assert any("ISO" in name for name in fw_names)
    assert any("SOC 2" in name for name in fw_names)
