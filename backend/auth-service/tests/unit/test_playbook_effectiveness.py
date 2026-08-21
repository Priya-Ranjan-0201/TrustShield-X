import pytest
from app.services.soc.soc_scorecard_engine import SOCScorecardEngine


def test_playbook_effectiveness_metrics():
    engine = SOCScorecardEngine()
    card = engine.compute_scorecard("tenant_pb_eff")

    assert card.automation_rate_pct > 80.0
    assert card.verification_rate_pct > 95.0
    assert card.failed_action_count == 0
