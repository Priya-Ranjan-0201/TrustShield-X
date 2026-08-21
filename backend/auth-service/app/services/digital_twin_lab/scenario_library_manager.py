"""
TruthShield X — Scenario Library Manager (Phase 26).

Catalog of pre-packaged safe simulation templates across attacks, failures, and what-if hypotheses.
"""

from typing import Dict, List, Any


class ScenarioLibraryManager:
    """Provides validated scenario templates for rapid what-if security modeling."""

    def __init__(self):
        self._templates: Dict[str, Dict[str, Any]] = {
            "tmpl_ransomware_disruption": {
                "name": "Ransomware Encryptor & Storage Disruption",
                "category": "ATTACK",
                "objective": "Evaluate automated datastore snapshot recovery and lateral isolation.",
                "assumptions": ["Attacker gains execution on internal compute node"],
                "constraints": {"max_affected_nodes": 20},
            },
            "tmpl_waf_control_outage": {
                "name": "Edge WAF Bypass / Control Failure",
                "category": "CONTROL_FAILURE",
                "objective": "Determine secondary defense efficacy if edge WAF service is disabled.",
                "assumptions": ["Edge WAF rule evaluation disabled by configuration error"],
                "constraints": {"max_affected_nodes": 10},
            },
            "tmpl_database_failover_drill": {
                "name": "Primary PostgreSQL Datastore Failure",
                "category": "SERVICE_FAILURE",
                "objective": "Simulate automatic replica promotion and verify zero data corruption.",
                "assumptions": ["Primary node heartbeat timeout triggers failover"],
                "constraints": {"max_affected_nodes": 5},
            },
        }

    def list_templates(self) -> List[Dict[str, Any]]:
        return [{"id": k, **v} for k, v in self._templates.items()]

    def get_template(self, template_id: str) -> Dict[str, Any]:
        return self._templates.get(template_id, {})
