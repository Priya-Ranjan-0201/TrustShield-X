import pytest
from app.services.response_decision_engine import ResponseDecisionEngine
from app.schemas.autonomous_defense_models import DecisionContextDTO


def test_safety_classification_tiers():
    engine = ResponseDecisionEngine()
    assert engine.classify_action_safety("COLLECT_EVIDENCE") == "READ_ONLY"
    assert engine.classify_action_safety("ENRICH_IOC") == "READ_ONLY"
    assert engine.classify_action_safety("MARK_INDICATOR") == "LOW_RISK_MUTATION"
    assert engine.classify_action_safety("BLOCK_DOMAIN") == "HIGH_RISK_MUTATION"
    assert engine.classify_action_safety("QUARANTINE_FILE") == "HIGH_RISK_MUTATION"
    assert engine.classify_action_safety("DELETE_RESOURCE") == "DESTRUCTIVE"
    assert engine.classify_action_safety("PERMANENT_DELETE_DATA") == "IRREVERSIBLE"


def test_legal_hold_blocks_destructive_actions():
    engine = ResponseDecisionEngine()
    ctx = DecisionContextDTO(
        risk_score=95.0,
        severity="CRITICAL",
        confidence=0.98,
        action_type="DELETE_RESOURCE",
        target="malicious_dataset.csv",
        legal_hold=True,
    )
    res = engine.evaluate_decision(ctx)
    assert res.decision == "NO_ACTION"
    assert res.policy_basis == "GOVERNANCE_LEGAL_HOLD_BLOCK"
    assert "legal hold" in res.reason.lower()


def test_mission_critical_asset_requires_approval():
    engine = ResponseDecisionEngine()
    ctx = DecisionContextDTO(
        risk_score=90.0,
        severity="CRITICAL",
        confidence=0.95,
        action_type="BLOCK_IP",
        target="198.51.100.5",
        asset_criticality="MISSION_CRITICAL",
    )
    res = engine.evaluate_decision(ctx)
    assert res.decision == "REQUEST_APPROVAL"
    assert res.required_approval is True
    assert res.policy_basis == "MISSION_CRITICAL_ASSET_PROTECTION"


def test_low_risk_action_automated_execution():
    engine = ResponseDecisionEngine()
    ctx = DecisionContextDTO(
        risk_score=45.0,
        severity="MEDIUM",
        confidence=0.85,
        action_type="MARK_INDICATOR",
        target="suspicious-domain.com",
    )
    res = engine.evaluate_decision(ctx)
    assert res.decision == "EXECUTE"
    assert res.required_approval is False


def test_risk_score_banding_decisions():
    engine = ResponseDecisionEngine()

    # < 20: MONITOR
    ctx1 = DecisionContextDTO(risk_score=15.0, action_type="BLOCK_DOMAIN", target="test1.com")
    assert engine.evaluate_decision(ctx1).decision == "MONITOR"

    # 20-40: INVESTIGATE
    ctx2 = DecisionContextDTO(risk_score=35.0, action_type="BLOCK_DOMAIN", target="test2.com")
    assert engine.evaluate_decision(ctx2).decision == "INVESTIGATE"

    # 40-60: ALERT
    ctx3 = DecisionContextDTO(risk_score=50.0, action_type="BLOCK_DOMAIN", target="test3.com")
    assert engine.evaluate_decision(ctx3).decision == "ALERT"

    # 60-80: REQUEST_APPROVAL
    ctx4 = DecisionContextDTO(risk_score=72.0, action_type="BLOCK_DOMAIN", target="test4.com")
    assert engine.evaluate_decision(ctx4).decision == "REQUEST_APPROVAL"
    assert engine.evaluate_decision(ctx4).required_approval is True

    # 80-100: REQUEST_APPROVAL (High confidence)
    ctx5 = DecisionContextDTO(risk_score=95.0, confidence=0.95, action_type="BLOCK_DOMAIN", target="test5.com")
    assert engine.evaluate_decision(ctx5).decision == "REQUEST_APPROVAL"
    assert engine.evaluate_decision(ctx5).required_approval is True
