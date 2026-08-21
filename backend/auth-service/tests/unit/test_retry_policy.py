import pytest
from app.schemas.autonomous_soc_models import ResponseActionExecutionDTO


def test_retry_policy_count_tracking():
    act = ResponseActionExecutionDTO(
        incident_id="inc_retry",
        target="srv_flaky",
        provider="DNS",
        retries_count=2,
    )

    assert act.retries_count == 2
