"""Async Manifest Repository Layer for AndroidManifest Intelligence Engine (Phase 3.7 Part 1A.5 & Part 1A.7).

Provides database operations for persisting and retrieving apk_manifest, apk_permissions,
apk_activities, apk_services, apk_receivers, apk_providers, apk_intent_filters,
apk_features, apk_libraries, and apk_queries.
"""

import uuid
from typing import Optional, List, Any
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.apk_manifest import (
    APKManifestModel,
    APKComponentModel,
    APKIntentFilterModel,
    APKFeatureModel,
    APKLibraryModel,
    APKPermissionFullModel as APKGranularPermissionModel,
    APKActivityModel,
    APKServiceModel,
    APKReceiverModel,
    APKProviderModel,
    APKQueryModel,
)
from app.schemas.manifest_intelligence_models import ManifestIntelligenceDTO


class ManifestRepository:
    """Async repository for Manifest Intelligence DB operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_manifest(
        self,
        scan_id: uuid.UUID,
        dto: ManifestIntelligenceDTO,
    ) -> APKManifestModel:
        manifest_model = APKManifestModel(
            scan_id=scan_id,
            package_name=dto.package_name,
            version_name=dto.version_name,
            version_code=dto.version_code,
            min_sdk=dto.min_sdk,
            target_sdk=dto.target_sdk,
            compile_sdk=dto.compile_sdk,
            sdk_category=dto.sdk_category.value if hasattr(dto.sdk_category, 'value') else str(dto.sdk_category),
            shared_user_id=dto.shared_user_id,
            application_label=dto.application_label,
            debuggable=dto.debuggable,
            allow_backup=dto.allow_backup,
            uses_cleartext_traffic=dto.uses_cleartext_traffic,
        )
        self.db.add(manifest_model)
        await self.db.flush()
        return manifest_model

    async def store_permissions(self, manifest_id: uuid.UUID, permissions: List[Any]) -> None:
        models = [
            APKGranularPermissionModel(
                manifest_id=manifest_id,
                permission_name=p.name,
                protection_level=p.protection_level,
                declared=p.declared,
                requested=p.requested,
                is_custom=p.is_custom,
            )
            for p in permissions
        ]
        if models:
            self.db.add_all(models)

    async def store_activities(self, manifest_id: uuid.UUID, activities: List[Any]) -> None:
        models = [
            APKActivityModel(
                manifest_id=manifest_id,
                activity_name=a.name,
                exported=a.exported,
                enabled=a.enabled,
                permission=a.permission,
                launch_mode=a.launch_mode,
                task_affinity=a.task_affinity,
                theme=a.theme,
            )
            for a in activities
        ]
        if models:
            self.db.add_all(models)

    async def store_services(self, manifest_id: uuid.UUID, services: List[Any]) -> None:
        models = [
            APKServiceModel(
                manifest_id=manifest_id,
                service_name=s.name,
                exported=s.exported,
                enabled=s.enabled,
                permission=s.permission,
                foreground_service_type=s.foreground_service_type,
            )
            for s in services
        ]
        if models:
            self.db.add_all(models)

    async def store_receivers(self, manifest_id: uuid.UUID, receivers: List[Any]) -> None:
        models = [
            APKReceiverModel(
                manifest_id=manifest_id,
                receiver_name=r.name,
                exported=r.exported,
                enabled=r.enabled,
                permission=r.permission,
            )
            for r in receivers
        ]
        if models:
            self.db.add_all(models)

    async def store_providers(self, manifest_id: uuid.UUID, providers: List[Any]) -> None:
        models = [
            APKProviderModel(
                manifest_id=manifest_id,
                provider_name=p.name,
                authorities=p.authorities,
                exported=p.exported,
                enabled=p.enabled,
                grant_uri_permissions=p.grant_uri_permissions,
                read_permission=p.read_permission,
                write_permission=p.write_permission,
            )
            for p in providers
        ]
        if models:
            self.db.add_all(models)

    async def store_queries(self, manifest_id: uuid.UUID, queries: List[Any]) -> None:
        models = [
            APKQueryModel(
                manifest_id=manifest_id,
                query_type=q.query_type,
                target=q.target,
            )
            for q in queries
        ]
        if models:
            self.db.add_all(models)

    async def save_full_manifest(
        self,
        scan_id: uuid.UUID,
        dto: ManifestIntelligenceDTO,
    ) -> APKManifestModel:
        """Saves manifest root, components, intent filters, features, libraries, queries inside one atomic transaction."""
        manifest_model = await self.create_manifest(scan_id, dto)

        # Process Components & Intent Filters
        all_components = dto.activities + dto.services + dto.receivers + dto.providers
        for comp in all_components:
            comp_model = APKComponentModel(
                manifest_id=manifest_model.id,
                component_name=comp.name,
                component_type=comp.component_type.value if hasattr(comp.component_type, 'value') else str(comp.component_type),
                exported=comp.exported,
                enabled=comp.enabled,
                permission=comp.permission,
                process=comp.process,
                launch_mode=comp.launch_mode,
                authorities=comp.authorities,
            )
            self.db.add(comp_model)
            await self.db.flush()

            for if_dto in comp.intent_filters:
                if_model = APKIntentFilterModel(
                    component_id=comp_model.id,
                    actions={"actions": if_dto.actions},
                    categories={"categories": if_dto.categories},
                    schemes={"schemes": if_dto.schemes},
                    hosts={"hosts": if_dto.hosts},
                    mime_types={"mime_types": if_dto.mime_types},
                    priority=if_dto.priority,
                )
                self.db.add(if_model)

        # Granular Component & Query Persistence
        await self.store_permissions(manifest_model.id, dto.permissions)
        await self.store_activities(manifest_model.id, dto.activities)
        await self.store_services(manifest_model.id, dto.services)
        await self.store_receivers(manifest_model.id, dto.receivers)
        await self.store_providers(manifest_model.id, dto.providers)
        await self.store_queries(manifest_model.id, dto.queries)

        # Process Features
        feature_models = [
            APKFeatureModel(
                manifest_id=manifest_model.id,
                feature_name=f.name,
                required=f.required,
                gl_version=f.gl_version,
            )
            for f in dto.features
        ]
        if feature_models:
            self.db.add_all(feature_models)

        # Process Libraries
        library_models = [
            APKLibraryModel(
                manifest_id=manifest_model.id,
                library_name=l.name,
                required=l.required,
            )
            for l in dto.libraries
        ]
        if library_models:
            self.db.add_all(library_models)

        await self.db.commit()
        return manifest_model

    async def get_manifest(self, scan_id: uuid.UUID) -> Optional[APKManifestModel]:
        stmt = (
            select(APKManifestModel)
            .where(APKManifestModel.scan_id == scan_id)
            .options(
                selectinload(APKManifestModel.components).selectinload(APKComponentModel.intent_filters),
                selectinload(APKManifestModel.features),
                selectinload(APKManifestModel.libraries),
            )
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def delete_manifest(self, scan_id: uuid.UUID) -> bool:
        manifest = await self.get_manifest(scan_id)
        if not manifest:
            return False

        await self.db.delete(manifest)
        await self.db.commit()
        return True
