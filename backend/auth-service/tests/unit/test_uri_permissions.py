"""Unit tests for URI Permissions Intelligence (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import UriPermissionDTO


def test_uri_permission_dto():
    uri_perm = UriPermissionDTO(
        caller_method="com.bank.Permission.grant",
        target_package="com.bank.helper",
        uri="content://com.bank.provider/data",
        permission_flags="FLAG_GRANT_READ_URI_PERMISSION",
    )

    assert uri_perm.permission_flags == "FLAG_GRANT_READ_URI_PERMISSION"
