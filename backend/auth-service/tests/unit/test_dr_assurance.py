import pytest
from app.services.assurance.security_slo_engine import SecuritySLOEngine


def test_disaster_recovery_assurance_slo():
    engine = SecuritySLOEngine()
    slos = engine.list_slos()

    bak_slo = next(s for s in slos if s.slo_id == "slo_bak_01")
    assert bak_slo.target_metric == "BACKUP_FRESHNESS_RPO_SLO"
    assert bak_slo.status == "MET"
