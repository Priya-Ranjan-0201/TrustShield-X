"""Correlation Scoring Engine with False-Positive Safeguards (Phase 4.0 Part 5 — Sections 19-21, 53-54).

Calculates relationship candidate scores, applies false-correlation penalties for shared
cloud/CDN infrastructure, shared certificate authorities, and common third-party SDKs.
"""

from typing import Tuple, List, Optional
from app.schemas.intelligence_graph_models import (
    CanonicalEntityDTO,
    CorrelationCandidateDTO,
    GraphRelationshipDTO,
)
from app.services.graph.correlation_rules.domain_rules import DomainCorrelationRule, URLCorrelationRule
from app.services.graph.correlation_rules.certificate_rules import (
    CertificateCorrelationRule,
    PackageCorrelationRule,
    HashCorrelationRule,
)
from app.services.graph.correlation_rules.payment_rules import (
    PaymentCorrelationRule,
    ThreatIntelCorrelationRule,
    TemporalCorrelationRule,
)


class CorrelationScoringEngine:
    """Computes correlation candidate scores with false-positive penalty controls."""

    # Common Third-Party SDKs and Libraries (Section 19)
    COMMON_SDKS = {
        "com.google.android.gms", "com.google.firebase", "com.facebook.android",
        "com.adjust.sdk", "com.appsflyer", "okhttp3", "retrofit2", "androidx"
    }

    # Public Cloud & CDN Suffixes
    PUBLIC_INFRASTRUCTURE = {
        "cloudflare.com", "amazonaws.com", "azure.com", "googleapis.com",
        "akamaized.net", "fastly.net"
    }

    @classmethod
    def evaluate_candidate(
        cls, entity_a: CanonicalEntityDTO, entity_b: CanonicalEntityDTO
    ) -> Optional[CorrelationCandidateDTO]:
        """Evaluates two canonical entities to generate a scored correlation candidate."""
        if entity_a.entity_id == entity_b.entity_id:
            return None

        # 1. Exact Package Match
        if entity_a.entity_type == "PACKAGE" and entity_b.entity_type == "PACKAGE":
            res = PackageCorrelationRule.evaluate(entity_a, entity_b)
            if res.matched:
                return cls._build_candidate(entity_a, entity_b, res)

        # 2. Exact Hash Match
        if entity_a.entity_type in ["HASH", "FILE"] and entity_b.entity_type in ["HASH", "FILE"]:
            res = HashCorrelationRule.evaluate(entity_a, entity_b)
            if res.matched:
                return cls._build_candidate(entity_a, entity_b, res)

        # 3. Certificate Binding
        if entity_b.entity_type == "CERTIFICATE" or entity_a.entity_type == "CERTIFICATE":
            source = entity_a if entity_b.entity_type == "CERTIFICATE" else entity_b
            cert = entity_b if entity_b.entity_type == "CERTIFICATE" else entity_a
            res = CertificateCorrelationRule.evaluate(source, cert)
            if res.matched:
                return cls._build_candidate(source, cert, res)

        # 4. Domain & URL Hosting
        if entity_a.entity_type in ["URL", "PHISHING_KIT"] and entity_b.entity_type == "DOMAIN":
            res = URLCorrelationRule.evaluate(entity_a, entity_b)
            if res.matched:
                return cls._build_candidate(entity_a, entity_b, res)
        elif entity_b.entity_type in ["URL", "PHISHING_KIT"] and entity_a.entity_type == "DOMAIN":
            res = URLCorrelationRule.evaluate(entity_b, entity_a)
            if res.matched:
                return cls._build_candidate(entity_b, entity_a, res)

        # 5. Domain Subdomain Overlap
        if entity_a.entity_type == "DOMAIN" and entity_b.entity_type == "DOMAIN":
            res = DomainCorrelationRule.evaluate(entity_a, entity_b)
            if res.matched:
                return cls._build_candidate(entity_a, entity_b, res)

        # 6. Payment Collection
        if entity_b.entity_type in ["UPI_ID", "BANK_IDENTIFIER"]:
            res = PaymentCorrelationRule.evaluate(entity_a, entity_b)
            if res.matched:
                return cls._build_candidate(entity_a, entity_b, res)

        # 7. Threat Intel Match
        if entity_b.entity_type == "IOC":
            res = ThreatIntelCorrelationRule.evaluate(entity_a, entity_b)
            if res.matched:
                return cls._build_candidate(entity_a, entity_b, res)

        # 8. Temporal Proximity
        res_temp = TemporalCorrelationRule.evaluate(entity_a, entity_b)
        if res_temp.matched and res_temp.candidate_score >= 0.5:
            return cls._build_candidate(entity_a, entity_b, res_temp)

        return None

    @classmethod
    def _build_candidate(
        cls, entity_a: CanonicalEntityDTO, entity_b: CanonicalEntityDTO, res
    ) -> CorrelationCandidateDTO:
        # Check false-correlation rules for SDKs and Public Cloud
        val_a = entity_a.normalized_value
        val_b = entity_b.normalized_value

        extra_penalty = 0.0
        if any(s in val_a or s in val_b for s in cls.COMMON_SDKS):
            extra_penalty += 0.6
        if any(p in val_a or p in val_b for p in cls.PUBLIC_INFRASTRUCTURE):
            extra_penalty += 0.5

        final_score = max(0.0, res.candidate_score - res.false_correlation_penalty - extra_penalty)
        final_conf = cls.score_to_confidence(final_score)

        return CorrelationCandidateDTO(
            candidate_id=f"cand_{entity_a.entity_id}_{entity_b.entity_id}",
            source_entity_id=entity_a.entity_id,
            target_entity_id=entity_b.entity_id,
            relationship_type=res.relationship_type,
            candidate_score=round(final_score, 3),
            confidence=final_conf,
            evidence_count=1,
            correlation_method=res.provenance_source,
            false_correlation_penalty=round(res.false_correlation_penalty + extra_penalty, 3),
        )

    @staticmethod
    def score_to_confidence(score: float) -> str:
        """Maps numeric score to authoritative confidence level."""
        if score >= 0.90:
            return "VERY_HIGH"
        elif score >= 0.70:
            return "HIGH"
        elif score >= 0.50:
            return "MEDIUM"
        elif score >= 0.30:
            return "LOW"
        else:
            return "VERY_LOW"
