"""Response Provider Adapters & Multi-Vendor Abstraction (Phase 4.0 Part 7 — Sections 40, 86)."""

from typing import List, Dict, Any, Optional, Tuple
from abc import ABC, abstractmethod
from app.schemas.soc_operations_models import ResponseActionDTO


class TargetValidationError(Exception):
    """Raised when action target fails tenant, existence, or safety validation."""
    pass


class ProtectedTargetViolationError(Exception):
    """Raised when action attempts to target protected critical infrastructure."""
    pass


class UnknownExecutionStateError(Exception):
    """Raised when provider execution result is indeterminate due to timeout or communication failure."""
    pass


class ResponseProviderAdapter(ABC):
    """Abstract interface for all security response integrations."""

    @abstractmethod
    def validate_target(self, target: str, target_type: str) -> bool:
        """Verify target syntax and validity."""
        pass

    @abstractmethod
    def dry_run(self, action: ResponseActionDTO) -> Dict[str, Any]:
        """Perform dry-run without external state mutations."""
        pass

    @abstractmethod
    def execute(self, action: ResponseActionDTO) -> Dict[str, Any]:
        """Execute the remediation action against provider API."""
        pass

    @abstractmethod
    def verify(self, action: ResponseActionDTO) -> Tuple[str, str]:
        """Verify empirical containment. Returns (status, observations)."""
        pass

    @abstractmethod
    def rollback(self, action: ResponseActionDTO) -> Tuple[bool, str]:
        """Attempt rollback. Returns (success, reason)."""
        pass


class DNSResponseAdapter(ResponseProviderAdapter):
    """Adapter for DNS sinkholing and domain blocking."""

    def __init__(self, simulate_timeout: bool = False, simulate_unsupported_rollback: bool = False):
        self.blocked_domains: Dict[str, bool] = {}
        self.simulate_timeout = simulate_timeout
        self.simulate_unsupported_rollback = simulate_unsupported_rollback

    def validate_target(self, target: str, target_type: str) -> bool:
        return "." in target and not target.startswith("http")

    def dry_run(self, action: ResponseActionDTO) -> Dict[str, Any]:
        return {"status": "DRY_RUN_SUCCESS", "target": action.target, "action": action.action_type}

    def execute(self, action: ResponseActionDTO) -> Dict[str, Any]:
        if self.simulate_timeout:
            raise UnknownExecutionStateError("DNS API timed out while applying policy. Action state unknown.")
        self.blocked_domains[action.target] = True
        return {"status": "SUCCESS", "message": f"Domain '{action.target}' successfully sinkholed."}

    def verify(self, action: ResponseActionDTO) -> Tuple[str, str]:
        if self.blocked_domains.get(action.target, False):
            return "SUCCESS", f"Verified DNS query for {action.target} resolves to sinkhole 0.0.0.0."
        return "FAILED", f"Domain {action.target} still resolves to public IP."

    def rollback(self, action: ResponseActionDTO) -> Tuple[bool, str]:
        if self.simulate_unsupported_rollback:
            return False, "ROLLBACK_UNAVAILABLE: Provider does not support automated DNS block reversal."
        self.blocked_domains.pop(action.target, None)
        return True, f"Domain {action.target} removed from DNS sinkhole list."


class FirewallResponseAdapter(ResponseProviderAdapter):
    """Adapter for perimeter and border firewalls."""

    def __init__(self):
        self.blocked_ips: Dict[str, bool] = {}

    def validate_target(self, target: str, target_type: str) -> bool:
        return len(target.split(".")) == 4

    def dry_run(self, action: ResponseActionDTO) -> Dict[str, Any]:
        return {"status": "DRY_RUN_SUCCESS", "target": action.target, "action": action.action_type}

    def execute(self, action: ResponseActionDTO) -> Dict[str, Any]:
        self.blocked_ips[action.target] = True
        return {"status": "SUCCESS", "message": f"IP '{action.target}' blocked on ingress/egress firewall."}

    def verify(self, action: ResponseActionDTO) -> Tuple[str, str]:
        if self.blocked_ips.get(action.target, False):
            return "SUCCESS", f"Verified firewall drop rule active for {action.target}."
        return "FAILED", f"Firewall rule missing for {action.target}."

    def rollback(self, action: ResponseActionDTO) -> Tuple[bool, str]:
        self.blocked_ips.pop(action.target, None)
        return True, f"IP {action.target} removed from firewall blocklist."


class EDRResponseAdapter(ResponseProviderAdapter):
    """Adapter for endpoint EDR host isolation and file quarantine."""

    def __init__(self):
        self.isolated_devices: Dict[str, bool] = {}
        self.quarantined_files: Dict[str, bool] = {}

    def validate_target(self, target: str, target_type: str) -> bool:
        return bool(target and len(target) > 2)

    def dry_run(self, action: ResponseActionDTO) -> Dict[str, Any]:
        return {"status": "DRY_RUN_SUCCESS", "target": action.target, "action": action.action_type}

    def execute(self, action: ResponseActionDTO) -> Dict[str, Any]:
        if action.action_type == "ISOLATE_DEVICE":
            self.isolated_devices[action.target] = True
            return {"status": "SUCCESS", "message": f"Device '{action.target}' network-isolated."}
        elif action.action_type == "QUARANTINE_FILE":
            self.quarantined_files[action.target] = True
            return {"status": "SUCCESS", "message": f"File '{action.target}' moved to vault."}
        return {"status": "SUCCESS", "message": "EDR action executed."}

    def verify(self, action: ResponseActionDTO) -> Tuple[str, str]:
        if action.action_type == "ISOLATE_DEVICE" and self.isolated_devices.get(action.target):
            return "SUCCESS", f"Confirmed host {action.target} offline from corporate network."
        if action.action_type == "QUARANTINE_FILE" and self.quarantined_files.get(action.target):
            return "SUCCESS", f"Confirmed file {action.target} inaccessible in quarantine."
        return "FAILED", "EDR action verification failed."

    def rollback(self, action: ResponseActionDTO) -> Tuple[bool, str]:
        if action.action_type == "ISOLATE_DEVICE":
            self.isolated_devices.pop(action.target, None)
            return True, f"Device {action.target} network isolation released."
        return False, "ROLLBACK_UNAVAILABLE: File un-quarantine must be performed manually."
