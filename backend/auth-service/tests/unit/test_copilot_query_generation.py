import pytest
from app.services.copilot.threat_hunting_copilot import ThreatHuntingCopilot


def test_copilot_multi_syntax_query_generation():
    hunter = ThreatHuntingCopilot()

    sql_q = hunter.generate_hunt_query("SQL", "srv_1", "test")
    log_q = hunter.generate_hunt_query("LOG", "srv_1", "test")
    graph_q = hunter.generate_hunt_query("GRAPH", "srv_1", "test")

    assert "SELECT" in sql_q.query_text
    assert "stats count" in log_q.query_text
    assert "MATCH" in graph_q.query_text
