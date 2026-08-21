import pytest
import time
from app.services.copilot.security_copilot_service import SecurityCopilot


def test_copilot_low_latency_response():
    copilot = SecurityCopilot()

    start = time.perf_counter()
    res = copilot.process_chat_message("sess_perf", "Explain CVE-2026-9942 risk")
    elapsed = time.perf_counter() - start

    assert elapsed < 0.2  # < 200ms
    assert res.confidence > 0.85
