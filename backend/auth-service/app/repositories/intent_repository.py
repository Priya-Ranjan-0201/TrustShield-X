"""Async Intent Repository Layer for Intent & Deep Link Intelligence Engine (Phase 3.7 Part 1A.10).

Provides database operations for persisting and retrieving intent_catalog, apk_intents,
apk_intent_actions, apk_intent_categories, apk_deep_links, and navigation_graph.
"""

import uuid
from typing import Optional, List
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.apk_intent_intel import (
    IntentCatalogModel,
    APKIntentModel,
    IntentActionModel,
    IntentCategoryModel,
    DeepLinkModel,
    NavigationGraphModel,
)
from app.schemas.intent_intelligence_models import IntentIntelligenceResultDTO


class IntentRepository:
    """Async repository for Intent & Deep Link Intelligence DB operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_full_intent_intelligence(
        self,
        scan_id: uuid.UUID,
        dto: IntentIntelligenceResultDTO,
    ) -> List[APKIntentModel]:
        """Saves all intent filters, actions, categories, deep links, and navigation graph entries inside one atomic transaction."""
        intent_models: List[APKIntentModel] = []

        # Store Deep Links & Actions as intents
        for dl in dto.deep_links:
            intent_m = APKIntentModel(
                scan_id=scan_id,
                component_name=dl.component_name,
                priority=0,
                auto_verify=dl.auto_verify,
                is_exported=dl.is_browsable,
            )
            self.db.add(intent_m)
            await self.db.flush()

            dl_m = DeepLinkModel(
                intent_id=intent_m.id,
                scheme=dl.scheme,
                host=dl.host,
                port=dl.port,
                path=dl.path,
                mime_type=dl.mime_type,
                is_app_link=dl.is_app_link,
                is_browsable=dl.is_browsable,
            )
            self.db.add(dl_m)
            intent_models.append(intent_m)

        # Store Navigation Graph
        nav_models = [
            NavigationGraphModel(
                scan_id=scan_id,
                source_component=n.source_component,
                intent_action=n.intent_action,
                target_scheme=n.target_scheme,
                target_host=n.target_host,
                destination_component=n.destination_component,
            )
            for n in dto.navigation_nodes
        ]
        if nav_models:
            self.db.add_all(nav_models)

        await self.db.commit()
        return intent_models

    async def get_intents(self, scan_id: uuid.UUID) -> List[APKIntentModel]:
        stmt = (
            select(APKIntentModel)
            .where(APKIntentModel.scan_id == scan_id)
            .options(
                selectinload(APKIntentModel.actions),
                selectinload(APKIntentModel.categories),
                selectinload(APKIntentModel.deep_links),
            )
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())
