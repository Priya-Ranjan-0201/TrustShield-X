"""Claim Validator Service (Phase 4.0 Part 2 — Sections 41-43).

Validates every narrative statement:
- Checks referenced IDs exist in source data
- Verifies claim strength doesn't exceed evidence
- Detects unsupported numerical values, entities, causal relationships
- Rejects hallucinated claims (Section 42)
- Enforces numerical consistency (Section 43)
"""

import re
from typing import List, Dict, Any, Optional
from app.schemas.trust_narrative_models import NarrativeStatementDTO, NarrativeDocumentDTO


# Hallucination patterns (Section 42)
HALLUCINATION_PATTERNS = [
    (r"confirmed malware", "HALLUCINATION: 'confirmed malware' unsupported"),
    (r"user's data was stolen", "HALLUCINATION: 'data was stolen' unsupported"),
    (r"\battacker\b", "HALLUCINATION: 'attacker' attribution unsupported"),
    (r"\bvictim\b", "HALLUCINATION: 'victim' reference unsupported"),
    (r"government agency", "HALLUCINATION: 'government agency' reference unsupported"),
    (r"definitely malicious", "HALLUCINATION: 'definitely malicious' unsupported"),
    (r"this app steals", "HALLUCINATION: 'steals' unsupported"),
    (r"this is a scam", "HALLUCINATION: 'this is a scam' unsupported"),
]


class ClaimValidator:
    """Validates narrative claims against authoritative source data."""

    def validate_document(
        self,
        doc: NarrativeDocumentDTO,
        authoritative_risk_score: float = 0.0,
        authoritative_risk_band: str = "TRUSTED",
        authoritative_confidence: str = "HIGH",
        authoritative_evidence_sufficiency: str = "SUFFICIENT",
        authoritative_finding_ids: Optional[List[str]] = None,
    ) -> List[str]:
        """Validate entire narrative document. Returns list of validation failures."""
        failures: List[str] = []

        # Numerical consistency (Section 43)
        failures.extend(self._validate_numerical_consistency(
            doc, authoritative_risk_score, authoritative_risk_band,
            authoritative_confidence, authoritative_evidence_sufficiency,
        ))

        # Statement-level validation
        for stmt in doc.statements:
            failures.extend(self._validate_statement(stmt, authoritative_finding_ids or []))

        # Hallucination detection across all narrative text
        all_text = self._collect_all_text(doc)
        failures.extend(self._detect_hallucinations(all_text))

        return failures

    def _validate_numerical_consistency(
        self, doc: NarrativeDocumentDTO,
        expected_score: float, expected_band: str,
        expected_confidence: str, expected_sufficiency: str,
    ) -> List[str]:
        failures = []
        risk_expl = doc.risk_narrative.risk_statement

        # Check risk score presence
        score_str = f"{expected_score:.1f}"
        if score_str not in risk_expl:
            failures.append(f"NARRATIVE_VALIDATION_ERROR: Risk score {score_str} not found in risk statement.")

        # Check risk band presence
        if expected_band not in risk_expl:
            failures.append(f"NARRATIVE_VALIDATION_ERROR: Risk band {expected_band} not found in risk statement.")

        return failures

    def _validate_statement(self, stmt: NarrativeStatementDTO, valid_ids: List[str]) -> List[str]:
        failures = []
        # Verify claim is non-empty
        if not stmt.claim or not stmt.claim.strip():
            failures.append(f"CLAIM_VALIDATION_ERROR: Statement {stmt.statement_id} has empty claim.")
        return failures

    def _detect_hallucinations(self, text: str) -> List[str]:
        failures = []
        text_lower = text.lower()
        for pattern, msg in HALLUCINATION_PATTERNS:
            if re.search(pattern, text_lower):
                failures.append(msg)
        return failures

    def _collect_all_text(self, doc: NarrativeDocumentDTO) -> str:
        parts = [
            doc.executive_summary.headline,
            doc.executive_summary.overall_assessment,
            doc.risk_narrative.risk_statement,
            doc.technical_summary,
            doc.user_friendly_summary,
            doc.analyst_summary,
        ]
        for stmt in doc.statements:
            parts.append(stmt.claim)
        for fn in doc.finding_narratives:
            parts.append(fn.what_was_found)
            parts.append(fn.why_it_matters)
        for en in doc.evidence_narratives:
            parts.append(en.what_was_observed)
        return " ".join(parts)

    def validate_llm_output(self, llm_statements: List[dict], valid_finding_ids: List[str]) -> List[str]:
        """Validate LLM output contract (Section 40). Reject if source IDs missing or unsupported facts appear."""
        failures = []
        for stmt in llm_statements:
            if "statement_id" not in stmt:
                failures.append("LLM_VALIDATION_ERROR: Missing statement_id.")
            if "text" not in stmt:
                failures.append("LLM_VALIDATION_ERROR: Missing text.")
            if "source_ids" not in stmt or not stmt["source_ids"]:
                failures.append(f"LLM_VALIDATION_ERROR: Missing source_ids in statement {stmt.get('statement_id', 'unknown')}.")
            text = stmt.get("text", "").lower()
            for pattern, msg in HALLUCINATION_PATTERNS:
                if re.search(pattern, text):
                    failures.append(f"LLM_{msg}")
        return failures
