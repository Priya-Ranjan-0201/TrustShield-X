"""Unit tests for Dynamic Class Loader Detection (Phase 3.7 Part 1A.17)."""

import pytest
from app.schemas.reflection_models import DynamicClassDTO


def test_dynamic_class_dto():
    loader = DynamicClassDTO(
        caller_method="com.bank.PluginManager.load",
        loader_type="DexClassLoader",
        dex_path="/sdcard/plugin.apk",
        is_memory_only=False,
    )

    assert loader.caller_method == "com.bank.PluginManager.load"
    assert loader.loader_type == "DexClassLoader"
    assert loader.dex_path == "/sdcard/plugin.apk"
    assert loader.is_memory_only is False
