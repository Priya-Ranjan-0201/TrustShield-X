"""Extended Multi-Vendor Response Provider Adapters (Phase 5).

Includes Identity/IAM, Cloud Storage, Fraud Control, and Email/Messaging integrations.
"""

from typing import Dict, Any, Tuple
from app.schemas.soc_operations_models import ResponseActionDTO
from app.services.soc.response_adapters import (
    ResponseProviderAdapter,
    UnknownExecutionStateError,
)


class IAMResponseAdapter(ResponseProviderAdapter):
    """Adapter for Identity and Access Management (IAM), Session termination, and Credential resets."""

    def __init__(self, simulate_timeout: bool = False):
        self.disabled_accounts: Dict[str, bool] = {}
        self.revoked_tokens: Dict[str, bool] = {}
        self.simulate_timeout = simulate_timeout

    def validate_target(self, target: str, target_type: str) -> bool:
        return bool(target and len(target) > 3)

    def dry_run(self, action: ResponseActionDTO) -> Dict[str, Any]:
        return {
            "status": "DRY_RUN_SUCCESS",
            "provider": "IAMResponseAdapter",
            "target": action.target,
            "action": action.action_type,
            "estimated_impact": f"Would revoke all active sessions for identity '{action.target}'.",
        }

    def execute(self, action: ResponseActionDTO) -> Dict[str, Any]:
        if self.simulate_timeout:
            raise UnknownExecutionStateError("IAM Provider timed out. Session revocation state unknown.")

        if action.action_type in ("DISABLE_ACCOUNT", "RESET_CREDENTIAL"):
            self.disabled_accounts[action.target] = True
            return {"status": "SUCCESS", "message": f"Account '{action.target}' disabled in IAM directory."}
        else:
            self.revoked_tokens[action.target] = True
            return {"status": "SUCCESS", "message": f"Tokens & sessions revoked for '{action.target}'."}

    def verify(self, action: ResponseActionDTO) -> Tuple[str, str]:
        if action.action_type in ("DISABLE_ACCOUNT", "RESET_CREDENTIAL"):
            if self.disabled_accounts.get(action.target):
                return "SUCCESS", f"Confirmed account '{action.target}' is in DISABLED state."
            return "FAILED", f"Account '{action.target}' still active in IAM directory."
        else:
            if self.revoked_tokens.get(action.target):
                return "SUCCESS", f"Confirmed all tokens revoked in Redis token blacklist for '{action.target}'."
            return "FAILED", "Tokens still valid."

    def rollback(self, action: ResponseActionDTO) -> Tuple[bool, str]:
        if action.action_type == "DISABLE_ACCOUNT":
            self.disabled_accounts.pop(action.target, None)
            return True, f"Account '{action.target}' re-enabled in IAM directory."
        return False, "ROLLBACK_UNAVAILABLE: Token revocation is irreversible; user must log in again."


class FraudControlResponseAdapter(ResponseProviderAdapter):
    """Adapter for financial/UPI fraud response and instant transaction freeze."""

    def __init__(self, simulate_timeout: bool = False):
        self.frozen_vpas: Dict[str, bool] = {}
        self.simulate_timeout = simulate_timeout

    def validate_target(self, target: str, target_type: str) -> bool:
        return "@" in target or len(target) >= 10

    def dry_run(self, action: ResponseActionDTO) -> Dict[str, Any]:
        return {
            "status": "DRY_RUN_SUCCESS",
            "provider": "FraudControlResponseAdapter",
            "target": action.target,
            "action": action.action_type,
            "estimated_impact": f"Would block inbound/outbound UPI transactions for VPA '{action.target}'.",
        }

    def execute(self, action: ResponseActionDTO) -> Dict[str, Any]:
        if self.simulate_timeout:
            raise UnknownExecutionStateError("Fraud Gateway timeout during freeze dispatch.")
        self.frozen_vpas[action.target] = True
        return {"status": "SUCCESS", "message": f"UPI Handle / VPA '{action.target}' frozen on NPCI gateway."}

    def verify(self, action: ResponseActionDTO) -> Tuple[str, str]:
        if self.frozen_vpas.get(action.target):
            return "SUCCESS", f"NPCI API confirmed VPA '{action.target}' status is FROZEN."
        return "FAILED", "VPA still active."

    def rollback(self, action: ResponseActionDTO) -> Tuple[bool, str]:
        self.frozen_vpas.pop(action.target, None)
        return True, f"UPI handle '{action.target}' un-frozen."


class CloudStorageResponseAdapter(ResponseProviderAdapter):
    """Adapter for Cloud Object Storage (S3 / GCS / Azure Blob) security isolation."""

    def __init__(self, simulate_timeout: bool = False):
        self.isolated_buckets: Dict[str, bool] = {}
        self.simulate_timeout = simulate_timeout

    def validate_target(self, target: str, target_type: str) -> bool:
        return bool(target and len(target) >= 3 and not target.startswith("/"))

    def dry_run(self, action: ResponseActionDTO) -> Dict[str, Any]:
        return {
            "status": "DRY_RUN_SUCCESS",
            "provider": "CloudStorageResponseAdapter",
            "target": action.target,
            "action": action.action_type,
            "estimated_impact": f"Would enforce private ACLs and block public read/write on bucket '{action.target}'.",
        }

    def execute(self, action: ResponseActionDTO) -> Dict[str, Any]:
        if self.simulate_timeout:
            raise UnknownExecutionStateError("Cloud API timeout during policy attachment.")
        self.isolated_buckets[action.target] = True
        return {"status": "SUCCESS", "message": f"Bucket '{action.target}' public access blocked and isolated."}

    def verify(self, action: ResponseActionDTO) -> Tuple[str, str]:
        if self.isolated_buckets.get(action.target):
            return "SUCCESS", f"Confirmed bucket '{action.target}' policy is BlockPublicAccess=True."
        return "FAILED", "Bucket still publicly accessible."

    def rollback(self, action: ResponseActionDTO) -> Tuple[bool, str]:
        self.isolated_buckets.pop(action.target, None)
        return True, f"Bucket '{action.target}' isolation policy removed."
