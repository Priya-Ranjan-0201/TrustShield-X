"""Response Simulation & Dry-Run Engine (Phase 4.0 Part 7 — Sections 37-38).

Simulates playbook workflows and remediation actions with zero external side effects.
"""

from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime, timezone
from app.schemas.soc_operations_models import (
    ResponseActionDTO,
    ResponseSimulationDTO,
    ResponsePlaybookDTO,
    SecurityIncidentDTO,
)


class ResponseSimulationEngine:
    """Performs non-destructive dry-run simulation of response actions and playbooks."""

    @staticmethod
    def simulate_action(action: ResponseActionDTO) -> ResponseSimulationDTO:
        act_type = action.action_type
        target = action.target

        # Derive expected effect and risk assessment
        effects: Dict[str, Dict[str, Any]] = {
            "BLOCK_DOMAIN": {
                "provider": "Edge-DNS-WAF-Adapter",
                "expected_effect": f"Sinkhole DNS resolution and inject block page for domain '{target}'.",
                "risk": "High impact if target is a shared service or false positive.",
                "permissions": ["soc:response:execute", "dns:write"],
                "rollback": True,
                "side_effects": ["Legitimate users visiting domain will receive connection errors."],
            },
            "BLOCK_IP": {
                "provider": "Core-Firewall-Adapter",
                "expected_effect": f"Drop inbound and outbound traffic at border firewall for IP '{target}'.",
                "risk": "High impact; may affect collocated services on shared IP.",
                "permissions": ["soc:response:execute", "firewall:write"],
                "rollback": True,
                "side_effects": ["All TCP/UDP traffic to target IP rejected."],
            },
            "QUARANTINE_FILE": {
                "provider": "Endpoint-EDR-Adapter",
                "expected_effect": f"Move file '{target}' to encrypted quarantine vault.",
                "risk": "Medium impact; application may crash if file is a required dependency.",
                "permissions": ["soc:response:execute", "endpoint:quarantine"],
                "rollback": True,
                "side_effects": ["File inaccessible to local OS processes."],
            },
            "ISOLATE_DEVICE": {
                "provider": "Network-NAC-Adapter",
                "expected_effect": f"Quarantine host '{target}' into restricted VLAN with zero internet access.",
                "risk": "Critical impact; user on device will lose all productivity access.",
                "permissions": ["soc:response:execute", "network:isolate"],
                "rollback": True,
                "side_effects": ["Host disconnected from corporate LAN and internet."],
            },
            "REVOKE_TOKEN": {
                "provider": "IAM-Auth-Adapter",
                "expected_effect": f"Invalidate active refresh tokens and sessions for user/token '{target}'.",
                "risk": "Low/Medium impact; forces user re-authentication.",
                "permissions": ["soc:response:execute", "iam:revoke"],
                "rollback": False,
                "side_effects": ["Active sessions terminated immediately."],
            },
        }

        meta = effects.get(act_type, {
            "provider": "Generic-SOAR-Adapter",
            "expected_effect": f"Execute action '{act_type}' on target '{target}'.",
            "risk": "Low/Standard impact.",
            "permissions": ["soc:response:execute"],
            "rollback": False,
            "side_effects": [],
        })

        return ResponseSimulationDTO(
            simulation_id=f"sim_{uuid.uuid4().hex[:12]}",
            action_id=action.action_id,
            target=target,
            provider=meta["provider"],
            expected_effect=meta["expected_effect"],
            risk_assessment=meta["risk"],
            required_permissions=meta["permissions"],
            rollback_supported=meta["rollback"],
            side_effects=meta["side_effects"],
        )

    @staticmethod
    def simulate_playbook(playbook: ResponsePlaybookDTO, incident: SecurityIncidentDTO) -> Dict[str, Any]:
        """Simulate an entire response playbook against an incident."""
        simulated_steps = []
        requires_human_approval = False

        for step in playbook.steps:
            if step.approval_required:
                requires_human_approval = True

            simulated_steps.append({
                "step_number": step.step_number,
                "name": step.name,
                "action_type": step.action_type,
                "risk_level": step.risk_level,
                "approval_required": step.approval_required,
                "dry_run_supported": step.dry_run_supported,
                "rollback_supported": step.rollback_supported,
                "expected_outcome": f"Would execute {step.action_type} for incident {incident.incident_number}",
            })

        return {
            "playbook_id": playbook.playbook_id,
            "playbook_version": playbook.current_version,
            "incident_id": incident.incident_id,
            "total_steps": len(playbook.steps),
            "requires_human_approval": requires_human_approval,
            "simulated_steps": simulated_steps,
            "safety_verdict": "SIMULATION_PASSED_ZERO_EXTERNAL_MUTATIONS",
        }
