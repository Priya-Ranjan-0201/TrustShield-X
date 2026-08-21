"""
TruthShield X — Asset Canonicalization Service & SSRF Target Validator
"""

import ipaddress
import re
import urllib.parse
from typing import Tuple, Dict, Any


class AssetCanonicalizationService:
    """Normalizes identifiers and validates target safety to prevent SSRF and injection attacks."""

    PRIVATE_AND_RESERVED_NETWORKS = [
        ipaddress.ip_network("127.0.0.0/8"),
        ipaddress.ip_network("10.0.0.0/8"),
        ipaddress.ip_network("172.16.0.0/12"),
        ipaddress.ip_network("192.168.0.0/16"),
        ipaddress.ip_network("169.254.0.0/16"),  # Cloud metadata / link local
        ipaddress.ip_network("0.0.0.0/8"),
        ipaddress.ip_network("::1/128"),
        ipaddress.ip_network("fc00::/7"),
        ipaddress.ip_network("fe80::/10"),
    ]

    @staticmethod
    def canonicalize_identifier(asset_type: str, raw_identifier: str) -> Tuple[str, str]:
        """Returns (canonical_identifier, display_identifier). Preserves original representation."""
        raw = raw_identifier.strip()
        asset_type_upper = asset_type.upper()

        if asset_type_upper in ("DOMAIN", "SUBDOMAIN", "EMAIL_DOMAIN"):
            # Lowercase, remove trailing dots, strip protocol if present
            cleaned = raw.lower()
            if "://" in cleaned:
                parsed = urllib.parse.urlparse(cleaned)
                cleaned = parsed.netloc or parsed.path
            cleaned = cleaned.rstrip(".")
            return (cleaned, raw)

        elif asset_type_upper == "URL":
            parsed = urllib.parse.urlparse(raw)
            scheme = (parsed.scheme or "https").lower()
            netloc = (parsed.netloc or "").lower()
            path = parsed.path or "/"
            query = f"?{parsed.query}" if parsed.query else ""
            canonical = f"{scheme}://{netloc}{path}{query}"
            return (canonical, raw)

        elif asset_type_upper == "IP_ADDRESS":
            # Strip CIDR or port if provided
            ip_clean = raw.split("/")[0].split(":")[0].strip()
            return (ip_clean, raw)

        elif asset_type_upper == "UPI_IDENTIFIER":
            cleaned = raw.lower().strip()
            return (cleaned, raw)

        elif asset_type_upper == "PHONE_NUMBER":
            # E.164 normalization: strip non-digits, ensure + prefix
            digits = re.sub(r"\D", "", raw)
            canonical = f"+{digits}" if not raw.startswith("+") else f"+{digits}"
            return (canonical, raw)

        elif asset_type_upper in ("CERTIFICATE", "APK", "PACKAGE"):
            # Lowercase hex / string
            return (raw.lower(), raw)

        return (raw, raw)

    @classmethod
    def validate_target_safety(cls, target: str) -> Dict[str, Any]:
        """Validates that a hostname or IP address is safe for active monitoring and not an SSRF target."""
        clean_target = target.strip().lower()
        if "://" in clean_target:
            clean_target = urllib.parse.urlparse(clean_target).netloc or clean_target
        clean_target = clean_target.split(":")[0]  # remove port

        # Check direct localhost strings
        if clean_target in ("localhost", "127.0.0.1", "::1", "metadata.google.internal", "instance-data"):
            return {"is_safe": False, "reason": "Target is local host or cloud metadata service."}

        # Check IP address blocks
        try:
            ip_obj = ipaddress.ip_address(clean_target)
            for net in cls.PRIVATE_AND_RESERVED_NETWORKS:
                if ip_obj in net:
                    return {"is_safe": False, "reason": f"Target IP {clean_target} belongs to private or reserved subnet {net}."}
            if ip_obj.is_multicast or ip_obj.is_reserved or ip_obj.is_link_local:
                return {"is_safe": False, "reason": f"Target IP {clean_target} is reserved or non-routable."}
        except ValueError:
            # Target is a domain name
            pass

        # Check suspicious internal patterns
        if re.search(r"(\.internal|\.local|\.lan|\.corp|\.home)$", clean_target):
            return {"is_safe": False, "reason": "Target domain uses a private/internal TLD."}

        return {"is_safe": True, "reason": "Target passed SSRF and network safety checks."}
