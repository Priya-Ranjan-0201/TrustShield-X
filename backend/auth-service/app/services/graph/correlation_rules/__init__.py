"""Correlation Rules Package for TruthShield X Intelligence Graph (Phase 4.0 Part 5 — Section 51)."""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class CorrelationRuleResult:
    rule_id: str
    rule_version: str
    matched: bool
    relationship_type: str
    confidence: str
    candidate_score: float
    false_correlation_penalty: float
    evidence_summary: str
    provenance_source: str
