"""Unit tests for MethodHandles and Dynamic Invocations (Phase 3.7 Part 1A.17)."""

import pytest
from app.schemas.reflection_models import DynamicInvocationDTO


def test_dynamic_invocation_dto():
    inv = DynamicInvocationDTO(source_symbol="com.bank.Handler.dispatch", resolved_target="com.bank.Handler.processAction", confidence=0.95)

    assert inv.source_symbol == "com.bank.Handler.dispatch"
    assert inv.resolved_target == "com.bank.Handler.processAction"
    assert inv.confidence == 0.95
