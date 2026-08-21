import pytest
from app.services.copilot.investigation_copilot import InvestigationCopilot


def test_copilot_investigation_workflow():
    investigation = InvestigationCopilot()
    summary = investigation.build_investigation_summary("inc_pay_01")

    assert summary.investigation_id == "inv_inc_pay_01"
    assert len(summary.what_we_know) >= 2
    assert len(summary.what_we_do_not_know) >= 2
    assert len(summary.recommended_actions) >= 2
