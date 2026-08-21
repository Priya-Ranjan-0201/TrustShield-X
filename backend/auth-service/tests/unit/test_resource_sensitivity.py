import pytest
from app.services.zero_trust_exposure.data_classification_engine import DataClassificationEngine

def test_resource_classification_and_dlp_egress():
    engine = DataClassificationEngine()
    res = engine.classify_resource("RES-SECRET-DB", "t1", "RESTRICTED", contains_credentials=True)
    assert res["classification_level"] == "RESTRICTED"
    
    # DLP block on secret exfiltration
    leak_check = engine.inspect_egress_data("t1", "AKIAIOSFODNN7EXAMPLE", "EXTERNAL_IP")
    assert leak_check["decision"] == "DENY"
    assert "CREDENTIAL_EXFILTRATION_DETECTED" in leak_check["findings"]
