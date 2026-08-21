import pytest
from app.services.knowledge_fabric.security_hypothesis_engine import SecurityHypothesisEngine


def test_alternative_explanations_identification():
    engine = SecurityHypothesisEngine()
    hypotheses = engine.list_hypotheses()

    alt = next((h for h in hypotheses if h.is_alternative_explanation), None)
    assert alt is not None
    assert "Admin" in alt.title or "Anomaly" in alt.title
