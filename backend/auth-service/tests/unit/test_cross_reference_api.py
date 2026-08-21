"""Unit tests for API Cross-References (Phase 3.7 Part 1A.16)."""

import pytest
from app.schemas.api_intelligence_models import APICrossRefDTO


def test_api_cross_ref_dto():
    xref = APICrossRefDTO(source_symbol="com.bank.Net.send", api_canonical_id="okhttp3.OkHttpClient.newCall", xref_type="INVOKE")

    assert xref.source_symbol == "com.bank.Net.send"
    assert xref.api_canonical_id == "okhttp3.OkHttpClient.newCall"
    assert xref.xref_type == "INVOKE"
