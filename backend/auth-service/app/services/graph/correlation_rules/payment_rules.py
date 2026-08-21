"""Payment, Document, Audio, Threat Intel, and Temporal Correlation Rules (Phase 4.0 Part 5 — Section 51)."""

from datetime import datetime
from app.schemas.intelligence_graph_models import CanonicalEntityDTO
from app.services.graph.correlation_rules import CorrelationRuleResult


class PaymentCorrelationRule:
    RULE_ID = "CORR_PAY_001"
    VERSION = "1.0.0"

    @classmethod
    def evaluate(cls, source_ent: CanonicalEntityDTO, upi_ent: CanonicalEntityDTO) -> CorrelationRuleResult:
        if upi_ent.entity_type not in ["UPI_ID", "BANK_IDENTIFIER"]:
            return CorrelationRuleResult(cls.RULE_ID, cls.VERSION, False, "", "UNKNOWN", 0.0, 0.0, "", "")

        if source_ent.entity_type in ["QR_PAYLOAD", "URL", "PHISHING_KIT", "AUDIO", "DOCUMENT"]:
            return CorrelationRuleResult(
                rule_id=cls.RULE_ID,
                rule_version=cls.VERSION,
                matched=True,
                relationship_type="COLLECTS",
                confidence="HIGH",
                candidate_score=0.90,
                false_correlation_penalty=0.0,
                evidence_summary=f"Payment identifier {upi_ent.display_value} collected by {source_ent.entity_type}",
                provenance_source="PAYMENT_GATEWAY_EXTRACTOR",
            )

        return CorrelationRuleResult(cls.RULE_ID, cls.VERSION, False, "", "UNKNOWN", 0.0, 0.0, "", "")


class ThreatIntelCorrelationRule:
    RULE_ID = "CORR_TI_001"
    VERSION = "1.0.0"

    @classmethod
    def evaluate(cls, entity: CanonicalEntityDTO, ioc: CanonicalEntityDTO) -> CorrelationRuleResult:
        if ioc.entity_type != "IOC":
            return CorrelationRuleResult(cls.RULE_ID, cls.VERSION, False, "", "UNKNOWN", 0.0, 0.0, "", "")

        if entity.normalized_value == ioc.normalized_value:
            return CorrelationRuleResult(
                rule_id=cls.RULE_ID,
                rule_version=cls.VERSION,
                matched=True,
                relationship_type="MATCHES",
                confidence="VERY_HIGH",
                candidate_score=0.96,
                false_correlation_penalty=0.0,
                evidence_summary=f"Direct match with verified threat intelligence indicator {ioc.display_value}",
                provenance_source="THREAT_INTELLIGENCE_FEED",
            )

        return CorrelationRuleResult(cls.RULE_ID, cls.VERSION, False, "", "UNKNOWN", 0.0, 0.0, "", "")


class TemporalCorrelationRule:
    RULE_ID = "CORR_TEMP_001"
    VERSION = "1.0.0"

    @classmethod
    def evaluate(cls, entity_a: CanonicalEntityDTO, entity_b: CanonicalEntityDTO) -> CorrelationRuleResult:
        try:
            t_a = datetime.fromisoformat(entity_a.first_seen.replace("Z", "+00:00"))
            t_b = datetime.fromisoformat(entity_b.first_seen.replace("Z", "+00:00"))
            diff_hours = abs((t_a - t_b).total_seconds()) / 3600.0

            # Proximity within 2 hours
            if diff_hours <= 2.0:
                return CorrelationRuleResult(
                    rule_id=cls.RULE_ID,
                    rule_version=cls.VERSION,
                    matched=True,
                    relationship_type="CORRELATED_WITH",
                    confidence="MEDIUM",
                    candidate_score=0.65,
                    false_correlation_penalty=0.0,
                    evidence_summary=f"Observed within {diff_hours:.1f} hours of each other (temporal proximity)",
                    provenance_source="TEMPORAL_ANALYZER",
                )
            elif diff_hours > 4320.0:  # > 180 days (6 months)
                # Lower temporal relevance
                return CorrelationRuleResult(
                    rule_id=cls.RULE_ID,
                    rule_version=cls.VERSION,
                    matched=True,
                    relationship_type="CORRELATED_WITH",
                    confidence="LOW",
                    candidate_score=0.20,
                    false_correlation_penalty=0.4,
                    evidence_summary=f"Observed {diff_hours / 24.0:.0f} days apart (distant temporal window)",
                    provenance_source="TEMPORAL_ANALYZER",
                )
        except Exception:
            pass

        return CorrelationRuleResult(cls.RULE_ID, cls.VERSION, False, "", "UNKNOWN", 0.0, 0.0, "", "")
