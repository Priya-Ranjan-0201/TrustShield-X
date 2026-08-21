import pytest
from app.services.knowledge_fabric.decision_traceability_engine import DecisionTraceabilityEngine


def test_defense_reasoning_policy_links():
    engine = DecisionTraceabilityEngine()
    dec = engine.record_decision(
        decision_type="DEFENSIVE_ISOLATION",
        driving_knowledge=["kobj_cve_9942"],
        supporting_evidence=["ev_pcap_trace_88"],
        governing_policy="POL_SEC_ADAPTIVE_DEFENSE",
        alternative_options=["LOG_ALERT"],
        decision_maker="POLICY_ENGINE_V2",
    )

    assert dec.governing_policy == "POL_SEC_ADAPTIVE_DEFENSE"
    assert "ev_pcap_trace_88" in dec.supporting_evidence
