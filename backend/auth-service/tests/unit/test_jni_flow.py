"""Unit tests for JNI Native Dataflow (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import JNIDataflowDTO


def test_jni_flow_dto():
    j = JNIDataflowDTO(
        java_method="com.bank.NativeBridge.process",
        native_symbol="Java_com_bank_NativeBridge_process",
        library_name="libnative.so",
        direction="JAVA_TO_NATIVE",
    )

    assert j.library_name == "libnative.so"
    assert j.direction == "JAVA_TO_NATIVE"
