import pytest
from app.services.threat_intelligence.threat_intelligence_graph_engine import ThreatIntelligenceGraphEngine
from app.schemas.threat_intelligence_fabric_models import ThreatGraphNodeDTO, ThreatGraphEdgeDTO


def test_graph_poisoning_preserves_provenance_and_confidence():
    engine = ThreatIntelligenceGraphEngine()

    fake_node = ThreatGraphNodeDTO(node_id="node_fake_claim", node_type="INDICATOR", label="benign.org")
    engine.add_node(fake_node)

    fake_edge = ThreatGraphEdgeDTO(
        source_node_id="node_camp_shadow",
        target_node_id="node_fake_claim",
        relationship_type="USES",
        confidence=0.15,
        source_id="src_unverified_contributor",
    )
    engine.add_edge(fake_edge)

    # Edge preserves low confidence and source provenance without auto-elevating
    assert fake_edge.confidence == 0.15
    assert fake_edge.source_id == "src_unverified_contributor"
