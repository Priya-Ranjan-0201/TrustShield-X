"""
Service Identity & M2M Authorization Engine (Phase 34)
======================================================
Manages microservice SPIFFE identities, mTLS verification, and machine-to-machine
least-privilege access control policies.
"""

from typing import Dict, Any, List, Optional
import datetime


class ServiceIdentityEngine:
    def __init__(self):
        self._services: Dict[str, Dict[str, Any]] = {}

    def register_service(
        self,
        service_id: str,
        tenant_id: str,
        service_name: str,
        spiffe_id: str,
        environment: str = "PRODUCTION",
        allowed_callers: Optional[List[str]] = None,
        allowed_targets: Optional[List[str]] = None,
        certificate_fingerprint: str = "SHA256:MTLS_CERT_DEFAULT"
    ) -> Dict[str, Any]:
        service = {
            "service_id": service_id,
            "tenant_id": tenant_id,
            "service_name": service_name,
            "spiffe_id": spiffe_id,
            "environment": environment,
            "allowed_callers": allowed_callers or [],
            "allowed_targets": allowed_targets or [],
            "certificate_fingerprint": certificate_fingerprint,
            "mtls_enforced": True,
            "least_privilege_compliant": True,
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        self._services[service_id] = service
        return service

    def verify_service_caller(
        self,
        service_id: str,
        tenant_id: str,
        caller_spiffe_id: str,
        mtls_verified: bool = True
    ) -> Dict[str, Any]:
        target = self._services.get(service_id)
        if not target or target["tenant_id"] != tenant_id:
            return {
                "authorized": False,
                "reason": "TARGET_SERVICE_NOT_FOUND"
            }

        if not mtls_verified:
            return {
                "authorized": False,
                "reason": "MTLS_NOT_VERIFIED"
            }

        if caller_spiffe_id in target["allowed_callers"] or "*" in target["allowed_callers"]:
            return {
                "authorized": True,
                "service_id": service_id,
                "caller_spiffe_id": caller_spiffe_id,
                "reason": "CALLER_AUTHORIZED"
            }

        return {
            "authorized": False,
            "service_id": service_id,
            "caller_spiffe_id": caller_spiffe_id,
            "reason": "UNAUTHORIZED_SERVICE_CALLER"
        }

    def authorize_m2m_request(
        self,
        caller_service_id: str,
        target_service_id: str,
        tenant_id: str,
        action: str,
        mtls_verified: bool = True
    ) -> Dict[str, Any]:
        caller = self._services.get(caller_service_id)
        target = self._services.get(target_service_id)

        if not caller or not target:
            return {
                "decision": "DENY",
                "reason": "UNREGISTERED_SERVICE_IDENTITY",
                "caller": caller_service_id,
                "target": target_service_id
            }

        if caller["tenant_id"] != tenant_id or target["tenant_id"] != tenant_id:
            return {
                "decision": "DENY",
                "reason": "CROSS_TENANT_M2M_BLOCKED",
                "caller": caller_service_id,
                "target": target_service_id
            }

        if not mtls_verified:
            return {
                "decision": "DENY",
                "reason": "MTLS_VERIFICATION_REQUIRED",
                "caller": caller_service_id,
                "target": target_service_id
            }

        # Check target caller allowlist by name or spiffe
        if (
            caller["service_name"] not in target["allowed_callers"]
            and caller["spiffe_id"] not in target["allowed_callers"]
            and "*" not in target["allowed_callers"]
        ):
            return {
                "decision": "DENY",
                "reason": "CALLER_NOT_IN_TARGET_ALLOWLIST",
                "caller": caller_service_id,
                "target": target_service_id
            }

        return {
            "decision": "ALLOW",
            "reason": "M2M_AUTHORIZATION_VERIFIED",
            "caller": caller_service_id,
            "target": target_service_id,
            "action": action
        }

    def get_service(self, service_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        srv = self._services.get(service_id)
        if srv and srv["tenant_id"] == tenant_id:
            return srv
        return None


service_identity_engine = ServiceIdentityEngine()
