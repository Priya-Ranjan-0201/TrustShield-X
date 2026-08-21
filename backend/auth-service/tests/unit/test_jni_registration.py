"""Unit tests for JNI Registration & Native Loading (Phase 3.7 Part 1A.17)."""

import pytest
from app.schemas.reflection_models import JNIBindingDTO, NativeLoadingDTO


def test_jni_and_native_dtos():
    jni = JNIBindingDTO(native_method="decryptPayload", java_class="com.bank.NativeBridge", symbol_name="Java_com_bank_NativeBridge_decryptPayload")
    nl = NativeLoadingDTO(caller_method="com.bank.NativeBridge.init", library_name="crypto-native", load_api="System.loadLibrary")

    assert jni.native_method == "decryptPayload"
    assert jni.java_class == "com.bank.NativeBridge"
    assert nl.library_name == "crypto-native"
    assert nl.load_api == "System.loadLibrary"
