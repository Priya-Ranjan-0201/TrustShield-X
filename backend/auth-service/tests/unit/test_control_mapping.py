import pytest
from app.services.governance_fabric.control_mapping_engine import ControlMappingEngine


def test_control_mapping_traceability():
    engine = ControlMappingEngine()
    mappings = engine.list_mappings("req_soc2_cc6_1")

    assert len(mappings) >= 1
    soc2_map = mappings[0]
    assert soc2_map.control_id == "ctrl_iso_01"
    assert soc2_map.assertion_id == "ast_iso_01"
    assert soc2_map.test_id == "tst_tenant_isolation"
    assert soc2_map.evidence_id == "evi_iso_01"
