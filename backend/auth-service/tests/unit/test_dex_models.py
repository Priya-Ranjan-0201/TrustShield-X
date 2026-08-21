"""Unit tests for DEX Intelligence ORM Models & Migration 014 (Phase 3.7 Part 1A.6)."""

import uuid
import pytest
from app.models.apk_dex import (
    APKDexFileModel,
    APKDexClassModel,
    APKDexMethodModel,
    APKDexFieldModel,
    APKPackageModel,
)


def test_apk_dex_models_instantiation():
    scan_id = uuid.uuid4()
    dex_file = APKDexFileModel(
        scan_id=scan_id,
        dex_name="classes.dex",
        dex_order=0,
        sha256="a" * 64,
        sha1="b" * 40,
        checksum="12345678",
        file_size=1000,
    )

    dex_class = APKDexClassModel(
        dex_file_id=dex_file.id,
        class_name="Lcom/example/Test;",
        package_name="com.example",
        superclass="Ljava/lang/Object;",
    )

    dex_method = APKDexMethodModel(
        class_id=dex_class.id,
        method_name="doWork",
        return_type="V",
    )

    dex_field = APKDexFieldModel(
        class_id=dex_class.id,
        field_name="count",
        field_type="I",
    )

    package_model = APKPackageModel(
        scan_id=scan_id,
        package_name="com.example",
        class_count=1,
    )

    assert dex_file.dex_name == "classes.dex"
    assert dex_class.class_name == "Lcom/example/Test;"
    assert dex_method.method_name == "doWork"
    assert dex_field.field_name == "count"
    assert package_model.package_name == "com.example"
