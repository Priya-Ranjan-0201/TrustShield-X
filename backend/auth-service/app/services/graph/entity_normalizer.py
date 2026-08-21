"""Entity Normalizer with Privacy-Preserving Transformations (Phase 4.0 Part 5 — Sections 4-6, 75).

Provides deterministic, non-destructive canonical normalization for Domains, URLs,
IP Addresses, Hashes, Certificate Fingerprints, Package Names, Emails, Phone Numbers,
UPI IDs, and Bank Identifiers with Unicode lookalike safety and privacy masking.
"""

import re
import urllib.parse
import hashlib
import ipaddress
from typing import Tuple, Optional


class EntityNormalizer:
    """Deterministic, privacy-aware canonical entity normalizer."""

    # -----------------------------------------------------------------------
    # Section 4 & 5: Domain & URL Normalization
    # -----------------------------------------------------------------------

    @staticmethod
    def normalize_domain(domain_raw: str) -> Tuple[str, str, str]:
        """Normalizes a domain or hostname.
        
        Returns: (canonical_value, display_value, value_hash)
        """
        raw = (domain_raw or "").strip().lower()
        # Remove protocol prefix if accidentally supplied
        if raw.startswith("http://"):
            raw = raw[7:]
        elif raw.startswith("https://"):
            raw = raw[8:]
        # Remove path and port for pure domain normalization
        raw = raw.split("/")[0].split(":")[0].rstrip(".")

        try:
            # Handle IDNA / Punycode conversion for lookalikes
            idna_encoded = raw.encode("idna").decode("ascii")
            canonical = idna_encoded
        except Exception:
            canonical = raw

        display = canonical
        v_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return canonical, display, v_hash

    @staticmethod
    def normalize_url(url_raw: str) -> Tuple[str, str, str]:
        """Normalizes a URL while preserving query parameters and paths."""
        raw = (url_raw or "").strip()
        if not raw:
            return "", "", ""

        # Default protocol if missing
        if not (raw.startswith("http://") or raw.startswith("https://")):
            raw = f"http://{raw}"

        parsed = urllib.parse.urlparse(raw)
        scheme = parsed.scheme.lower()
        netloc = parsed.netloc.lower()
        
        # Remove default ports
        if netloc.endswith(":80") and scheme == "http":
            netloc = netloc[:-3]
        elif netloc.endswith(":443") and scheme == "https":
            netloc = netloc[:-4]

        path = parsed.path or "/"
        # Sort query parameters deterministically
        query_pairs = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
        sorted_query = urllib.parse.urlencode(sorted(query_pairs))

        canonical = urllib.parse.urlunparse((scheme, netloc, path, "", sorted_query, ""))
        display = canonical
        v_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return canonical, display, v_hash

    # -----------------------------------------------------------------------
    # IP Addresses & Hashes
    # -----------------------------------------------------------------------

    @staticmethod
    def normalize_ip(ip_raw: str) -> Tuple[str, str, str]:
        """Normalizes IPv4 and IPv6 addresses."""
        raw = (ip_raw or "").strip()
        try:
            ip_obj = ipaddress.ip_address(raw)
            canonical = str(ip_obj)
        except ValueError:
            canonical = raw.lower()

        display = canonical
        v_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return canonical, display, v_hash

    @staticmethod
    def normalize_hash(hash_raw: str) -> Tuple[str, str, str]:
        """Normalizes cryptographic hashes (MD5, SHA-1, SHA-256, SHA-512)."""
        raw = re.sub(r"[^0-9a-fA-F]", "", (hash_raw or "").strip()).lower()
        canonical = raw
        display = canonical
        v_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return canonical, display, v_hash

    @staticmethod
    def normalize_certificate(cert_raw: str) -> Tuple[str, str, str]:
        """Normalizes certificate SHA-256 fingerprint."""
        raw = re.sub(r"[^0-9a-fA-F]", "", (cert_raw or "").strip()).upper()
        canonical = raw
        display = ":".join(canonical[i:i+2] for i in range(0, len(canonical), 2)) if canonical else ""
        v_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return canonical, display, v_hash

    @staticmethod
    def normalize_package(package_raw: str) -> Tuple[str, str, str]:
        """Normalizes Android package name."""
        raw = (package_raw or "").strip().lower()
        canonical = raw
        display = canonical
        v_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return canonical, display, v_hash

    # -----------------------------------------------------------------------
    # Section 6 & 75: Privacy-Preserving Normalized Identifiers
    # -----------------------------------------------------------------------

    @staticmethod
    def normalize_phone(phone_raw: str) -> Tuple[str, str, str]:
        """Normalizes phone numbers with privacy masking.
        
        Example: +919876543210 -> Masked Display: +91******3210
        """
        digits = re.sub(r"[^\d+]", "", (phone_raw or "").strip())
        if not digits.startswith("+") and len(digits) == 10:
            digits = f"+91{digits}"

        canonical = digits
        if len(digits) >= 10:
            masked = f"{digits[:3]}******{digits[-4:]}"
        else:
            masked = "***"

        v_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return canonical, masked, v_hash

    @staticmethod
    def normalize_email(email_raw: str) -> Tuple[str, str, str]:
        """Normalizes email addresses with privacy masking."""
        raw = (email_raw or "").strip().lower()
        if "@" in raw:
            local_part, domain = raw.split("@", 1)
            canonical = f"{local_part}@{domain}"
            masked_local = f"{local_part[:2]}***" if len(local_part) > 2 else "***"
            masked = f"{masked_local}@{domain}"
        else:
            canonical = raw
            masked = "***"

        v_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return canonical, masked, v_hash

    @staticmethod
    def normalize_upi(upi_raw: str) -> Tuple[str, str, str]:
        """Normalizes Indian UPI IDs (e.g. user@bank) with privacy masking."""
        raw = (upi_raw or "").strip().lower()
        if "@" in raw:
            user_part, handle = raw.split("@", 1)
            canonical = f"{user_part}@{handle}"
            masked_user = f"{user_part[:2]}***{user_part[-2:]}" if len(user_part) > 4 else "***"
            masked = f"{masked_user}@{handle}"
        else:
            canonical = raw
            masked = "***"

        v_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return canonical, masked, v_hash

    # -----------------------------------------------------------------------
    # Generic Router
    # -----------------------------------------------------------------------

    @classmethod
    def normalize(cls, entity_type: str, raw_value: str) -> Tuple[str, str, str]:
        """Universal normalizer dispatching based on entity_type."""
        t = (entity_type or "").upper()
        if t in ["DOMAIN", "SUBDOMAIN"]:
            return cls.normalize_domain(raw_value)
        elif t in ["URL", "PHISHING_KIT"]:
            return cls.normalize_url(raw_value)
        elif t in ["IP_ADDRESS", "NETWORK_ENDPOINT"]:
            return cls.normalize_ip(raw_value)
        elif t in ["HASH", "FILE"]:
            return cls.normalize_hash(raw_value)
        elif t == "CERTIFICATE":
            return cls.normalize_certificate(raw_value)
        elif t in ["PACKAGE", "APPLICATION"]:
            return cls.normalize_package(raw_value)
        elif t == "PHONE":
            return cls.normalize_phone(raw_value)
        elif t == "EMAIL":
            return cls.normalize_email(raw_value)
        elif t in ["UPI_ID", "BANK_IDENTIFIER"]:
            return cls.normalize_upi(raw_value)
        else:
            cleaned = (raw_value or "").strip()
            v_hash = hashlib.sha256(cleaned.encode("utf-8")).hexdigest()
            return cleaned, cleaned, v_hash
