"""Unit tests for Cache Intelligence (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import CacheLocationDTO


def test_cache_location_dto():
    cache = CacheLocationDTO(
        caller_method="com.bank.Cache.init",
        cache_type="DISK_CACHE",
        path="/data/data/com.bank/cache/http_cache",
        eviction_policy="LRU",
    )

    assert cache.cache_type == "DISK_CACHE"
    assert cache.eviction_policy == "LRU"
