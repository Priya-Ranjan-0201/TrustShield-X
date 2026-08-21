import pytest
from app.services.fusion.incident_command_engine import IncidentCommandEngine


def test_security_kpis_calculation():
    engine = IncidentCommandEngine()
    engine.create_incident_command("INC-03", "commander", "HIGH", tenant_id="tenant_kpi")

    kpis = engine.calculate_kpis("tenant_kpi")
    assert kpis.mttd_minutes > 0.0
    assert kpis.mtti_minutes > 0.0
    assert kpis.mttc_minutes > 0.0
    assert kpis.response_success_rate >= 0.90
    assert kpis.active_incidents == 1
