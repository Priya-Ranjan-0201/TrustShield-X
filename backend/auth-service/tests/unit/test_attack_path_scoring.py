import pytest
from app.services.hunting.attack_path_reasoning_engine import AttackPathReasoningEngine


def test_attack_path_confidence_scoring():
    engine = AttackPathReasoningEngine()

    path = engine.construct_attack_path(
        entry_point="PhishSMS",
        target_asset="ExecutiveMailbox",
        campaign_name="CAMP-CEO-FRAUD",
    )

    assert 0.10 <= path.overall_confidence <= 0.99
    assert path.alternative_paths_count >= 1
