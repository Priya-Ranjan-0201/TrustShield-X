"""Unit tests for Method Resolver and Basic Blocks (Phase 3.7 Part 1A.15)."""

import pytest
from app.services.program_graph_service import MethodResolver


def test_method_resolver_categories():
    resolver = MethodResolver()

    assert resolver.resolve("android.location.LocationManager", "getLastKnownLocation") == "ANDROID_SDK"
    assert resolver.resolve("java.lang.String", "getBytes") == "JAVA_RUNTIME"
    assert resolver.resolve("com.example.bank.MainActivity", "onCreate") == "INTERNAL"
