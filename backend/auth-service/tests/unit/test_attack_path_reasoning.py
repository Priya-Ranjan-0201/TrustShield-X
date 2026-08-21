import pytest
from app.services.hunting.attack_path_reasoning_engine import AttackPathReasoningEngine


def test_attack_path_construction():
    engine = AttackPathReasoningEngine()

    intermediate = [
        {"source": "PublicExposureGateway", "target": "StagingC2", "rel": "EXPOSES", "observed": True, "confidence": 0.95},
    ]

    path = engine.construct_attack_path(
        entry_point="LookalikeDomain",
        target_asset="CustomerAuthDatabase",
        campaign_name="CAMP-FIN-STORM",
        intermediate_nodes=intermediate,
    )

    assert path.path_id.startswith("apg_")
    assert len(path.edges) >= 3
    # Check node classification types
    entry_edge = next(e for e in path.edges if e.node_type == "ENTRY_POINT")
    assert entry_edge.classification == "OBSERVED"
    target_edge = next(e for e in path.edges if e.node_type == "TARGET")
    assert target_edge.classification == "PREDICTED"
