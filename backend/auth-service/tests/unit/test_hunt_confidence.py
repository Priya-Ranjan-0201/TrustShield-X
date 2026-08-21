import pytest
from app.services.hunting.hypothesis_challenge_engine import HypothesisChallengeEngine
from app.services.hunting.threat_hunting_fabric import ThreatHuntingFabric


def test_calibrated_confidence_calculation():
    engine = HypothesisChallengeEngine()
    fabric = ThreatHuntingFabric(challenge_engine=engine)

    hyp = fabric.create_hunt_hypothesis("C2 Staging Infrastructure Check", "Desc", "MALWARE_CAMPAIGN")

    # 1. 3 strong supporting facts -> High confidence
    observed_facts = [
        {"indicator": "c2_ip_1", "confidence": 0.95},
        {"indicator": "c2_ip_2", "confidence": 0.90},
        {"indicator": "c2_ip_3", "confidence": 0.88},
    ]

    res = engine.challenge_hypothesis(hyp, observed_facts=observed_facts)
    assert res.confidence >= 0.80
    assert res.conclusion == "THREAT_CONFIRMED"
