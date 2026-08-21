"""
TruthShield X — Entity Resolution Engine (Phase 22).

Resolves equivalent cyber entities (defanged domains, case-varied hashes, IPv4 representations) into canonical forms.
"""

from typing import Dict, Any
import re


class EntityResolutionEngine:
    """Canonicalizes cyber entities across obfuscation and defanging techniques."""

    def resolve_entity(self, raw_value: str, entity_type: str = "DOMAIN") -> Dict[str, str]:
        val = raw_value.strip()

        # Defang resolution
        clean = val.replace("[.]", ".").replace("(.)", ".").replace("[dot]", ".")
        clean = clean.replace("hxxps://", "https://").replace("hxxp://", "http://")
        clean = clean.replace("[:]", ":")

        if entity_type in ("DOMAIN", "URL", "EMAIL"):
            canonical = clean.lower()
        elif entity_type == "HASH":
            canonical = clean.lower()
        elif entity_type == "IP":
            canonical = clean
        else:
            canonical = clean

        return {
            "raw_value": raw_value,
            "canonical_value": canonical,
            "entity_type": entity_type,
            "resolution_status": "RESOLVED",
        }
