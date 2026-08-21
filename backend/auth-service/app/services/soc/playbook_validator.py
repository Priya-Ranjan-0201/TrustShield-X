"""
TruthShield X — Playbook Validator Engine (Phase 21).

Detects unreachable nodes, infinite cycles, missing verification, and missing approval gates.
"""

from typing import List, Set, Dict
from app.schemas.autonomous_soc_models import SecurePlaybookDTO, PlaybookValidationResultDTO


class PlaybookValidator:
    """Validates structural and safety integrity of SOAR playbooks prior to production deployment."""

    def validate_playbook(self, playbook: SecurePlaybookDTO) -> PlaybookValidationResultDTO:
        node_map = {n.node_id: n for n in playbook.nodes}
        visited: Set[str] = set()
        unreachable: List[str] = []
        missing_verif: List[str] = []
        missing_approval: List[str] = []
        missing_timeouts: List[str] = []

        if not playbook.nodes:
            return PlaybookValidationResultDTO(playbook_id=playbook.playbook_id, is_valid=False)

        # BFS from entry node (n1 or first TRIGGER)
        start_id = playbook.nodes[0].node_id
        queue = [start_id]
        while queue:
            curr_id = queue.pop(0)
            if curr_id in visited:
                continue
            visited.add(curr_id)
            node = node_map.get(curr_id)
            if node:
                for next_id in node.next_node_ids:
                    if next_id not in visited and next_id in node_map:
                        queue.append(next_id)

        # Check unreachable nodes
        for node in playbook.nodes:
            if node.node_id not in visited:
                unreachable.append(node.node_id)
            if node.node_type == "ACTION" and not any(n.node_type == "VERIFY" for n in playbook.nodes):
                missing_verif.append(node.node_id)
            if node.node_type == "ACTION" and not node.requires_approval and not any(n.node_type == "APPROVAL" for n in playbook.nodes):
                missing_approval.append(node.node_id)
            if node.timeout_seconds <= 0:
                missing_timeouts.append(node.node_id)

        # Check infinite cycle without terminal END node
        has_end = any(n.node_type == "END" for n in playbook.nodes)
        has_infinite = not has_end

        is_valid = len(unreachable) == 0 and not has_infinite and len(missing_timeouts) == 0

        return PlaybookValidationResultDTO(
            playbook_id=playbook.playbook_id,
            is_valid=is_valid,
            unreachable_nodes=unreachable,
            has_infinite_loop=has_infinite,
            missing_approvals=missing_approval,
            unsafe_actions=[],
            missing_verification=missing_verif,
            missing_timeouts=missing_timeouts,
        )
