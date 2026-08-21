import pytest
from app.schemas.collective_defense_models import GlobalCampaignDetailDTO
from app.services.collective_defense.global_early_warning_engine import GlobalEarlyWarningEngine


def test_early_warning_trigger_on_expanding_campaign():
    engine = GlobalEarlyWarningEngine()
    camp = GlobalCampaignDetailDTO(
        name="Surging Ransomware Delivery Campaign",
        confidence=0.88,
        modalities=["MALICIOUS_APK", "QR_PHISHING", "NETWORK_INFRASTRUCTURE"],
        indicators=["drop-payload.com", "c2-relay.net", "198.51.100.1"],
        infrastructure_nodes=["drop-payload.com", "c2-relay.net"],
        expansion_warning=True,
    )

    warning = engine.evaluate_campaign_for_warning(camp)
    assert warning is not None
    assert "Surging Ransomware Delivery Campaign" in warning.title
    assert len(warning.recommended_threat_hunts) >= 1
    assert warning.confidence == 0.88
