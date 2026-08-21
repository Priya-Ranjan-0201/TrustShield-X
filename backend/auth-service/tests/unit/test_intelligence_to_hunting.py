import pytest
from app.services.threat_intelligence.intelligence_operationalization_engine import IntelligenceOperationalizationEngine


def test_intelligence_to_hunting_hypothesis_structure():
    engine = IntelligenceOperationalizationEngine()
    hunt = engine.generate_hunting_hypothesis("T1059.001", "c2.shadowhydra.net")

    assert "SELECT" in hunt["query"]
    assert "T1059.001" in hunt["hypothesis"]
    assert hunt["limitations"] is not None
