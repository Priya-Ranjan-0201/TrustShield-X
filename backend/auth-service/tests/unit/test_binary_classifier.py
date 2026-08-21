"""Unit tests for Binary File Classification (Phase 3.7 Part 1A.12)."""

import pytest
from app.services.apk_binary_inventory import APKBinaryInventoryService
from app.schemas.apk_binary_inventory_models import FileCategoryEnum


def test_classify_file_categories():
    service = APKBinaryInventoryService()

    assert service.classify_file("classes.dex") == FileCategoryEnum.DEX
    assert service.classify_file("classes2.dex") == FileCategoryEnum.DEX
    assert service.classify_file("lib/arm64-v8a/libfoo.so") == FileCategoryEnum.NATIVE_LIBRARY
    assert service.classify_file("META-INF/CERT.RSA") == FileCategoryEnum.CERTIFICATE
    assert service.classify_file("AndroidManifest.xml") == FileCategoryEnum.MANIFEST
    assert service.classify_file("assets/model.tflite") == FileCategoryEnum.ML_MODEL
    assert service.classify_file("res/layout/main.xml") == FileCategoryEnum.XML
    assert service.classify_file("res/drawable/bg.png") == FileCategoryEnum.IMAGE
    assert service.classify_file("assets/script.js") == FileCategoryEnum.JAVASCRIPT
