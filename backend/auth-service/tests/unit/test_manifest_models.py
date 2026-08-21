"""Unit tests for Manifest Intelligence ORM Models & Migration 015 (Phase 3.7 Part 1A.7)."""

import uuid
import pytest
from app.models.apk_manifest import (
    APKManifestModel,
    APKComponentModel,
    APKIntentFilterModel,
    APKFeatureModel,
    APKLibraryModel,
)
from app.models.apk_manifest_full import (
    APKManifestFullModel,
    APKPermissionModel as APKGranularPermissionModel,
    APKActivityModel,
    APKServiceModel,
    APKReceiverModel,
    APKProviderModel,
    APKQueryModel,
)


def test_apk_manifest_models_instantiation():
    scan_id = uuid.uuid4()
    manifest = APKManifestModel(
        scan_id=scan_id,
        package_name="com.example.test",
        version_name="1.0.0",
        version_code=1,
        min_sdk=23,
        target_sdk=33,
        sdk_category="MODERN",
    )

    comp = APKComponentModel(
        manifest_id=manifest.id,
        component_name=".MainActivity",
        component_type="ACTIVITY",
        exported=True,
    )

    ifilter = APKIntentFilterModel(
        component_id=comp.id,
        actions={"actions": ["android.intent.action.MAIN"]},
    )

    feat = APKFeatureModel(
        manifest_id=manifest.id,
        feature_name="android.hardware.camera",
        required=True,
    )

    lib = APKLibraryModel(
        manifest_id=manifest.id,
        library_name="org.apache.http.legacy",
        required=False,
    )

    activity = APKActivityModel(
        manifest_id=manifest.id,
        activity_name=".MainActivity",
        exported=True,
    )

    service = APKServiceModel(
        manifest_id=manifest.id,
        service_name=".MyService",
        exported=False,
    )

    query = APKQueryModel(
        manifest_id=manifest.id,
        query_type="package",
        target="com.google.android.apps.maps",
    )

    assert manifest.package_name == "com.example.test"
    assert comp.component_name == ".MainActivity"
    assert ifilter.actions["actions"] == ["android.intent.action.MAIN"]
    assert feat.feature_name == "android.hardware.camera"
    assert lib.library_name == "org.apache.http.legacy"
    assert activity.activity_name == ".MainActivity"
    assert service.service_name == ".MyService"
    assert query.target == "com.google.android.apps.maps"
