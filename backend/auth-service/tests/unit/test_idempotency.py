import pytest
from app.schemas.autonomous_soc_models import ResponseActionExecutionDTO


def test_response_action_idempotency_key():
    act1 = ResponseActionExecutionDTO(incident_id="inc_1", target="srv_1", provider="WAF")
    act2 = ResponseActionExecutionDTO(incident_id="inc_1", target="srv_1", provider="WAF")

    assert act1.idempotency_key.startswith("idemp_")
    assert act2.idempotency_key.startswith("idemp_")
    assert act1.idempotency_key != act2.idempotency_key
