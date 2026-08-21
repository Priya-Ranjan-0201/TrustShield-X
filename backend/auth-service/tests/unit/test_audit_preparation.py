import pytest
from app.services.governance_fabric.audit_preparation_engine import AuditPreparationEngine
from app.services.governance_fabric.governance_framework_registry import GovernanceFrameworkRegistry
from app.services.governance_fabric.governance_evidence_collector import GovernanceEvidenceCollector


def test_audit_preparation_compilation():
    registry = GovernanceFrameworkRegistry()
    collector = GovernanceEvidenceCollector()
    audit_engine = AuditPreparationEngine()

    reqs = registry.list_requirements("fw_soc2_t2")
    evs = collector.list_evidence()

    pkg = audit_engine.compile_audit_package("fw_soc2_t2", "2022", reqs, evs)
    assert pkg.package_id.startswith("pkg_")
    assert pkg.total_requirements_assessed == len(reqs)
    assert len(pkg.integrity_manifest_hash) == 64
