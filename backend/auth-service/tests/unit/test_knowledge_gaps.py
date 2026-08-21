import pytest
from app.services.knowledge_fabric.knowledge_gap_engine import KnowledgeGapEngine


def test_knowledge_gaps_detection():
    engine = KnowledgeGapEngine()

    gap = engine.record_gap(
        gap_type="UNKNOWN_CONTROL_STATUS",
        target_entity="ctrl_waf_edge_01",
        description="WAF rule telemetry stream disconnected.",
        security_impact="HIGH",
    )

    assert gap.gap_type == "UNKNOWN_CONTROL_STATUS"
    assert gap.target_entity == "ctrl_waf_edge_01"

    gaps = engine.list_gaps()
    assert len(gaps) >= 2
