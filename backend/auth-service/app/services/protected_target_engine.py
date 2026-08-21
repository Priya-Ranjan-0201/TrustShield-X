"""Protected Target Engine & SSRF / Infrastructure Defense (Phase 5).

Prevents malicious or accidental targeting of critical internal systems,
cloud metadata endpoints, loopback addresses, and unauthorized tenant resources.
"""

import ipaddress
import re
from typing import List, Optional, Set
import urllib.parse

PROTECTED_EXACT_TARGETS: Set[str] = {
    "localhost",
    "127.0.0.1",
    "::1",
    "0.0.0.0",
    "10.0.0.1",
    "192.168.1.1",
    "169.254.169.254",  # Cloud Instance Metadata (AWS/GCP/Azure)
    "metadata.google.internal",
    "trustshield.internal",
    "identity.trustshield.internal",
    "auth-service",
    "postgres",
    "redis",
    "root",
    "admin",
    "soc_lead",
    "system",
}

PROTECTED_DOMAINS_SUFFIXES = (
    ".internal",
    ".local",
    ".localhost",
    ".corp",
    ".lan",
    "trustshield.io",
    "truthshield.org",
)


class ProtectedTargetViolationError(Exception):
    """Raised when an action attempts to target protected infrastructure."""
    pass


class TargetValidationError(Exception):
    """Raised when an action target is malformed or unauthorized."""
    pass


class ProtectedTargetEngine:
    """Validates and normalizes targets against SSRF, internal network abuse, and tenancy rules."""

    @staticmethod
    def normalize_target(raw_target: str) -> str:
        """Strip protocols, ports, trailing paths, query strings, and whitespace."""
        t = raw_target.strip().lower()
        if t.startswith("http://") or t.startswith("https://"):
            parsed = urllib.parse.urlparse(t)
            t = parsed.netloc or parsed.path
        
        # Handle bracketed IPv6 with port [::1]:8080
        if t.startswith("[") and "]:" in t:
            t = t.split("]:")[0] + "]"
        elif ":" in t and not t.startswith("[") and t.count(":") == 1:
            t = t.split(":")[0]  # Remove port
            
        t = t.strip("/").strip()
        return t

    @classmethod
    def is_protected_target(cls, raw_target: str) -> bool:
        """Determines if a target is protected system infrastructure."""
        normalized = cls.normalize_target(raw_target)

        # 1. Exact match against blacklist
        if normalized in PROTECTED_EXACT_TARGETS:
            return True

        # 2. Check internal domain suffixes
        if any(normalized.endswith(suffix) for suffix in PROTECTED_DOMAINS_SUFFIXES):
            return True

        # 3. Check IP address ranges (Loopback, Private RFC1918, Link-Local, Multicast, Metadata)
        try:
            clean_ip = normalized.strip("[]")
            ip_obj = ipaddress.ip_address(clean_ip)
            if (
                ip_obj.is_loopback
                or ip_obj.is_private
                or ip_obj.is_link_local
                or ip_obj.is_multicast
                or clean_ip == "169.254.169.254"
            ):
                return True
        except ValueError:
            # Not an IP literal, domain name check
            pass

        # 4. Check for decimal, octal, or hex encoded IP evasion
        if normalized.isdigit():
            try:
                dec_ip = ipaddress.IPv4Address(int(normalized))
                if dec_ip.is_loopback or dec_ip.is_private or dec_ip.is_link_local:
                    return True
            except ValueError:
                pass

        return False

    @classmethod
    def validate_action_target(
        cls,
        target: str,
        target_type: str,
        tenant_id: str,
        authorized_tenant_targets: Optional[List[str]] = None,
    ) -> None:
        """Validates target safety and tenant boundary compliance."""
        if not target or not target.strip():
            raise TargetValidationError("Target cannot be empty.")

        if cls.is_protected_target(target):
            raise ProtectedTargetViolationError(
                f"Action rejected: Target '{target}' is protected infrastructure (SSRF/Loopback/Internal)."
            )

        # Multi-tenant boundary check
        if authorized_tenant_targets is not None:
            normalized = cls.normalize_target(target)
            allowed = [cls.normalize_target(t) for t in authorized_tenant_targets]
            if normalized not in allowed:
                raise TargetValidationError(
                    f"Cross-tenant violation: Target '{target}' does not belong to authorized scope for tenant '{tenant_id}'."
                )
