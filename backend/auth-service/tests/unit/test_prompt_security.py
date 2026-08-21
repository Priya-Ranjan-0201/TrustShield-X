import pytest
from app.services.ai_governance.prompt_security_engine import PromptSecurityEngine

def test_clean_prompt_passed():
    engine = PromptSecurityEngine()
    res = engine.inspect_prompt_input("Summarize the recent DarkStorm campaign telemetry.")
    assert res["is_safe"] is True
    assert res["status"] == "CLEAN"
