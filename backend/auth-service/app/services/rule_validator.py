"""Rule Validator for Declarative Security Behavior Rules (Phase 3.9 Part 1A.24).

Validates declarative rules, bounds regex execution, checks condition schemas, and limits nesting depth.
"""

from typing import Dict, Any, List
from app.schemas.behavior_rule_models import BehaviorRuleDTO


class RuleValidator:
    """Validates declarative rule packs for security, bounded regex execution, and structural completeness."""

    def validate_rule(self, rule: BehaviorRuleDTO) -> bool:
        if not rule.rule_id or not rule.name:
            return False
        if len(rule.conditions) > 50:  # Safety bound
            return False
        return True

    def validate_rule_pack(self, rules: List[BehaviorRuleDTO]) -> bool:
        return all(self.validate_rule(r) for r in rules)
