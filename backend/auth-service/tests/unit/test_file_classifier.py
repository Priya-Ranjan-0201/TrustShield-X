"""Unit tests for File Classifier Engine (Phase 3.7 Part 1A.4)."""

import pytest
from app.services.file_classifier import FileClassifier, FileCategory


def test_classify_android_manifest():
    cat = FileClassifier.classify_file("AndroidManifest.xml")
    assert cat == FileCategory.MANIFEST


def test_classify_dex_file():
    cat = FileClassifier.classify_file("classes2.dex", header_bytes=b"dex\n035\x00")
    assert cat == FileCategory.DEX


def test_classify_native_library():
    cat = FileClassifier.classify_file("lib/arm64-v8a/libcrypto.so", header_bytes=b"\x7fELF\x02\x01\x01\x00")
    assert cat == FileCategory.NATIVE_LIBRARY


def test_classify_certificate():
    cat = FileClassifier.classify_file("META-INF/CERT.RSA")
    assert cat == FileCategory.CERTIFICATE


def test_classify_media_and_data():
    assert FileClassifier.classify_file("res/drawable/icon.png") == FileCategory.IMAGE
    assert FileClassifier.classify_file("assets/data.json") == FileCategory.JSON
    assert FileClassifier.classify_file("res/layout/main.xml") == FileCategory.XML
    assert FileClassifier.classify_file("unknown.xyz") == FileCategory.UNKNOWN
