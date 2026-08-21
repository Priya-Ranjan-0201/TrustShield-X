"""Deprecation re-export for apk_manifest_full."""

from app.models.apk_manifest import (
    APKManifestModel as APKManifestFullModel,
    APKPermissionFullModel as APKPermissionModel,
    APKActivityModel,
    APKServiceModel,
    APKReceiverModel,
    APKProviderModel,
    APKQueryModel,
)
