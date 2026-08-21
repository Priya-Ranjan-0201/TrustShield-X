import pytest
from app.services.exposure.change_detection_engine import ChangeDetectionEngine
from app.schemas.exposure_models import AssetBaselineDTO, AssetObservationDTO


def test_change_detection_and_classification():
    engine = ChangeDetectionEngine()

    baseline = AssetBaselineDTO(
        baseline_id="base_01",
        asset_id="ast_202",
        tenant_id="tenant_chg",
        exposed_ports=[80, 443],
        dns_records={"A": ["198.51.100.40"]},
    )

    # Observation with newly exposed RDP port (3389)
    obs = AssetObservationDTO(
        observation_id="obs_01",
        asset_id="ast_202",
        tenant_id="tenant_chg",
        source_type="PASSIVE",
        source_name="SHODAN_PASSIVE_FEED",
        observed_data={
            "exposed_ports": [80, 443, 3389],
            "dns_records": {"A": ["198.51.100.40"]},
        },
        confidence=0.96,
    )

    changes = engine.evaluate_observation(obs, baseline)
    assert len(changes) == 1
    assert changes[0].change_type == "NEW_EXPOSED_PORTS_DETECTED"
    assert changes[0].classification == "HIGH_RISK"
    assert 3389 in changes[0].new_state["newly_opened"]
