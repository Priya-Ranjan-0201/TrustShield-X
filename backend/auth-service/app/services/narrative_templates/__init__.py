"""Narrative Templates (Phase 4.0 Part 2 — Section 36).

Deterministic template modules for each narrative section type.
"""

EXECUTIVE_SUMMARY_TEMPLATE = "Digital Trust Assessment — {risk_band_display}. {overall_assessment}"
RISK_EXPLANATION_TEMPLATE = "Risk Score: {risk_score:.1f} / 100. Risk Band: {risk_band}. Confidence: {confidence}. Evidence Sufficiency: {evidence_sufficiency}."
FINDING_TEMPLATE = "Finding [{finding_id}]: {title}. {description}"
EVIDENCE_TEMPLATE = "Evidence [{evidence_id}]: {observation}. Strength: {evidence_strength}."
DATAFLOW_RESOLVED_TEMPLATE = "Analysis identified a resolved path from {source} to {sink}."
DATAFLOW_UNRESOLVED_TEMPLATE = "Analysis identified a potential path from {source}-related functionality, but the complete destination could not be resolved."
BEHAVIOR_TEMPLATE = "The analyzed application exhibits a behavior chain: {chain}."
THREAT_CURRENT_TEMPLATE = "The analyzed {indicator} matches a threat-intelligence indicator currently classified as malicious by the configured intelligence source."
THREAT_STALE_TEMPLATE = "The analyzed {indicator} matches an older threat-intelligence record, but the record is stale and therefore provides weaker current attribution."
CONTRADICTION_TEMPLATE = "Two evidence sources provide conflicting assessments. Because the evidence is unresolved, confidence in this finding is reduced."
MITIGATION_TEMPLATE = "{mitigation} provides a protective control, but it does not eliminate independently observed risk indicators."
RECOMMENDATION_TEMPLATE = "Recommendation ({priority}): {recommendation}."
LIMITATION_TEMPLATE = "{limitation}"
TECHNICAL_SUMMARY_TEMPLATE = "Technical Summary — Engine v{engine_version} — Risk Score: {risk_score:.1f}/100 — Risk Band: {risk_band} — Schema: {schema_version}."

TEMPLATE_VERSION = "1.0.0"
SCHEMA_VERSION = "4.0.0"
LANGUAGE_VERSION = "1.0.0"
