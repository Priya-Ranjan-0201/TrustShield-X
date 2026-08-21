import pytest
from app.services.enterprise_governance.third_party_risk_engine import ThirdPartyRiskEngine

def test_vendor_data_access_validation():
    engine = ThirdPartyRiskEngine()
    res = engine.evaluate_vendor_data_access("vnd_cloud_storage_aws", "CONFIDENTIAL_ENCRYPTED")
    assert res["allowed"] is True
    assert res["status"] == "VENDOR_ACCESS_AUTHORIZED"
