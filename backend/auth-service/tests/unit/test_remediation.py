import pytest
from app.services.enterprise_governance.compliance_remediation_engine import ComplianceRemediationEngine

def test_remediation_tasks_listing():
    engine = ComplianceRemediationEngine()
    tasks = engine.list_tasks()
    assert len(tasks) >= 1
    assert tasks[0].priority in ("P0", "P1", "P2", "P3")
