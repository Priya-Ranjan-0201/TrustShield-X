import pytest
from app.services.knowledge_fabric.temporal_knowledge_engine import TemporalKnowledgeEngine


def test_twin_reasoning_simulation_labeling():
    engine = TemporalKnowledgeEngine()

    sim_rec = engine.record_temporal_state(
        object_id="sim_twin_outage_01",
        temporal_state="SIMULATED",
    )

    assert sim_rec.temporal_state == "SIMULATED"
