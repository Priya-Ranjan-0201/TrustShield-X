import pytest
from app.schemas.collective_defense_models import GlobalCampaignDetailDTO
from app.services.collective_defense.global_early_warning_engine import GlobalEarlyWarningEngine


def test_threat_trend_report_generation():
    engine = GlobalEarlyWarningEngine()
    campaigns = [
        GlobalCampaignDetailDTO(name="Wave 1", modalities=["VOICE_CLONE"], indicators=["ind_1", "ind_2"]),
        GlobalCampaignDetailDTO(name="Wave 2", modalities=["QR_PHISHING"], indicators=["ind_3"]),
    ]

    report = engine.generate_trend_report(campaigns)
    assert report.timeframe == "LAST_30_DAYS"
    assert report.campaign_growth_rate == 2.0
    assert len(report.top_modalities) >= 1
