"""Domain and URL Correlation Rules (Phase 4.0 Part 5 — Section 51)."""

from app.schemas.intelligence_graph_models import CanonicalEntityDTO
from app.services.graph.correlation_rules import CorrelationRuleResult


class DomainCorrelationRule:
    RULE_ID = "CORR_DOM_001"
    VERSION = "1.0.0"

    # Known Shared Public Hosting / CDNs (Section 19-20)
    COMMON_INFRASTRUCTURE = {
        "cloudflare.com", "cloudfront.net", "akamai.net", "fastly.net",
        "azureedge.net", "googleusercontent.com", "aws.amazon.com", "github.io"
    }

    @classmethod
    def evaluate(cls, entity_a: CanonicalEntityDTO, entity_b: CanonicalEntityDTO) -> CorrelationRuleResult:
        if entity_a.entity_type != "DOMAIN" or entity_b.entity_type != "DOMAIN":
            return CorrelationRuleResult(cls.RULE_ID, cls.VERSION, False, "", "UNKNOWN", 0.0, 0.0, "", "")

        dom_a = entity_a.normalized_value
        dom_b = entity_b.normalized_value

        # Subdomain / Parent domain relationship
        if dom_a != dom_b and (dom_a.endswith(f".{dom_b}") or dom_b.endswith(f".{dom_a}")):
            # Check false-correlation penalty if parent domain is a public suffix / shared hosting
            is_common = any(dom_a.endswith(f".{c}") or dom_b.endswith(f".{c}") for c in cls.COMMON_INFRASTRUCTURE)
            penalty = 0.5 if is_common else 0.0
            conf = "LOW" if is_common else "HIGH"
            score = 0.4 if is_common else 0.85

            return CorrelationRuleResult(
                rule_id=cls.RULE_ID,
                rule_version=cls.VERSION,
                matched=True,
                relationship_type="RESOLVES_TO" if not is_common else "SHARES_INFRASTRUCTURE",
                confidence=conf,
                candidate_score=score,
                false_correlation_penalty=penalty,
                evidence_summary=f"Hierarchical domain overlap between {dom_a} and {dom_b}",
                provenance_source="DOMAIN_NORMALIZER",
            )

        return CorrelationRuleResult(cls.RULE_ID, cls.VERSION, False, "", "UNKNOWN", 0.0, 0.0, "", "")


class URLCorrelationRule:
    RULE_ID = "CORR_URL_001"
    VERSION = "1.0.0"

    @classmethod
    def evaluate(cls, url_entity: CanonicalEntityDTO, domain_entity: CanonicalEntityDTO) -> CorrelationRuleResult:
        if url_entity.entity_type not in ["URL", "PHISHING_KIT"] or domain_entity.entity_type != "DOMAIN":
            return CorrelationRuleResult(cls.RULE_ID, cls.VERSION, False, "", "UNKNOWN", 0.0, 0.0, "", "")

        url_val = url_entity.normalized_value
        dom_val = domain_entity.normalized_value

        if f"://{dom_val}" in url_val or f".{dom_val}/" in url_val or url_val.startswith(f"http://{dom_val}") or url_val.startswith(f"https://{dom_val}"):
            return CorrelationRuleResult(
                rule_id=cls.RULE_ID,
                rule_version=cls.VERSION,
                matched=True,
                relationship_type="HOSTS",
                confidence="VERY_HIGH",
                candidate_score=0.95,
                false_correlation_penalty=0.0,
                evidence_summary=f"Domain {dom_val} hosts URL {url_entity.display_value}",
                provenance_source="URL_PARSER",
            )

        return CorrelationRuleResult(cls.RULE_ID, cls.VERSION, False, "", "UNKNOWN", 0.0, 0.0, "", "")
