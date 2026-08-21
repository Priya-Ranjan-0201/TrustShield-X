import pytest
from app.services.ai_governance.dataset_governance_engine import DatasetGovernanceEngine

def test_dataset_registry_listing():
    engine = DatasetGovernanceEngine()
    datasets = engine.list_datasets()
    assert len(datasets) >= 1
    assert datasets[0].classification == "RESTRICTED"
