import pytest
from app.services.threat_intelligence.campaign_evolution_engine import CampaignEvolutionEngine


def test_campaign_expansion_differentiation():
    engine = CampaignEvolutionEngine()
    evo = engine.record_evolution(
        campaign_id="camp_1",
        new_infrastructure=["domain.bad.net"],
        new_techniques=[],
        new_targets=[],
    )

    assert "domain.bad.net" in evo["observed_changes"]
    assert evo["lifecycle_state"] == "EXPANDING"
