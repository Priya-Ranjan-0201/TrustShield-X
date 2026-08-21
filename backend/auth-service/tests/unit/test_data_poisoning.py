import pytest
from app.services.ai_governance.dataset_governance_engine import DatasetGovernanceEngine

def test_data_poisoning_detection():
    engine = DatasetGovernanceEngine()
    res = engine.inspect_dataset_integrity("ds_threat_intel_training_v1", has_anomalous_labels=True)
    assert res["status"] == "POTENTIAL_DATA_POISONING"
    assert res["is_clean"] is False
