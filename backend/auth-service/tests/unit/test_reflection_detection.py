"""Unit tests for Java Reflection Detection (Phase 3.7 Part 1A.17)."""

import pytest
from app.schemas.reflection_models import ReflectionCallDTO


def test_reflection_call_dto():
    call = ReflectionCallDTO(
        caller_method="com.bank.Auth.login",
        reflection_api="java.lang.Class.forName",
        target_class="com.bank.SecretService",
        target_member="execute",
        offset=16,
    )

    assert call.caller_method == "com.bank.Auth.login"
    assert call.reflection_api == "java.lang.Class.forName"
    assert call.target_class == "com.bank.SecretService"
    assert call.target_member == "execute"
    assert call.offset == 16
