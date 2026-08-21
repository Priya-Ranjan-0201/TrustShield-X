import pytest
from app.services.fusion.security_priority_engine import SecurityPriorityEngine


def test_attack_path_qualification():
    engine = SecurityPriorityEngine()
    path = engine.construct_attack_path(
        entry_point="fake-hdfc-kyc.com",
        target_asset="corp-auth-gw",
        campaign_name="CAMP-2026-0891",
        intermediate_infra=["198.51.100.44", "cert_sha256_fake"],
    )
    assert len(path.path_nodes) == 5
    # Verify exact qualifications
    assert path.path_nodes[0].status == "OBSERVED_PATH"
    assert path.path_nodes[-1].status == "POTENTIAL_PATH"
