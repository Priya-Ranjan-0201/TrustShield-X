"""Async Component Repository Layer for Android Component Intelligence Engine (Phase 3.7 Part 1A.9).

Provides database operations for persisting and retrieving component_catalog, apk_components_intel,
component_intent_filters_full, component_relationships, and component_processes.
"""

import uuid
from typing import Optional, List
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.apk_component_intel import (
    ComponentCatalogModel,
    APKComponentIntelligenceModel,
    ComponentIntentFilterFullModel,
    ComponentRelationshipModel,
    ComponentProcessModel,
)
from app.schemas.component_intelligence_models import ComponentIntelligenceResultDTO


class ComponentRepository:
    """Async repository for Component Intelligence DB operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_full_component_intelligence(
        self,
        scan_id: uuid.UUID,
        dto: ComponentIntelligenceResultDTO,
    ) -> List[APKComponentIntelligenceModel]:
        """Saves all components, intent filters, relationships, and processes inside one atomic transaction."""
        comp_models: List[APKComponentIntelligenceModel] = []

        for comp in dto.components:
            c_model = APKComponentIntelligenceModel(
                scan_id=scan_id,
                component_name=comp.name,
                component_type=comp.component_type,
                exported_status=comp.exported_status.value if hasattr(comp.exported_status, 'value') else str(comp.exported_status),
                is_enabled=comp.is_enabled,
                permission=comp.permission,
                process_name=comp.process_name,
                is_launcher=comp.is_launcher,
                is_foreground=comp.is_foreground,
            )
            self.db.add(c_model)
            await self.db.flush()

            for if_dto in comp.intent_filters:
                if_model = ComponentIntentFilterFullModel(
                    component_id=c_model.id,
                    actions={"actions": if_dto.actions},
                    categories={"categories": if_dto.categories},
                    schemes={"schemes": if_dto.schemes},
                    hosts={"hosts": if_dto.hosts},
                    ports={"ports": if_dto.ports},
                    paths={"paths": if_dto.paths},
                    mime_types={"mime_types": if_dto.mime_types},
                    priority=if_dto.priority,
                    auto_verify=if_dto.auto_verify,
                    is_deep_link=if_dto.is_deep_link,
                )
                self.db.add(if_model)

            comp_models.append(c_model)

        # Process Relationships
        rel_models = [
            ComponentRelationshipModel(
                scan_id=scan_id,
                parent_component=r.parent_component,
                child_component=r.child_component,
                relationship_type=r.relationship_type,
            )
            for r in dto.relationships
        ]
        if rel_models:
            self.db.add_all(rel_models)

        # Processes
        proc_models = [
            ComponentProcessModel(
                scan_id=scan_id,
                process_name=p.process_name,
                process_type=p.process_type.value if hasattr(p.process_type, 'value') else str(p.process_type),
                component_count=p.component_count,
            )
            for p in dto.processes
        ]
        if proc_models:
            self.db.add_all(proc_models)

        await self.db.commit()
        return comp_models

    async def get_components(self, scan_id: uuid.UUID) -> List[APKComponentIntelligenceModel]:
        stmt = (
            select(APKComponentIntelligenceModel)
            .where(APKComponentIntelligenceModel.scan_id == scan_id)
            .options(selectinload(APKComponentIntelligenceModel.intent_filters))
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def delete_components(self, scan_id: uuid.UUID) -> bool:
        comps = await self.get_components(scan_id)
        if not comps:
            return False

        for c in comps:
            await self.db.delete(c)
        await self.db.commit()
        return True
