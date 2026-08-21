import pytest
from app.services.hunting.hypothesis_challenge_engine import HypothesisChallengeEngine


def test_hypothesis_challenge_alternative_explanations():
    engine = HypothesisChallengeEngine()
    alternatives = engine.generate_alternative_explanations("INFRASTRUCTURE_REUSE", "New DNS CNAME mapping")
    assert len(alternatives) >= 3
    assert any("migration" in a.lower() for a in alternatives)
