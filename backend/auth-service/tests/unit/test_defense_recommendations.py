import pytest
from app.services.adaptive_defense.adaptive_defense_fabric import AdaptiveDefenseFabric


def test_defense_recommendation_creation():
    fabric = AdaptiveDefenseFabric()
    rec = fabric.create_recommendation(
        tenant_id="tenant_bank",
        title="Quarantine compromised workstation ep-user-01",
        action_classification="ASSET_ISOLATION",
        target_resource="ep-user-01",
        automation_level="LEVEL_2_HUMAN_APPROVAL",
        evidence_references=["ev_malware_c2_beacon", "ev_credential_dump"],
    )

    assert rec.recommendation_id.startswith("rec_")
    assert rec.action_classification == "ASSET_ISOLATION"
    assert rec.automation_level == "LEVEL_2_HUMAN_APPROVAL"
    assert len(rec.evidence_references) == 2
