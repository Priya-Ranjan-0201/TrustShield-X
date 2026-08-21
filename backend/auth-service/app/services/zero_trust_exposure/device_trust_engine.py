"""
Device Trust Engine (Phase 34)
==============================
Manages device inventory, posture assessment (OS, patch, encryption, EDR, cert),
quarantine actions, and trust state machine invariants.
"""

from typing import Dict, Any, List, Optional
import datetime


class DeviceTrustEngine:
    def __init__(self):
        self._devices: Dict[str, Dict[str, Any]] = {}

    def register_device(
        self,
        device_id: str,
        tenant_id: str,
        owner_id: str,
        hostname: str,
        os_name: str,
        os_version: str,
        edr_active: bool = False,
        disk_encrypted: bool = False,
        firewall_active: bool = False,
        patch_compliant: bool = True,
        certificate_valid: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        posture_score = 10.0 if (edr_active and disk_encrypted) or (firewall_active and patch_compliant) else 5.0
        trust_state = "TRUSTED" if posture_score >= 8.0 else "CONDITIONAL"
        record = {
            "device_id": device_id,
            "tenant_id": tenant_id,
            "owner_id": owner_id,
            "hostname": hostname,
            "os_name": os_name,
            "os_version": os_version,
            "trust_state": trust_state,
            "encryption_enabled": disk_encrypted or kwargs.get("encryption_enabled", False),
            "disk_encrypted": disk_encrypted,
            "patch_compliant": patch_compliant,
            "edr_active": edr_active,
            "firewall_active": firewall_active,
            "certificate_valid": certificate_valid,
            "posture_score": posture_score,
            "last_posture_assessment": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "quarantine_reason": None,
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        self._devices[device_id] = record
        return record

    def assess_posture(
        self,
        device_id: str,
        tenant_id: str,
        telemetry: Dict[str, Any]
    ) -> Dict[str, Any]:
        dev = self._devices.get(device_id)
        if not dev:
            return {
                "device_id": device_id,
                "tenant_id": tenant_id,
                "trust_state": "DEVICE_UNTRUSTED",
                "posture_score": 0.0,
                "reason": "DEVICE_NOT_REGISTERED"
            }
        
        if dev["tenant_id"] != tenant_id:
            return {
                "device_id": device_id,
                "tenant_id": tenant_id,
                "trust_state": "DEVICE_UNTRUSTED",
                "posture_score": 0.0,
                "reason": "TENANT_MISMATCH_DENIED"
            }

        # Check jailbroken / rooted state
        if telemetry.get("jailbroken") or telemetry.get("rooted"):
            dev["trust_state"] = "UNTRUSTED"
            dev["posture_score"] = 0.0
            dev["quarantine_reason"] = "DEVICE_JAILBROKEN"
            return {
                "device_id": device_id,
                "tenant_id": tenant_id,
                "trust_state": "UNTRUSTED",
                "posture_score": 0.0,
                "quarantine_reason": "DEVICE_JAILBROKEN"
            }

        score = 10.0
        reasons = []

        if not telemetry.get("disk_encrypted", dev.get("disk_encrypted", True)):
            score -= 3.0
            reasons.append("DISK_NOT_ENCRYPTED")
        
        if not telemetry.get("edr_active", dev.get("edr_active", True)):
            score -= 3.5
            reasons.append("EDR_INACTIVE")

        if not telemetry.get("patch_compliant", dev.get("patch_compliant", True)):
            score -= 2.0
            reasons.append("OS_PATCH_OUTDATED")

        if not telemetry.get("certificate_valid", dev.get("certificate_valid", True)):
            score -= 4.0
            reasons.append("CLIENT_CERTIFICATE_INVALID")

        score = max(0.0, score)
        dev["posture_score"] = score
        dev["last_posture_assessment"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

        if score < 4.0:
            dev["trust_state"] = "UNTRUSTED"
        elif score < 7.0:
            dev["trust_state"] = "CONDITIONAL"
        else:
            dev["trust_state"] = "TRUSTED"

        return {
            "device_id": device_id,
            "tenant_id": tenant_id,
            "trust_state": dev["trust_state"],
            "posture_score": score,
            "findings": reasons
        }

    def quarantine_device(
        self,
        device_id: str,
        tenant_id: str,
        reason: str
    ) -> Dict[str, Any]:
        dev = self._devices.get(device_id)
        if not dev or dev["tenant_id"] != tenant_id:
            return {"status": "FAILED", "reason": "DEVICE_NOT_FOUND"}
        
        dev["trust_state"] = "QUARANTINED"
        dev["posture_score"] = 0.0
        dev["quarantine_reason"] = reason
        return {
            "device_id": device_id,
            "tenant_id": tenant_id,
            "trust_state": "QUARANTINED",
            "quarantine_reason": reason
        }

    def get_device(self, device_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        dev = self._devices.get(device_id)
        if dev and dev["tenant_id"] == tenant_id:
            return dev
        return None


device_trust_engine = DeviceTrustEngine()
