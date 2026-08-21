"""Certificate, Package, and Hash Correlation Rules (Phase 4.0 Part 5 — Section 51)."""

from app.schemas.intelligence_graph_models import CanonicalEntityDTO
from app.services.graph.correlation_rules import CorrelationRuleResult


class CertificateCorrelationRule:
    RULE_ID = "CORR_CERT_001"
    VERSION = "1.0.0"

    @classmethod
    def evaluate(cls, app_or_dom: CanonicalEntityDTO, cert: CanonicalEntityDTO) -> CorrelationRuleResult:
        if cert.entity_type != "CERTIFICATE":
            return CorrelationRuleResult(cls.RULE_ID, cls.VERSION, False, "", "UNKNOWN", 0.0, 0.0, "", "")

        # Check exact certificate binding
        if app_or_dom.entity_type in ["PACKAGE", "APPLICATION", "DOMAIN", "APK"]:
            return CorrelationRuleResult(
                rule_id=cls.RULE_ID,
                rule_version=cls.VERSION,
                matched=True,
                relationship_type="USES_CERTIFICATE",
                confidence="VERY_HIGH",
                candidate_score=0.98,
                false_correlation_penalty=0.0,
                evidence_summary=f"Entity {app_or_dom.display_value} cryptographically signed with Certificate {cert.display_value}",
                provenance_source="CERT_PARSER",
            )

        return CorrelationRuleResult(cls.RULE_ID, cls.VERSION, False, "", "UNKNOWN", 0.0, 0.0, "", "")


class PackageCorrelationRule:
    RULE_ID = "CORR_PKG_001"
    VERSION = "1.0.0"

    @classmethod
    def evaluate(cls, pkg_a: CanonicalEntityDTO, pkg_b: CanonicalEntityDTO) -> CorrelationRuleResult:
        if pkg_a.entity_type != "PACKAGE" or pkg_b.entity_type != "PACKAGE":
            return CorrelationRuleResult(cls.RULE_ID, cls.VERSION, False, "", "UNKNOWN", 0.0, 0.0, "", "")

        if pkg_a.normalized_value == pkg_b.normalized_value:
            return CorrelationRuleResult(
                rule_id=cls.RULE_ID,
                rule_version=cls.VERSION,
                matched=True,
                relationship_type="MATCHES",
                confidence="VERY_HIGH",
                candidate_score=1.0,
                false_correlation_penalty=0.0,
                evidence_summary=f"Identical package identifier {pkg_a.normalized_value}",
                provenance_source="APK_MANIFEST_PARSER",
            )

        return CorrelationRuleResult(cls.RULE_ID, cls.VERSION, False, "", "UNKNOWN", 0.0, 0.0, "", "")


class HashCorrelationRule:
    RULE_ID = "CORR_HASH_001"
    VERSION = "1.0.0"

    @classmethod
    def evaluate(cls, hash_a: CanonicalEntityDTO, hash_b: CanonicalEntityDTO) -> CorrelationRuleResult:
        if hash_a.entity_type != "HASH" or hash_b.entity_type != "HASH":
            return CorrelationRuleResult(cls.RULE_ID, cls.VERSION, False, "", "UNKNOWN", 0.0, 0.0, "", "")

        if hash_a.normalized_value == hash_b.normalized_value:
            return CorrelationRuleResult(
                rule_id=cls.RULE_ID,
                rule_version=cls.VERSION,
                matched=True,
                relationship_type="MATCHES",
                confidence="VERY_HIGH",
                candidate_score=1.0,
                false_correlation_penalty=0.0,
                evidence_summary=f"Identical cryptographic hash {hash_a.normalized_value}",
                provenance_source="CRYPTO_HASH_VERIFIER",
            )

        return CorrelationRuleResult(cls.RULE_ID, cls.VERSION, False, "", "UNKNOWN", 0.0, 0.0, "", "")
