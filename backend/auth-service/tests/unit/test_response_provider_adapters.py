import pytest
from app.services.soc.response_adapters.extended_adapters import (
    IAMResponseAdapter,
    FraudControlResponseAdapter,
    CloudStorageResponseAdapter,
)
from app.schemas.soc_operations_models import ResponseActionDTO


def test_iam_adapter_account_disable_and_rollback():
    adapter = IAMResponseAdapter()
    act = ResponseActionDTO(
        action_id="act_iam_01",
        incident_id="inc_01",
        action_type="DISABLE_ACCOUNT",
        target="compromised_user_99",
        requested_by="analyst_1",
        reason="Credential theft",
    )

    # 1. Dry run
    dry = adapter.dry_run(act)
    assert dry["status"] == "DRY_RUN_SUCCESS"

    # 2. Execute
    exec_res = adapter.execute(act)
    assert exec_res["status"] == "SUCCESS"
    assert adapter.disabled_accounts.get("compromised_user_99") is True

    # 3. Verify
    status, obs = adapter.verify(act)
    assert status == "SUCCESS"
    assert "DISABLED" in obs

    # 4. Rollback
    rb_success, rb_reason = adapter.rollback(act)
    assert rb_success is True
    assert adapter.disabled_accounts.get("compromised_user_99") is None


def test_fraud_control_upi_freeze():
    adapter = FraudControlResponseAdapter()
    act = ResponseActionDTO(
        action_id="act_fraud_01",
        incident_id="inc_02",
        action_type="FREEZE_UPI_HANDLE",
        target="scam.merchant@okhdfcbank",
        requested_by="fraud_analyst",
        reason="UPI Phishing scam",
    )

    assert adapter.validate_target(act.target, "UPI_VPA") is True
    adapter.execute(act)
    status, obs = adapter.verify(act)
    assert status == "SUCCESS"
    assert "FROZEN" in obs


def test_cloud_storage_bucket_isolation():
    adapter = CloudStorageResponseAdapter()
    act = ResponseActionDTO(
        action_id="act_cloud_01",
        incident_id="inc_03",
        action_type="ISOLATE_S3_BUCKET",
        target="leaked-corporate-data-bucket",
        requested_by="cloud_sec_lead",
        reason="Public data exposure",
    )

    assert adapter.validate_target(act.target, "CLOUD_STORAGE_BUCKET") is True
    adapter.execute(act)
    status, obs = adapter.verify(act)
    assert status == "SUCCESS"
    assert "BlockPublicAccess=True" in obs
