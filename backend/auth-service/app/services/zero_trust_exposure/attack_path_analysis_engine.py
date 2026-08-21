"""
Attack Path Analysis & Exposure Graph Engine (Phase 34)
========================================================
Models multi-stage attack paths:
(ENTRY_POINT -> ASSET -> VULNERABILITY -> CREDENTIAL -> PRIVILEGE -> LATERAL_MOVEMENT -> HIGH_VALUE_ASSET / CROWN_JEWEL)
Path Types: NETWORK, IDENTITY, APPLICATION, CLOUD, DATA, SERVICE, HYBRID.
Enforces reachability verification invariants (ATTACK_PATH_UNVERIFIED fallback).
AI-generated paths default to CANDIDATE_ATTACK_PATH until validated with reachability proof.
"""

from typing import Dict, Any, List, Optional
import datetime
from app.schemas.zero_trust_exposure_models import AttackPathDTO


class AttackPathAnalysisEngine:
    VALID_PATH_TYPES = {"NETWORK", "IDENTITY", "APPLICATION", "CLOUD", "DATA", "SERVICE", "HYBRID"}

    def __init__(self):
        self._attack_paths: Dict[str, Dict[str, Any]] = {}

    def analyze_path(
        self,
        path_id: str,
        tenant_id: str,
        entry_point: str,
        target_crown_jewel: str,
        path_type: str = "NETWORK",
        nodes: Optional[List[Any]] = None,
        edges: Optional[List[Any]] = None,
        evidence: Optional[List[Any]] = None,
        is_ai_generated: bool = False,
        is_simulation: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        p_type = path_type.upper() if path_type.upper() in self.VALID_PATH_TYPES else path_type
        has_evidence = evidence is not None and len(evidence) > 0
        reachability_verified = all(
            (e.get("reachability_confirmed", False) or e.get("reachability_proven", False))
            for e in (evidence or []) if isinstance(e, dict)
        ) if has_evidence else False

        if is_simulation:
            status = "SIMULATED"
            feasibility = "SIMULATED"
            validation_status = "SIMULATION_ISOLATED"
        elif is_ai_generated and not reachability_verified:
            status = "CANDIDATE_ATTACK_PATH"
            feasibility = "SPECULATIVE"
            validation_status = "AI_PATH_UNVERIFIED"
        elif not reachability_verified:
            status = "ATTACK_PATH_UNVERIFIED"
            feasibility = "UNVERIFIED"
            validation_status = "ATTACK_PATH_UNVERIFIED"
        else:
            status = "VERIFIED"
            feasibility = "VERIFIED"
            validation_status = "DETERMINISTIC_PROOF_CONFIRMED"

        risk_score = 9.0 if status == "VERIFIED" else 6.0 if status == "PROBABLE" else 4.0 if status == "SIMULATED" else 2.0

        path = {
            "path_id": path_id,
            "tenant_id": tenant_id,
            "entry_point": entry_point,
            "target_crown_jewel": target_crown_jewel,
            "path_type": p_type,
            "nodes": nodes or [],
            "edges": edges or [],
            "status": status,
            "feasibility": feasibility,
            "validation_status": validation_status,
            "reachability_verified": reachability_verified,
            "evidence": evidence or [],
            "risk_score": risk_score,
            "is_ai_generated": is_ai_generated,
            "is_simulation": is_simulation,
            "discovered_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        self._attack_paths[path_id] = path
        return path


    def validate_ai_candidate_path(
        self,
        path_id: str,
        tenant_id: str,
        verification_evidence: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        path = self._attack_paths.get(path_id)
        if not path or path["tenant_id"] != tenant_id:
            return {"status": "FAILED", "reason": "PATH_NOT_FOUND"}

        all_verified = all(e.get("reachability_confirmed", False) for e in verification_evidence)
        if all_verified and len(verification_evidence) > 0:
            path["status"] = "VERIFIED"
            path["reachability_verified"] = True
            path["evidence"] = verification_evidence
            path["risk_score"] = 9.5
        else:
            path["status"] = "ATTACK_PATH_UNVERIFIED"
            path["reachability_verified"] = False

        return path

    def get_paths(self, tenant_id: str) -> List[Dict[str, Any]]:
        return [p for p in self._attack_paths.values() if p["tenant_id"] == tenant_id]

    def get_path(self, path_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        path = self._attack_paths.get(path_id)
        if path and path["tenant_id"] == tenant_id:
            return path
        return None


attack_path_analysis_engine = AttackPathAnalysisEngine()
