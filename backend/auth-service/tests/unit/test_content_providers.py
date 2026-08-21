"""Unit tests for Content Provider Intelligence (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import ContentProviderDTO, ContentProviderOperationDTO


def test_content_provider_dtos():
    cp = ContentProviderDTO(
        authority="com.bank.provider",
        provider_class="com.bank.DataProvider",
        is_exported=True,
        read_permission="com.bank.permission.READ",
    )
    cpop = ContentProviderOperationDTO(
        caller_method="com.bank.Client.query",
        authority="com.bank.provider",
        uri="content://com.bank.provider/accounts",
        operation="QUERY",
    )

    assert cp.is_exported is True
    assert cpop.operation == "QUERY"
