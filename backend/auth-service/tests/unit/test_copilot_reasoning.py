import pytest
from app.services.copilot.security_copilot_service import SecurityCopilot


def test_copilot_reasoning_trace_epistemic_status():
    copilot = SecurityCopilot()
    res = copilot.process_chat_message("sess_4", "Is checkout service at risk from Shadow Hydra?")

    assert res.epistemic_status == "INFERRED"
    assert res.confidence > 0.85
    assert len(res.sources) >= 2
