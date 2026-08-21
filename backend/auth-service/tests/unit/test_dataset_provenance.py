import pytest
from app.services.ai_governance.dataset_governance_engine import DatasetGovernanceEngine

def test_dataset_provenance_tracking():
    engine = DatasetGovernanceEngine()
    ds = engine.list_datasets()[0]
    assert ds.source is not None
    assert "MODEL_TRAINING" in ds.permitted_uses
