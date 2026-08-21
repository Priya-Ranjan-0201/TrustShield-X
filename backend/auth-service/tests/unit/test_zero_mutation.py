import pytest
from app.services.simulation.digital_security_twin_service import DigitalSecurityTwinService


def test_zero_mutation_guarantee():
    service = DigitalSecurityTwinService()

    original_assets = [{"asset_id": "ast_01", "name": "ProductionAuthServer"}]
    twin = service.create_twin_from_snapshot("snap_orig", original_assets)

    # Mutate twin inside simulation
    twin.modeled_assets.append({"asset_id": "ast_sim", "name": "InjectedSimulatedAsset"})

    # Invariant: Original asset input list remains untouched
    assert len(original_assets) == 1
    assert len(twin.modeled_assets) == 2
