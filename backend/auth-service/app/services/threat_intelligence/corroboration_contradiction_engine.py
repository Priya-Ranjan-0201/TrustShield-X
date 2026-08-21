"""
TruthShield X — Corroboration & Contradiction Engine (Phase 22).

Identifies independent corroboration and captures conflicting intelligence claims without destructive overrides.
"""

from typing import Dict, List, Any


class CorroborationContradictionEngine:
    """Evaluates multi-source convergence and flags intelligence conflicts."""

    def evaluate_corroboration(self, claims: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculates independent corroboration and identifies conflicting claims."""
        if not claims:
            return {"corroboration_count": 0, "status": "INSUFFICIENT_EVIDENCE", "conflicts": []}

        # Distinct sources supporting the claim
        sources = {c.get("source_id") for c in claims if c.get("source_id")}
        statuses = {c.get("reputation") or c.get("status") for c in claims if c.get("reputation") or c.get("status")}

        conflicts = []
        if len(statuses) > 1 and ("MALICIOUS" in statuses or "MALICIOUS_REPORTED" in statuses) and ("BENIGN" in statuses or "CLEAN_REPORTED" in statuses):
            conflicts.append({
                "conflict_type": "REPUTATION_DISAGREEMENT",
                "competing_claims": list(statuses),
                "resolution": "CONFLICTING_INTELLIGENCE",
            })

        status = "CORROBORATED" if len(sources) >= 2 else "SINGLE_SOURCE"
        if conflicts:
            status = "CONFLICTING_INTELLIGENCE"

        return {
            "corroborating_source_count": len(sources),
            "independent_sources": list(sources),
            "status": status,
            "conflicts": conflicts,
            "preserves_all_claims": True,
        }
