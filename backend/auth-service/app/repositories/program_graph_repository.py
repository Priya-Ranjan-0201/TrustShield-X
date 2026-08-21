"""Async Program Graph Repository Layer (Phase 3.7 Part 1A.15).

Provides database operations for persisting and retrieving cfg_nodes, cfg_edges,
call_graph_nodes, call_graph_edges, method_xrefs, loop_analysis, dominators,
execution_paths, scc_analysis, and graph_metrics.
"""

import uuid
from typing import Optional, List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.program_graph import (
    CFGNodeModel,
    CFGEdgeModel,
    CallGraphNodeModel,
    CallGraphEdgeModel,
    MethodXRefModel,
    LoopAnalysisModel,
    DominatorModel,
    ExecutionPathModel,
    SCCModel,
    GraphMetricModel,
)
from app.schemas.program_graph_models import ProgramGraphResultDTO


class ProgramGraphRepository:
    """Async repository for Program Graph DB operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_full_program_graph(
        self,
        scan_id: uuid.UUID,
        dto: ProgramGraphResultDTO,
    ) -> GraphMetricModel:
        """Saves CFGs, Call Graphs, XRefs, loops, dominators, paths, SCCs, and metrics inside one atomic transaction."""
        for n in dto.cfg_nodes:
            self.db.add(
                CFGNodeModel(
                    scan_id=scan_id,
                    method_name=n.method_name,
                    block_id=n.block_id,
                    start_offset=n.start_offset,
                    end_offset=n.end_offset,
                    instruction_count=n.instruction_count,
                    is_entry=n.is_entry,
                    is_exit=n.is_exit,
                    is_loop_header=n.is_loop_header,
                )
            )

        for e in dto.cfg_edges:
            self.db.add(
                CFGEdgeModel(
                    scan_id=scan_id,
                    method_name=e.method_name,
                    source_block_id=e.source_block_id,
                    target_block_id=e.target_block_id,
                    edge_type=e.edge_type,
                )
            )

        for cn in dto.call_graph_nodes:
            self.db.add(
                CallGraphNodeModel(
                    scan_id=scan_id,
                    method_name=cn.method_name,
                    class_name=cn.class_name,
                    is_reachable=cn.is_reachable,
                    in_degree=cn.in_degree,
                    out_degree=cn.out_degree,
                )
            )

        for ce in dto.call_graph_edges:
            self.db.add(
                CallGraphEdgeModel(
                    scan_id=scan_id,
                    caller_method=ce.caller_method,
                    callee_method=ce.callee_method,
                    invoke_type=ce.invoke_type,
                    offset=ce.offset,
                )
            )

        for xref in dto.xrefs:
            self.db.add(
                MethodXRefModel(
                    scan_id=scan_id,
                    source_symbol=xref.source_symbol,
                    target_symbol=xref.target_symbol,
                    xref_type=xref.xref_type,
                )
            )

        for loop in dto.loops:
            self.db.add(
                LoopAnalysisModel(
                    scan_id=scan_id,
                    method_name=loop.method_name,
                    header_block_id=loop.header_block_id,
                    loop_depth=loop.loop_depth,
                )
            )

        for dom in dto.dominators:
            self.db.add(
                DominatorModel(
                    scan_id=scan_id,
                    method_name=dom.method_name,
                    block_id=dom.block_id,
                    idom_block_id=dom.idom_block_id,
                    depth=dom.depth,
                )
            )

        for scc in dto.sccs:
            self.db.add(
                SCCModel(
                    scan_id=scan_id,
                    scc_id=scc.scc_id,
                    node_count=scc.node_count,
                    is_recursive=scc.is_recursive,
                )
            )

        stats_m = GraphMetricModel(
            scan_id=scan_id,
            cfg_count=dto.metrics.cfg_count,
            call_graph_nodes_count=dto.metrics.call_graph_nodes_count,
            call_graph_edges_count=dto.metrics.call_graph_edges_count,
            cyclomatic_complexity=dto.metrics.cyclomatic_complexity,
            reachable_methods_count=dto.metrics.reachable_methods_count,
            reachability_percentage=dto.metrics.reachability_percentage,
        )
        self.db.add(stats_m)

        await self.db.commit()
        return stats_m

    async def get_program_graph(self, scan_id: uuid.UUID) -> Optional[GraphMetricModel]:
        stmt = select(GraphMetricModel).where(GraphMetricModel.scan_id == scan_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()
