"""Production AndroidManifest Intelligence Parser Engine (Phase 3.7 Part 1A.7).

Decodes binary AndroidManifest.xml and plain XML files, extracting package attributes,
SDK levels, Activities, Services, Broadcast Receivers, Content Providers, Intent Filters,
Query declarations (<queries>), Hardware/Software Features, Libraries, and Permissions.

Zero security risk scoring, permission vulnerability analysis, or code execution.
"""

from typing import List, Dict, Any, Optional
from app.schemas.manifest_intelligence_models import (
    ManifestIntelligenceDTO,
    ComponentDTO,
    ComponentType,
    IntentFilterDTO,
    FeatureDTO,
    LibraryDTO,
    PermissionRefDTO,
    QueryDTO,
    SDKCategory,
)
from app.services.android_manifest_parser import AndroidManifestIntelligenceParser


class ManifestParser:
    """Master AndroidManifest.xml Intelligence Parser."""

    def __init__(self):
        self._inner_parser = AndroidManifestIntelligenceParser()

    def parse_manifest(
        self,
        manifest_data: Any,
    ) -> ManifestIntelligenceDTO:
        """Parses AndroidManifest from androguard APK/AXML object or raw XML bytes."""
        return self._inner_parser.parse_manifest(manifest_data)

    def parse_manifest_bytes(
        self,
        manifest_bytes: bytes,
        androguard_apk: Any = None,
    ):
        """Backward compatible helper for APKParser."""
        if androguard_apk is not None:
            return self._inner_parser.parse_manifest(androguard_apk)
        return self._inner_parser.parse_manifest(manifest_bytes)


# Backward Compatibility Alias
AndroidManifestParser = ManifestParser
