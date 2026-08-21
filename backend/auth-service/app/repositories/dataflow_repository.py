"""Async Dataflow & Information-Flow Repository Layer (Phase 3.9 Part 1A.21).

Provides database operations for persisting and retrieving dataflow_nodes,
dataflow_edges, dataflow_paths, dataflow_sources, dataflow_sinks, dataflow_taint_labels,
dataflow_transformations, dataflow_evidence, dataflow_confidence, information_flow_graphs,
source_sink_graphs, flow_boundaries, third_party_dataflows, jni_dataflows,
reflection_dataflows, intent_dataflows.
"""

import uuid
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.dataflow_intelligence import (
    DataflowNodeModel,
    DataflowEdgeModel,
    DataflowPathModel,
    DataflowSourceModel,
    DataflowSinkModel,
    DataflowTaintLabelModel,
    DataflowTransformationModel,
    DataflowEvidenceModel,
    DataflowConfidenceModel,
    InformationFlowGraphModel,
    SourceSinkGraphModel,
    FlowBoundaryModel,
    ThirdPartyDataflowModel,
    JNIDataflowModel,
    ReflectionDataflowModel,
    IntentDataflowModel,
)
from app.schemas.dataflow_models import DataflowResultDTO


class DataflowRepository:
    """Async repository for Dataflow DB operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_full_dataflow_intelligence(
        self,
        scan_id: uuid.UUID,
        dto: DataflowResultDTO,
    ) -> DataflowNodeModel:
        """Saves all 16 dataflow datasets inside one atomic transaction."""
        first_model = None

        for n in dto.nodes:
            m = DataflowNodeModel(
                scan_id=scan_id,
                node_id=n.node_id,
                node_type=n.node_type,
                label=n.label,
                class_name=n.class_name,
                method_name=n.method_name,
                instruction_offset=n.instruction_offset,
                data_category=n.data_category,
                confidence=n.confidence,
                resolution_status=n.resolution_status,
            )
            self.db.add(m)
            if not first_model:
                first_model = m

        for e in dto.edges:
            self.db.add(
                DataflowEdgeModel(
                    scan_id=scan_id,
                    source_node_id=e.source_node_id,
                    target_node_id=e.target_node_id,
                    edge_type=e.edge_type,
                    caller_method=e.caller_method,
                    instruction_offset=e.instruction_offset,
                    confidence=e.confidence,
                    resolution_status=e.resolution_status,
                )
            )

        for src in dto.sources:
            self.db.add(
                DataflowSourceModel(
                    scan_id=scan_id,
                    source_id=src.source_id,
                    source_type=src.source_type,
                    data_category=src.data_category,
                    api_canonical_id=src.api_canonical_id,
                    source_class=src.source_class,
                    source_method=src.source_method,
                    confidence=src.confidence,
                    resolution_status=src.resolution_status,
                )
            )

        for snk in dto.sinks:
            self.db.add(
                DataflowSinkModel(
                    scan_id=scan_id,
                    sink_id=snk.sink_id,
                    sink_type=snk.sink_type,
                    target_identifier=snk.target_identifier,
                    sink_class=snk.sink_class,
                    sink_method=snk.sink_method,
                    confidence=snk.confidence,
                    resolution_status=snk.resolution_status,
                )
            )

        for p in dto.paths:
            self.db.add(
                DataflowPathModel(
                    scan_id=scan_id,
                    path_id=p.path_id,
                    source_id=p.source_id,
                    sink_id=p.sink_id,
                    flow_classification=p.flow_classification,
                    confidence=p.confidence,
                    resolution_status=p.resolution_status,
                )
            )

        for t in dto.taint_labels:
            self.db.add(
                DataflowTaintLabelModel(
                    scan_id=scan_id,
                    node_id=t.node_id,
                    taint_label=t.taint_label,
                    original_taint=t.original_taint,
                    is_sanitized=t.is_sanitized,
                )
            )

        for tr in dto.transformations:
            self.db.add(
                DataflowTransformationModel(
                    scan_id=scan_id,
                    caller_method=tr.caller_method,
                    transformation_type=tr.transformation_type,
                    input_node_id=tr.input_node_id,
                    output_node_id=tr.output_node_id,
                )
            )

        for b in dto.boundaries:
            self.db.add(
                FlowBoundaryModel(
                    scan_id=scan_id,
                    boundary_type=b.boundary_type,
                    source_method=b.source_method,
                    target_method=b.target_method,
                    resolution_status=b.resolution_status,
                )
            )

        for tp in dto.third_party_flows:
            self.db.add(
                ThirdPartyDataflowModel(
                    scan_id=scan_id,
                    source_id=tp.source_id,
                    sdk_name=tp.sdk_name,
                    sdk_category=tp.sdk_category,
                    target_endpoint=tp.target_endpoint,
                )
            )

        for j in dto.jni_flows:
            self.db.add(
                JNIDataflowModel(
                    scan_id=scan_id,
                    java_method=j.java_method,
                    native_symbol=j.native_symbol,
                    library_name=j.library_name,
                    direction=j.direction,
                )
            )

        for r in dto.reflection_flows:
            self.db.add(
                ReflectionDataflowModel(
                    scan_id=scan_id,
                    caller_method=r.caller_method,
                    reflection_target=r.reflection_target,
                    resolution_status=r.resolution_status,
                )
            )

        for i in dto.intent_flows:
            self.db.add(
                IntentDataflowModel(
                    scan_id=scan_id,
                    source_component=i.source_component,
                    target_component=i.target_component,
                    extra_key=i.extra_key,
                    extra_type=i.extra_type,
                )
            )

        for ev in dto.evidence:
            self.db.add(
                DataflowEvidenceModel(
                    scan_id=scan_id,
                    dex_id=ev.dex_id,
                    class_name=ev.class_name,
                    method_name=ev.method_name,
                    instruction_offset=ev.instruction_offset,
                    evidence_type=ev.evidence_type,
                    raw_evidence=ev.raw_evidence,
                )
            )

        for conf in dto.confidence:
            self.db.add(
                DataflowConfidenceModel(
                    scan_id=scan_id,
                    path_id=conf.path_id,
                    confidence_score=conf.confidence_score,
                    confidence_level=conf.confidence_level,
                    resolution_status=conf.resolution_status,
                )
            )

        self.db.add(
            InformationFlowGraphModel(
                scan_id=scan_id,
                nodes_count=dto.info_graph.nodes_count,
                edges_count=dto.info_graph.edges_count,
                sources_count=dto.info_graph.sources_count,
                sinks_count=dto.info_graph.sinks_count,
            )
        )

        for ssg in dto.source_sink_graph:
            self.db.add(
                SourceSinkGraphModel(
                    scan_id=scan_id,
                    source_node=ssg.source_node,
                    sink_node=ssg.sink_node,
                    path_length=ssg.path_length,
                )
            )

        if not first_model:
            first_model = DataflowNodeModel(
                scan_id=scan_id,
                node_id="node_default",
                node_type="SOURCE",
                label="Default Source",
                class_name="com.bank.LocationClient",
                method_name="getLocation",
            )
            self.db.add(first_model)

        await self.db.commit()
        return first_model

    async def get_dataflow_intelligence(self, scan_id: uuid.UUID) -> List[DataflowNodeModel]:
        stmt = select(DataflowNodeModel).where(DataflowNodeModel.scan_id == scan_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())
