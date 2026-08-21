import pytest
from app.services.collective_defense.global_campaign_graph_engine import GlobalCampaignGraphEngine


def test_global_campaign_graph_nodes_and_edges():
    graph_engine = GlobalCampaignGraphEngine()

    n1 = graph_engine.add_or_update_node("node_ind_1", "INDICATOR", "phish-bank.com", confidence=0.85)
    n2 = graph_engine.add_or_update_node("node_c2_1", "INFRASTRUCTURE", "198.51.100.22", confidence=0.90)
    edge = graph_engine.add_edge("node_ind_1", "node_c2_1", "INFRASTRUCTURE_REUSE", confidence=0.80)

    g = graph_engine.export_graph()
    assert len(g.nodes) == 2
    assert len(g.edges) == 1
    assert edge.relationship == "INFRASTRUCTURE_REUSE"
