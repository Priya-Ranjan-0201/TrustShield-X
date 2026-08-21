import pytest
from app.services.ai_governance.prompt_security_engine import PromptSecurityEngine

def test_prompt_versioning_tracking():
    engine = PromptSecurityEngine()
    prompts = engine.list_prompts()
    assert len(prompts) >= 1
    assert prompts[0].version == "1.2.0"
