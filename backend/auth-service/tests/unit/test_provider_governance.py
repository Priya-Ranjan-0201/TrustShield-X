import pytest
from app.services.ai_governance.ai_provider_governance_engine import AIProviderGovernanceEngine

def test_provider_governance_listing():
    engine = AIProviderGovernanceEngine()
    providers = engine.list_providers()
    assert len(providers) >= 1
    assert providers[0].retention_policy == "ZERO_RETENTION_EPHEMERAL"
