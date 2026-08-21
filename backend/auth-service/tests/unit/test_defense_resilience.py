import pytest
from app.services.adaptive_defense.adaptive_defense_fabric import AdaptiveDefenseFabric


def test_defense_resilience_on_invalid_recommendation():
    fabric = AdaptiveDefenseFabric()
    with pytest.raises(ValueError):
        fabric.execute_closed_loop_defense("non_existent_rec_id")
