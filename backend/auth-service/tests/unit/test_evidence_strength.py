import pytest
from app.services.knowledge_fabric.evidence_strength_engine import EvidenceStrengthEngine


def test_seven_dimension_evidence_strength():
    engine = EvidenceStrengthEngine()
    strength = engine.evaluate_strength(
        source_reliability=0.95,
        directness=0.90,
        freshness=0.98,
        corroboration=0.85,
        reproducibility=0.92,
        integrity=1.0,
        independence=0.88,
    )

    assert strength.source_reliability == 0.95
    assert strength.integrity == 1.0
    assert 0.90 <= strength.overall_strength <= 0.96
