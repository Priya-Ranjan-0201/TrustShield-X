"""
Microsegmentation & Software-Defined Perimeter (SDP) Engine (Phase 34)
======================================================================
Manages network zones, fine-grained flow policies, default-deny enforcement,
and east-west lateral movement containment.
"""

from typing import Dict, Any, List, Optional
import datetime


class MicrosegmentationEngine:
    def __init__(self):
        self._zones: Dict[str, Dict[str, Any]] = {}
        self._rules: Dict[str, Dict[str, Any]] = {}

    def create_zone(
        self,
        zone_id: str,
        tenant_id: str,
        name: str,
        zone_type: str = "APPLICATION",
        trust_level: str = "MEDIUM",
        **kwargs
    ) -> Dict[str, Any]:
        zone = {
            "zone_id": zone_id,
            "tenant_id": tenant_id,
            "name": name,
            "zone_type": zone_type,
            "trust_level": trust_level,
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        self._zones[zone_id] = zone
        return zone

    def register_segment(
        self,
        segment_id: str,
        tenant_id: str,
        name: str,
        segment_type: str,
        trust_tier: str = "INTERNAL_HIGH"
    ) -> Dict[str, Any]:
        return self.create_zone(
            zone_id=segment_id,
            tenant_id=tenant_id,
            name=name,
            zone_type=segment_type,
            trust_level=trust_tier
        )

    def add_rule(
        self,
        rule_id: str,
        tenant_id: str,
        source_zone_id: str,
        dest_zone_id: str,
        protocol: str = "TCP",
        port_range: str = "443",
        action: str = "ALLOW",
        **kwargs
    ) -> Dict[str, Any]:
        rule = {
            "rule_id": rule_id,
            "tenant_id": tenant_id,
            "source_zone_id": source_zone_id,
            "dest_zone_id": dest_zone_id,
            "protocol": protocol.upper(),
            "port_range": str(port_range),
            "action": action.upper(),
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        self._rules[rule_id] = rule
        return rule

    def evaluate_traffic(
        self,
        tenant_id: str,
        source_zone_id: str,
        dest_zone_id: str,
        protocol: str = "TCP",
        port: int = 443
    ) -> Dict[str, Any]:
        # Enforce strict default deny
        matched_rule = None
        for rule in self._rules.values():
            if rule["tenant_id"] != tenant_id:
                continue
            if rule["source_zone_id"] in [source_zone_id, "*"] and rule["dest_zone_id"] in [dest_zone_id, "*"]:
                if rule["protocol"] in [protocol.upper(), "*"]:
                    # check port
                    if rule["port_range"] in [str(port), "*"]:
                        matched_rule = rule
                        break

        if matched_rule and matched_rule["action"] == "ALLOW":
            return {
                "action": "ALLOW",
                "reason": "MATCHING_RULE_FOUND",
                "matched_rule_id": matched_rule["rule_id"],
                "source_zone_id": source_zone_id,
                "dest_zone_id": dest_zone_id
            }

        return {
            "action": "BLOCK",
            "reason": "DEFAULT_DENY_NO_MATCH",
            "source_zone_id": source_zone_id,
            "dest_zone_id": dest_zone_id
        }

    def validate_zone_traffic(
        self,
        tenant_id: str,
        source_zone_id: str,
        dest_zone_id: str,
        protocol: str = "TCP",
        port: int = 443
    ) -> Dict[str, Any]:
        return self.evaluate_traffic(tenant_id, source_zone_id, dest_zone_id, protocol, port)

    def get_zones(self, tenant_id: str) -> List[Dict[str, Any]]:
        return [z for z in self._zones.values() if z["tenant_id"] == tenant_id]

    def get_rules(self, tenant_id: str) -> List[Dict[str, Any]]:
        return [r for r in self._rules.values() if r["tenant_id"] == tenant_id]


microsegmentation_engine = MicrosegmentationEngine()
