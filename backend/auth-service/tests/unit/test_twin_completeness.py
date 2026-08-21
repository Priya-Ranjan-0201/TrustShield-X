import pytest
from app.services.resilience_twin.twin_completeness_engine import TwinCompletenessEngine


def test_twin_completeness_eight_dimensions():
    engine = TwinCompletenessEngine()
    comp = engine.calculate_completeness(
        tenant_id="tenant_x",
        asset_vis=90.0,
        ident_vis=85.0,
        serv_vis=95.0,
        dep_vis=80.0,
        ctrl_vis=92.0,
        threat_vis=88.0,
        biz_map=75.0,
        rec_map=80.0,
    )

    assert comp.asset_visibility == 90.0
    assert comp.business_mapping == 75.0
    assert 80.0 <= comp.overall_completeness <= 90.0
