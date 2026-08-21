import pytest
from app.services.governance_fabric.control_mapping_engine import ControlMappingEngine


def test_control_objectives_mapping():
    engine = ControlMappingEngine()

    new_map = engine.map_requirement_to_control(
        requirement_id="req_custom_01",
        control_id="ctrl_waf_01",
        assertion_id="ast_waf_01",
        test_id="tst_waf_01",
        evidence_id="evi_waf_01",
    )

    assert new_map.mapping_id.startswith("map_")
    assert new_map.requirement_id == "req_custom_01"
    assert new_map.confidence_weight == 1.0
