"""Unit tests for Rule Execution Trace Generation (Phase 3.9 Part 1A.24)."""

import pytest
from app.schemas.behavior_rule_models import RuleExecutionTraceDTO, RuleConditionResultDTO


def test_rule_execution_trace_dto():
    trace = RuleExecutionTraceDTO(
        trace_id="tr_1",
        rule_id="RULE-DATAFLOW-001",
        rule_version="1.0.0",
        duration_ms=12,
        condition_results=[
            RuleConditionResultDTO(
                condition_id="c1",
                condition_type="PERMISSION_USED",
                expected="READ_SMS",
                actual="READ_SMS",
                matched=True,
            )
        ],
        final_state="MATCHED",
    )

    assert trace.trace_id == "tr_1"
    assert len(trace.condition_results) == 1
