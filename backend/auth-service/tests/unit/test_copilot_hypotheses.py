import pytest
from app.services.copilot.investigation_copilot import InvestigationCopilot


def test_copilot_hypotheses_ranking():
    investigation = InvestigationCopilot()
    summary = investigation.build_investigation_summary("inc_001")

    assert len(summary.likely_hypotheses) >= 2
    assert "H1:" in summary.likely_hypotheses[0]
    assert "H2:" in summary.likely_hypotheses[1]
