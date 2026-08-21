"""Unit tests for Inventory Builder & Entropy Engine (Phase 3.7 Part 1A.4)."""

import os
import pytest
from app.services.apk_inventory_builder import APKInventoryBuilder


def test_calculate_shannon_entropy(tmp_path):
    # Low entropy file (repeated zeroes)
    zero_file = tmp_path / "zeroes.bin"
    zero_file.write_bytes(b"\x00" * 1000)

    # High entropy file (pseudo-random bytes)
    random_bytes = bytes([i % 256 for i in range(1000)])
    rand_file = tmp_path / "random.bin"
    rand_file.write_bytes(random_bytes)

    low_ent = APKInventoryBuilder.calculate_shannon_entropy(str(zero_file))
    high_ent = APKInventoryBuilder.calculate_shannon_entropy(str(rand_file))

    assert low_ent == 0.0
    assert high_ent > 7.0


def test_build_inventory(tmp_path):
    (tmp_path / "AndroidManifest.xml").write_bytes(b"<manifest></manifest>")
    (tmp_path / "classes.dex").write_bytes(b"dex\n035\x00" + b"\x00" * 20)

    builder = APKInventoryBuilder()
    inv = builder.build_inventory(str(tmp_path))

    assert inv.total_files == 2
    assert os.path.exists(tmp_path / "inventory.json")
