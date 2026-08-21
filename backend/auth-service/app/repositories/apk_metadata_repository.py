"""Async APK Metadata Repository Layer for Package Intelligence Engine (Phase 3.7 Part 1A.11).

Provides database operations for persisting and retrieving apk_metadata_intel,
apk_versions, apk_sdk_profiles, apk_application_flags, and apk_resources_intel.
"""

import uuid
from typing import Optional, List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.apk_metadata_intel import (
    APKMetadataFullModel,
    APKVersionModel,
    SDKProfileModel,
    ApplicationFlagsModel,
    APKResourceModel,
)
from app.schemas.apk_metadata_intelligence_models import APKMetadataIntelligenceResultDTO


class APKMetadataRepository:
    """Async repository for APK Metadata & Package Intelligence DB operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_full_metadata_intelligence(
        self,
        scan_id: uuid.UUID,
        dto: APKMetadataIntelligenceResultDTO,
    ) -> APKMetadataFullModel:
        """Saves package metadata root, versions, SDK profiles, application flags, and resources inside one atomic transaction."""
        root_m = APKMetadataFullModel(
            scan_id=scan_id,
            package_name=dto.package_name,
            app_label=dto.resources.app_label,
            app_class=dto.resources.app_class,
            version_name=dto.version_info.version_name,
            version_code=dto.version_info.version_code,
            target_sdk=dto.sdk_profile.target_sdk,
            min_sdk=dto.sdk_profile.min_sdk,
            compile_sdk=dto.sdk_profile.compile_sdk,
            install_location=dto.install_location.value if hasattr(dto.install_location, 'value') else str(dto.install_location),
        )
        self.db.add(root_m)

        v_m = APKVersionModel(
            scan_id=scan_id,
            version_name=dto.version_info.version_name,
            version_code=dto.version_info.version_code,
            major=dto.version_info.major,
            minor=dto.version_info.minor,
            patch=dto.version_info.patch,
            build=dto.version_info.build,
        )
        self.db.add(v_m)

        sdk_m = SDKProfileModel(
            scan_id=scan_id,
            min_sdk=dto.sdk_profile.min_sdk,
            target_sdk=dto.sdk_profile.target_sdk,
            compile_sdk=dto.sdk_profile.compile_sdk,
            max_sdk=dto.sdk_profile.max_sdk,
            platform_version=dto.sdk_profile.platform_version,
            generation_name=dto.sdk_profile.generation_name,
        )
        self.db.add(sdk_m)

        flags_m = ApplicationFlagsModel(
            scan_id=scan_id,
            is_debuggable=dto.app_flags.is_debuggable,
            is_persistent=dto.app_flags.is_persistent,
            is_test_only=dto.app_flags.is_test_only,
            allow_backup=dto.app_flags.allow_backup,
            large_heap=dto.app_flags.large_heap,
            uses_cleartext=dto.app_flags.uses_cleartext,
            supports_rtl=dto.app_flags.supports_rtl,
        )
        self.db.add(flags_m)

        res_m = APKResourceModel(
            scan_id=scan_id,
            icon_ref=dto.resources.icon_ref,
            round_icon_ref=dto.resources.round_icon_ref,
            banner_ref=dto.resources.banner_ref,
            logo_ref=dto.resources.logo_ref,
            theme_ref=dto.resources.theme_ref,
        )
        self.db.add(res_m)

        await self.db.commit()
        return root_m

    async def get_metadata(self, scan_id: uuid.UUID) -> Optional[APKMetadataFullModel]:
        stmt = select(APKMetadataFullModel).where(APKMetadataFullModel.scan_id == scan_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()
