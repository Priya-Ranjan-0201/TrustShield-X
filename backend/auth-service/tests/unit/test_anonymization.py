import pytest
from app.services.threat_intelligence.collaborative_defense_engine import CollaborativeDefenseEngine


def test_anonymization_of_threat_contributions():
    engine = CollaborativeDefenseEngine()
    contrib = engine.contribute_intelligence(
        tenant_id="tenant_bank",
        contributor="usr_anon_analyst",
        raw_intelligence="Observed IP 203.0.113.55 targeting payment endpoints.",
    )

    assert contrib.is_redacted is True
    assert contrib.content_hash.startswith("sha256_")
