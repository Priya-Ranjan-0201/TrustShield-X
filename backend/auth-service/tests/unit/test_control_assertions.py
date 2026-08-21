import pytest
from app.schemas.assurance_models import ControlAssertionDTO


def test_control_assertions():
    assertion = ControlAssertionDTO(
        assertion_id="ast_iso_01",
        control_id="ctrl_iso_01",
        expression="Tenant A cannot read Tenant B documents",
        severity="CRITICAL",
        verification_method="SYNTHETIC_CROSS_TENANT_QUERY",
        expected_result="EMPTY_RESULT_SET_WITH_DENIAL",
        frequency="HOURLY",
    )

    assert assertion.last_evaluated_state == "SATISFIED"
    assert assertion.severity == "CRITICAL"
