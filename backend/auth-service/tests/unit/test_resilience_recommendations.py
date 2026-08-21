import pytest
from app.schemas.cyber_resilience_twin_models import ResilienceRecommendationDTO
from app.services.resilience_twin.resilience_roadmap_engine import ResilienceRoadmapEngine


def test_resilience_recommendations_evidence_linkage():
    engine = ResilienceRoadmapEngine()
    rec = ResilienceRecommendationDTO(
        title="Upgrade WAF inspection for API endpoints",
        target_resource="api_gateway_ingress",
        risk_reduction_impact=80.0,
        implementation_effort="LOW",
        stage="NOW",
        evidence_references=["ev_api_abuse_trace"],
    )

    engine.add_recommendation(rec)
    roadmap = engine.generate_roadmap()

    now_rec = next((r for r in roadmap.now_actions if r.target_resource == "api_gateway_ingress"), None)
    assert now_rec is not None
    assert len(now_rec.evidence_references) >= 1
