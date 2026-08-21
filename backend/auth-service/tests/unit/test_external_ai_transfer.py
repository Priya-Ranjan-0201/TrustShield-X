import pytest
from app.services.ai_governance.ai_provider_governance_engine import AIProviderGovernanceEngine

def test_external_ai_transfer_blocks_confidential():
    engine = AIProviderGovernanceEngine()
    res = engine.validate_external_transfer("prv_internal_enclave", "CONFIDENTIAL", is_explicitly_authorized=False)
    assert res["allowed"] is False
    assert res["status"] == "EXTERNAL_TRANSFER_BLOCKED"
