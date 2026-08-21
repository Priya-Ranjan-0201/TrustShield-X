"""Async Reflection Repository Layer (Phase 3.7 Part 1A.17).

Provides database operations for persisting and retrieving reflection_calls,
reflection_targets, dynamic_class_loading, native_loading, jni_registration,
hidden_api_usage, reflection_graph, and dynamic_invocations.
"""

import uuid
from typing import Optional, List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.reflection_intelligence import (
    ReflectionCallModel,
    ReflectionTargetModel,
    DynamicClassModel,
    NativeLibraryModel,
    JNIBindingModel,
    HiddenAPIModel,
    ReflectionGraphModel,
    DynamicInvocationModel,
)
from app.schemas.reflection_models import ReflectionResultDTO


class ReflectionRepository:
    """Async repository for Reflection DB operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_full_reflection_intelligence(
        self,
        scan_id: uuid.UUID,
        dto: ReflectionResultDTO,
    ) -> ReflectionCallModel:
        """Saves reflection calls, targets, dynamic loaders, native loads, JNI, hidden APIs, and graphs inside one atomic transaction."""
        first_model = None

        for call in dto.reflection_calls:
            m = ReflectionCallModel(
                scan_id=scan_id,
                caller_method=call.caller_method,
                reflection_api=call.reflection_api,
                target_class=call.target_class,
                target_member=call.target_member,
                offset=call.offset,
            )
            self.db.add(m)
            if not first_model:
                first_model = m

        for t in dto.targets:
            self.db.add(
                ReflectionTargetModel(
                    scan_id=scan_id,
                    canonical_target=t.canonical_target,
                    target_type=t.target_type,
                    is_resolved=t.is_resolved,
                )
            )

        for dc in dto.dynamic_classes:
            self.db.add(
                DynamicClassModel(
                    scan_id=scan_id,
                    caller_method=dc.caller_method,
                    loader_type=dc.loader_type,
                    dex_path=dc.dex_path,
                    is_memory_only=dc.is_memory_only,
                )
            )

        for nl in dto.native_loads:
            self.db.add(
                NativeLibraryModel(
                    scan_id=scan_id,
                    caller_method=nl.caller_method,
                    library_name=nl.library_name,
                    load_api=nl.load_api,
                )
            )

        for jni in dto.jni_bindings:
            self.db.add(
                JNIBindingModel(
                    scan_id=scan_id,
                    native_method=jni.native_method,
                    java_class=jni.java_class,
                    symbol_name=jni.symbol_name,
                )
            )

        for ha in dto.hidden_apis:
            self.db.add(
                HiddenAPIModel(
                    scan_id=scan_id,
                    api_signature=ha.api_signature,
                    access_mechanism=ha.access_mechanism,
                    restriction_level=ha.restriction_level,
                )
            )

        for edge in dto.reflection_graph:
            self.db.add(
                ReflectionGraphModel(
                    scan_id=scan_id,
                    caller_method=edge.caller_method,
                    target_symbol=edge.target_symbol,
                    invocation_type=edge.invocation_type,
                )
            )

        for inv in dto.dynamic_invocations:
            self.db.add(
                DynamicInvocationModel(
                    scan_id=scan_id,
                    source_symbol=inv.source_symbol,
                    resolved_target=inv.resolved_target,
                    confidence=inv.confidence,
                )
            )

        if not first_model:
            first_model = ReflectionCallModel(
                scan_id=scan_id,
                caller_method="system.Init",
                reflection_api="NONE",
            )
            self.db.add(first_model)

        await self.db.commit()
        return first_model

    async def get_reflection_intelligence(self, scan_id: uuid.UUID) -> List[ReflectionCallModel]:
        stmt = select(ReflectionCallModel).where(ReflectionCallModel.scan_id == scan_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())
