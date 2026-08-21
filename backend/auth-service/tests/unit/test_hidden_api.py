"""Unit tests for Hidden Android API Resolution (Phase 3.7 Part 1A.17)."""

import pytest
from app.schemas.reflection_models import HiddenAPIDTO


def test_hidden_api_dto():
    hapi = HiddenAPIDTO(
        api_signature="android.os.SystemProperties.get",
        access_mechanism="REFLECTION",
        restriction_level="GREYLIST",
    )

    assert hapi.api_signature == "android.os.SystemProperties.get"
    assert hapi.access_mechanism == "REFLECTION"
    assert hapi.restriction_level == "GREYLIST"
