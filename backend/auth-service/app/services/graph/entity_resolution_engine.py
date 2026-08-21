"""Entity Resolution Engine (Phase 4.0 Part 5 — Sections 7-10).

Executes exact and multi-signal probabilistic entity resolution across domains,
certificates, hashes, packages, phone numbers, emails, and payment identifiers
with calibrated confidence scoring and conflict detection.
"""

from typing import Tuple, List
from app.services.graph.entity_normalizer import EntityNormalizer


class EntityResolutionEngine:
    """Multi-signal, privacy-preserving entity resolution engine."""

    # -----------------------------------------------------------------------
    # Section 7 & 9: Exact and Specific Resolvers
    # -----------------------------------------------------------------------

    @staticmethod
    def resolve_exact(value_a: str, value_b: str) -> Tuple[str, str, List[str]]:
        """Compares two raw or canonical values for exact identity."""
        if not value_a or not value_b:
            return "NO_MATCH", "VERY_LOW", ["empty_value"]

        if value_a.strip() == value_b.strip():
            return "EXACT_MATCH", "VERY_HIGH", ["exact_string_identity"]
        return "NO_MATCH", "VERY_LOW", ["string_mismatch"]

    @staticmethod
    def resolve_hash(hash_a: str, hash_b: str) -> Tuple[str, str, List[str]]:
        """Resolves two cryptographic file or object hashes."""
        norm_a, _, h_a = EntityNormalizer.normalize_hash(hash_a)
        norm_b, _, h_b = EntityNormalizer.normalize_hash(hash_b)

        if not norm_a or not norm_b:
            return "UNKNOWN", "VERY_LOW", ["invalid_hash"]

        if norm_a == norm_b:
            return "EXACT_MATCH", "VERY_HIGH", ["exact_cryptographic_hash"]
        return "NO_MATCH", "VERY_LOW", ["hash_mismatch"]

    @staticmethod
    def resolve_certificate(cert_a: str, cert_b: str) -> Tuple[str, str, List[str]]:
        """Resolves certificate SHA-256 fingerprints."""
        norm_a, _, _ = EntityNormalizer.normalize_certificate(cert_a)
        norm_b, _, _ = EntityNormalizer.normalize_certificate(cert_b)

        if not norm_a or not norm_b:
            return "UNKNOWN", "VERY_LOW", ["invalid_certificate_fingerprint"]

        if norm_a == norm_b:
            return "EXACT_MATCH", "VERY_HIGH", ["exact_certificate_fingerprint"]
        return "NO_MATCH", "VERY_LOW", ["certificate_fingerprint_mismatch"]

    @staticmethod
    def resolve_domain(domain_a: str, domain_b: str) -> Tuple[str, str, List[str]]:
        """Resolves domains with subdomain overlap and punycode safety."""
        norm_a, _, _ = EntityNormalizer.normalize_domain(domain_a)
        norm_b, _, _ = EntityNormalizer.normalize_domain(domain_b)

        if not norm_a or not norm_b:
            return "UNKNOWN", "VERY_LOW", ["invalid_domain"]

        if norm_a == norm_b:
            return "EXACT_MATCH", "VERY_HIGH", ["exact_normalized_domain"]

        # Check subdomain relationship (e.g. auth.evil.com and evil.com)
        if norm_a.endswith(f".{norm_b}") or norm_b.endswith(f".{norm_a}"):
            return "PROBABLE_MATCH", "HIGH", ["subdomain_parent_relationship"]

        return "NO_MATCH", "VERY_LOW", ["domain_mismatch"]

    @staticmethod
    def resolve_package(pkg_a: str, pkg_b: str) -> Tuple[str, str, List[str]]:
        """Resolves Android package names."""
        norm_a, _, _ = EntityNormalizer.normalize_package(pkg_a)
        norm_b, _, _ = EntityNormalizer.normalize_package(pkg_b)

        if not norm_a or not norm_b:
            return "UNKNOWN", "VERY_LOW", ["invalid_package"]

        if norm_a == norm_b:
            return "EXACT_MATCH", "VERY_HIGH", ["exact_package_name"]

        # Similar package namespace check
        parts_a = norm_a.split(".")
        parts_b = norm_b.split(".")
        if len(parts_a) >= 2 and len(parts_b) >= 2 and parts_a[:2] == parts_b[:2]:
            return "POSSIBLE_MATCH", "MEDIUM", ["shared_package_namespace"]

        return "NO_MATCH", "VERY_LOW", ["package_mismatch"]

    @staticmethod
    def resolve_phone(phone_a: str, phone_b: str) -> Tuple[str, str, List[str]]:
        """Resolves phone numbers using canonical E.164 representation."""
        norm_a, _, _ = EntityNormalizer.normalize_phone(phone_a)
        norm_b, _, _ = EntityNormalizer.normalize_phone(phone_b)

        if not norm_a or not norm_b:
            return "UNKNOWN", "VERY_LOW", ["invalid_phone"]

        if norm_a == norm_b:
            return "EXACT_MATCH", "VERY_HIGH", ["exact_e164_phone"]
        return "NO_MATCH", "VERY_LOW", ["phone_mismatch"]

    @staticmethod
    def resolve_email(email_a: str, email_b: str) -> Tuple[str, str, List[str]]:
        """Resolves email addresses."""
        norm_a, _, _ = EntityNormalizer.normalize_email(email_a)
        norm_b, _, _ = EntityNormalizer.normalize_email(email_b)

        if not norm_a or not norm_b:
            return "UNKNOWN", "VERY_LOW", ["invalid_email"]

        if norm_a == norm_b:
            return "EXACT_MATCH", "VERY_HIGH", ["exact_normalized_email"]

        # Same domain check
        dom_a = norm_a.split("@")[-1] if "@" in norm_a else ""
        dom_b = norm_b.split("@")[-1] if "@" in norm_b else ""
        if dom_a and dom_a == dom_b and dom_a not in ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]:
            return "POSSIBLE_MATCH", "LOW", ["shared_custom_email_domain"]

        return "NO_MATCH", "VERY_LOW", ["email_mismatch"]

    @staticmethod
    def resolve_payment_identifier(upi_a: str, upi_b: str) -> Tuple[str, str, List[str]]:
        """Resolves UPI IDs."""
        norm_a, _, _ = EntityNormalizer.normalize_upi(upi_a)
        norm_b, _, _ = EntityNormalizer.normalize_upi(upi_b)

        if not norm_a or not norm_b:
            return "UNKNOWN", "VERY_LOW", ["invalid_upi"]

        if norm_a == norm_b:
            return "EXACT_MATCH", "VERY_HIGH", ["exact_normalized_upi"]
        return "NO_MATCH", "VERY_LOW", ["upi_mismatch"]

    # -----------------------------------------------------------------------
    # Universal Resolution Dispatcher
    # -----------------------------------------------------------------------

    @classmethod
    def resolve(
        cls, entity_type: str, raw_a: str, raw_b: str
    ) -> Tuple[str, str, List[str]]:
        """Resolves two entity observations based on type.
        
        Returns: (resolution_state, confidence, signals_used)
        """
        t = (entity_type or "").upper()
        if t in ["HASH", "FILE"]:
            return cls.resolve_hash(raw_a, raw_b)
        elif t == "CERTIFICATE":
            return cls.resolve_certificate(raw_a, raw_b)
        elif t in ["DOMAIN", "SUBDOMAIN"]:
            return cls.resolve_domain(raw_a, raw_b)
        elif t in ["PACKAGE", "APPLICATION"]:
            return cls.resolve_package(raw_a, raw_b)
        elif t == "PHONE":
            return cls.resolve_phone(raw_a, raw_b)
        elif t == "EMAIL":
            return cls.resolve_email(raw_a, raw_b)
        elif t in ["UPI_ID", "BANK_IDENTIFIER"]:
            return cls.resolve_payment_identifier(raw_a, raw_b)
        else:
            return cls.resolve_exact(raw_a, raw_b)
