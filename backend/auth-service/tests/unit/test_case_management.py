import pytest
from app.services.soc.case_task_engine import CaseTaskEngine


def test_security_case_creation_and_retrieval():
    engine = CaseTaskEngine()
    case = engine.create_case(
        tenant_id="tenant_case",
        title="Payment Gateway Perimeter Intrusion",
        incident_ids=["inc_01", "inc_02"],
    )

    assert case.case_id.startswith("case_")
    assert case.status == "OPEN"
    assert len(case.incident_ids) == 2
    assert engine.get_case(case.case_id) is not None
