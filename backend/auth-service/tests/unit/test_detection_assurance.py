import pytest
from app.services.assurance.security_slo_engine import SecuritySLOEngine


def test_detection_assurance_slo():
    engine = SecuritySLOEngine()
    slos = engine.list_slos()

    det_slo = next(s for s in slos if s.slo_id == "slo_det_01")
    assert det_slo.target_metric == "DETECTION_ENGINE_AVAILABILITY"
    assert det_slo.actual_percentage >= det_slo.target_percentage
    assert det_slo.status == "MET"
