"""Unit tests for AndroidManifest Intelligence Parser Engine (Phase 3.7 Part 1A.5 & Part 1A.7)."""

import pytest
from app.services.manifest_parser import ManifestParser, AndroidManifestIntelligenceParser
from app.schemas.manifest_intelligence_models import SDKCategory, ComponentType


SAMPLE_MANIFEST_XML = b"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.trustshield"
    android:versionCode="10"
    android:versionName="1.0.0">

    <uses-sdk android:minSdkVersion="23" android:targetSdkVersion="33" />
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-feature android:name="android.hardware.camera" android:required="true" />

    <queries>
        <package android:name="com.google.android.apps.maps" />
    </queries>

    <application
        android:label="TrustShield"
        android:debuggable="false"
        android:allowBackup="true"
        android:usesCleartextTraffic="false">

        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <service android:name=".MyService" android:exported="false" />
        <receiver android:name=".MyReceiver" android:exported="false" />
        <provider android:name=".MyProvider" android:authorities="com.example.provider" android:exported="false" />
        <uses-library android:name="org.apache.http.legacy" android:required="false" />

    </application>
</manifest>
"""


def test_parse_manifest_xml_success():
    parser = ManifestParser()
    dto = parser.parse_manifest(SAMPLE_MANIFEST_XML)

    assert dto.package_name == "com.example.trustshield"
    assert dto.version_code == 10
    assert dto.min_sdk == 23
    assert dto.target_sdk == 33
    assert dto.sdk_category == SDKCategory.MODERN

    assert len(dto.activities) == 1
    assert dto.activities[0].name == ".MainActivity"
    assert dto.activities[0].exported is True
    assert len(dto.activities[0].intent_filters) == 1
    assert "android.intent.action.MAIN" in dto.activities[0].intent_filters[0].actions

    assert len(dto.services) == 1
    assert len(dto.receivers) == 1
    assert len(dto.providers) == 1
    assert dto.providers[0].authorities == "com.example.provider"

    assert len(dto.permissions) == 2
    assert len(dto.features) == 1
    assert len(dto.libraries) == 1


def test_sdk_category_enum():
    assert AndroidManifestIntelligenceParser.categorize_sdk(19, 19) == SDKCategory.DEPRECATED
    assert AndroidManifestIntelligenceParser.categorize_sdk(21, 22) == SDKCategory.LEGACY
    assert AndroidManifestIntelligenceParser.categorize_sdk(23, 34) == SDKCategory.MODERN
    assert AndroidManifestIntelligenceParser.categorize_sdk(35, 35) == SDKCategory.FUTURE
