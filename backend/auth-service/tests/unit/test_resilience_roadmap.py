import pytest
from app.services.resilience_twin.resilience_roadmap_engine import ResilienceRoadmapEngine


def test_resilience_roadmap_temporal_stages():
    engine = ResilienceRoadmapEngine()
    roadmap = engine.generate_roadmap()

    assert len(roadmap.now_actions) >= 1
    assert len(roadmap.next_actions) >= 1
    assert len(roadmap.later_actions) >= 1
    assert roadmap.total_actions == len(roadmap.now_actions) + len(roadmap.next_actions) + len(roadmap.later_actions)
