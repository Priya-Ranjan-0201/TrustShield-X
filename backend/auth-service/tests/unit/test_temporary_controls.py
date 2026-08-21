import pytest
from app.services.adaptive_defense.adaptive_defense_fabric import AdaptiveDefenseFabric


def test_time_bounded_temporary_controls():
    fabric = AdaptiveDefenseFabric()
    rec = fabric.create_recommendation(
        tenant_id="tenant_temp",
        title="Temporary 60-minute egress block for investigation",
        action_classification="NETWORK_CONTROL",
        target_resource="198.51.100.77",
        duration_minutes=60,
    )

    assert rec.is_time_bounded is True
    assert rec.duration_minutes == 60
