import pytest
from app.services.copilot.threat_hunting_copilot import ThreatHuntingCopilot


def test_copilot_query_safety_mutation_rejection():
    hunter = ThreatHuntingCopilot()

    # Mutation query should be detected and marked unsafe
    assert hunter.validate_query("DROP TABLE auth_events;") is False
    assert hunter.validate_query("DELETE FROM users WHERE 1=1;") is False
    assert hunter.validate_query("SELECT * FROM auth_events LIMIT 10;") is True
