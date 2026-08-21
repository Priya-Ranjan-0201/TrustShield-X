import pytest
from app.services.knowledge_fabric.knowledge_quality_engine import KnowledgeQualityEngine


def test_knowledge_quality_scorecard():
    engine = KnowledgeQualityEngine()
    scorecard = engine.compute_scorecard(
        data_quality=95.0,
        evidence_quality=95.0,
        graph_quality=90.0,
        provenance_completeness=98.0,
        freshness_score=96.0,
        contradiction_rate=1.0,
    )

    assert scorecard.overall_health_score > 90.0
    assert scorecard.provenance_completeness == 98.0
