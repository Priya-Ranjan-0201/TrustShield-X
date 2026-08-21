"""Pydantic v2 DTO Schemas for Enterprise Call Graph & CFG Intelligence Engine (Phase 3.7 Part 1A.15).

Strictly typed DTOs for Control Flow Graph nodes & edges, Call Graph nodes & edges,
cross-references, loop analysis, dominators, execution paths, SCCs, and graph metrics.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class CFGNodeDTO(BaseModel):
    method_name: str
    block_id: int
    start_offset: int
    end_offset: int
    instruction_count: int = 1
    is_entry: bool = False
    is_exit: bool = False
    is_loop_header: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CFGEdgeDTO(BaseModel):
    method_name: str
    source_block_id: int
    target_block_id: int
    edge_type: str = "FALLTHROUGH"  # FALLTHROUGH, CONDITIONAL, JUMP, SWITCH, EXCEPTION

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CallGraphNodeDTO(BaseModel):
    method_name: str
    class_name: str
    is_reachable: bool = True
    in_degree: int = 0
    out_degree: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CallGraphEdgeDTO(BaseModel):
    caller_method: str
    callee_method: str
    invoke_type: str = "INVOKE_VIRTUAL"
    offset: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class MethodXRefDTO(BaseModel):
    source_symbol: str
    target_symbol: str
    xref_type: str = "CALL"  # CALL, READ_FIELD, WRITE_FIELD, USE_TYPE, STRING_REF

    model_config = ConfigDict(frozen=True, from_attributes=True)


class LoopAnalysisDTO(BaseModel):
    method_name: str
    header_block_id: int
    loop_depth: int = 1

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DominatorNodeDTO(BaseModel):
    method_name: str
    block_id: int
    idom_block_id: Optional[int] = None
    depth: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ExecutionPathDTO(BaseModel):
    method_name: str
    path_length: int = 1
    branch_count: int = 0
    exit_type: str = "RETURN"  # RETURN, THROW, INFINITE_LOOP

    model_config = ConfigDict(frozen=True, from_attributes=True)


class SCCNodeDTO(BaseModel):
    scc_id: int
    node_count: int = 1
    is_recursive: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ProgramGraphMetricsDTO(BaseModel):
    cfg_count: int = 0
    call_graph_nodes_count: int = 0
    call_graph_edges_count: int = 0
    cyclomatic_complexity: float = 1.0
    reachable_methods_count: int = 0
    reachability_percentage: float = 100.0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ProgramGraphResultDTO(BaseModel):
    cfg_nodes: List[CFGNodeDTO] = Field(default_factory=list)
    cfg_edges: List[CFGEdgeDTO] = Field(default_factory=list)
    call_graph_nodes: List[CallGraphNodeDTO] = Field(default_factory=list)
    call_graph_edges: List[CallGraphEdgeDTO] = Field(default_factory=list)
    xrefs: List[MethodXRefDTO] = Field(default_factory=list)
    loops: List[LoopAnalysisDTO] = Field(default_factory=list)
    dominators: List[DominatorNodeDTO] = Field(default_factory=list)
    execution_paths: List[ExecutionPathDTO] = Field(default_factory=list)
    sccs: List[SCCNodeDTO] = Field(default_factory=list)
    metrics: ProgramGraphMetricsDTO = Field(default_factory=ProgramGraphMetricsDTO)
    dot_export: Optional[str] = None
    mermaid_export: Optional[str] = None
    parsing_time_ms: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)
