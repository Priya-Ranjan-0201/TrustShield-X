"""Unit tests for HTTP Client Detection (Phase 3.8 Part 1A.19)."""

import pytest
from app.schemas.network_models import NetworkLibraryDTO, NetworkOperationDTO


def test_http_detection_dtos():
    lib = NetworkLibraryDTO(
        library_name="OkHttp",
        version="4.11.0",
        detection_evidence="okhttp3.OkHttpClient",
        dex_location="okhttp3",
    )
    op = NetworkOperationDTO(
        caller_method="com.bank.Net.send",
        operation_type="HTTP_REQUEST",
        http_method="POST",
        target_url="https://api.bank.com/v1/data",
    )

    assert lib.library_name == "OkHttp"
    assert op.http_method == "POST"
    assert op.operation_type == "HTTP_REQUEST"
