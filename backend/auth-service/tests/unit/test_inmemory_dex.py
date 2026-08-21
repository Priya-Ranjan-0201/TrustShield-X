"""Unit tests for InMemoryDexClassLoader and Reflection Metrics (Phase 3.7 Part 1A.17)."""

import pytest
from app.schemas.reflection_models import ReflectionMetricsDTO


def test_reflection_metrics_dto():
    metrics = ReflectionMetricsDTO(
        reflection_calls_count=12,
        dynamic_loaders_count=2,
        native_loads_count=1,
        hidden_apis_count=3,
    )

    assert metrics.reflection_calls_count == 12
    assert metrics.dynamic_loaders_count == 2
    assert metrics.native_loads_count == 1
    assert metrics.hidden_apis_count == 3
