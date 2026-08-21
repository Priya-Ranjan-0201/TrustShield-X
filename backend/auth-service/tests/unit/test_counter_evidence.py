import pytest
from app.services.hunting.hypothesis_challenge_engine import HypothesisChallengeEngine
from app.services.hunting.threat_hunting_fabric import ThreatHuntingFabric


def test_counter_evidence_handling():
    engine = HypothesisChallengeEngine()
    fabric = ThreatHuntingFabric(challenge_engine=engine)

    hyp = fabric.create_hunt_hypothesis("Investigate Subdomain Hijack", "Check DNS", "CAMPAIGN_EXPANSION")

    # Supply strong counter-evidence (e.g. valid internal ownership verification)
    counter_evidence = [
        {"source": "InternalDomainRegistrar", "owner": "Enterprise Core IT", "verified": True},
        {"source": "VerifiedSSLCertificate", "issuer": "Corporate DigiCert Authority", "valid": True},
    ]

    updated_hyp = engine.challenge_hypothesis(
        hypothesis=hyp,
        observed_facts=[],
        known_counter_evidence=counter_evidence,
    )

    # Invariant: Strong counter-evidence refutes hypothesis and lowers confidence
    assert updated_hyp.status in ("REFUTED", "INCONCLUSIVE")
    assert updated_hyp.confidence <= 0.50
