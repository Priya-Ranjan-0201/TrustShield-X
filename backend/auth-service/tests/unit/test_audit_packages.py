import pytest
from app.services.governance_fabric.audit_preparation_engine import AuditPreparationEngine
from app.services.governance_fabric.governance_framework_registry import GovernanceFrameworkRegistry
from app.services.governance_fabric.governance_evidence_collector import GovernanceEvidenceCollector


def test_audit_package_manifest_integrity():
    registry = GovernanceFrameworkRegistry()
    collector = GovernanceEvidenceCollector()
    audit_engine = AuditPreparationEngine()

    reqs = registry.list_requirements("fw_dpdp_2023")
    evs = collector.list_evidence()

    pkg = audit_engine.compile_audit_package("fw_dpdp_2023", "2023", reqs, evs)
    assert len(pkg.limitations) >= 1
    assert "Evidence validity limited" in pkg.limitations[0]
