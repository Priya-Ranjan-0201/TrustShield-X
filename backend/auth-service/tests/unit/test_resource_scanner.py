"""Unit tests for Resource Inventory Scanner (Phase 3.7 Part 1A Message 2)."""

import pytest
from app.services.resource_scanner import ResourceScanner


def test_resource_scanner_inventory():
    scanner = ResourceScanner()
    entries = [
        ("res/drawable/icon.png", 500, 1200),
        ("res/layout/main.xml", 200, 600),
        ("assets/data.json", 300, 800),
        ("assets/font.ttf", 4000, 8000),
        ("META-INF/MANIFEST.MF", 100, 200),
    ]

    res = scanner.scan_archive_resources(entries)
    assert res.resource_count == 4
    assert res.asset_count == 2
    assert res.image_count == 1
    assert res.xml_count == 1
    assert res.font_count == 1
    assert res.largest_resource_name == "assets/font.ttf"
    assert res.largest_resource_bytes == 8000
    assert res.total_compressed_bytes == 5100
    assert res.total_uncompressed_bytes == 10800
