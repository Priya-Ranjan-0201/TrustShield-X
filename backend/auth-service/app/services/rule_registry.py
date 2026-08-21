"""Rule Registry for Declarative Security Behavior Rules (Phase 3.9 Part 1A.24).

Loads, versions, enables/disables, and manages active rule packs without code execution.
"""

from typing import List, Dict, Any
from app.schemas.behavior_rule_models import BehaviorRuleDTO, BehaviorRuleConditionDTO, BehaviorRulePackDTO


class RuleRegistry:
    """Registry tracking active security behavior rules and rule packs."""

    def __init__(self):
        self._rules: Dict[str, BehaviorRuleDTO] = {
            "RULE-DATAFLOW-001": BehaviorRuleDTO(
                rule_id="RULE-DATAFLOW-001",
                rule_version="1.0.0",
                namespace="DATAFLOW",
                name="Sensitive SMS Data Reaches Network Sink",
                description="Detects SMS permission and SMS API data flowing to a network endpoint.",
                status="ACTIVE",
                severity_hint="HIGH",
                confidence_hint="HIGH",
                prerequisites=["MANIFEST_INTELLIGENCE", "API_INTELLIGENCE"],
                conditions=[
                    BehaviorRuleConditionDTO(condition_id="c1", condition_type="PERMISSION_USED", expected="android.permission.READ_SMS"),
                    BehaviorRuleConditionDTO(condition_id="c2", condition_type="API_CALL", expected="SmsManager"),
                ],
            ),
            "RULE-NETWORK-001": BehaviorRuleDTO(
                rule_id="RULE-NETWORK-001",
                rule_version="1.0.0",
                namespace="NETWORK",
                name="Static Network Endpoint Observed",
                description="Detects static HTTP/HTTPS network endpoint usage.",
                status="ACTIVE",
                severity_hint="MEDIUM",
                confidence_hint="HIGH",
                prerequisites=["NETWORK_INTELLIGENCE"],
                conditions=[
                    BehaviorRuleConditionDTO(condition_id="c3", condition_type="DOMAIN_EXISTS", expected="*"),
                ],
            ),
        }

    def list_active_rules(self) -> List[BehaviorRuleDTO]:
        return [r for r in self._rules.values() if r.status == "ACTIVE"]

    def get_rule_pack(self) -> BehaviorRulePackDTO:
        return BehaviorRulePackDTO(
            pack_id="pack_core_v1",
            pack_version="1.0.0",
            rules_count=len(self._rules),
            checksum="sha256_mock_pack_checksum_v1",
        )
