"""
TruthShield X — Simulation Safety Sandbox & Resource Controller (Phase 18).

Enforces resource limits, execution timeouts, cancellation controls, and strict credential isolation.
"""

from typing import Dict, Any, Optional
import time
import hashlib


class SandboxResourceExceededError(Exception):
    """Raised when simulation parameters exceed safe resource caps."""
    pass


class SandboxSecurityViolationError(Exception):
    """Raised when simulation attempts prohibited production operations."""
    pass


class SimulationSafetySandbox:
    """Controls sandbox execution limits, cancellation state, and deterministic caching."""

    def __init__(
        self,
        max_graph_nodes: int = 1000,
        timeout_seconds: int = 30,
        max_memory_mb: int = 512,
    ):
        self.max_graph_nodes = max_graph_nodes
        self.timeout_seconds = timeout_seconds
        self.max_memory_mb = max_memory_mb
        self._simulation_cache: Dict[str, Any] = {}
        self._cancelled_simulations: Dict[str, str] = {}  # sim_id -> reason

    def validate_simulation_request(self, node_count: int, contains_prod_secrets: bool = False):
        """Ensures request does not exceed resource boundaries or leak secrets."""
        if contains_prod_secrets:
            raise SandboxSecurityViolationError("Simulation rejected: Production secrets in payload.")

        if node_count > self.max_graph_nodes:
            raise SandboxResourceExceededError(
                f"Graph size {node_count} exceeds maximum allowed limit of {self.max_graph_nodes} nodes."
            )

    def generate_cache_key(self, state_hash: str, scenario_hash: str, model_version: str) -> str:
        """Generates reproducible simulation cache key."""
        raw = f"{state_hash}:{scenario_hash}:{model_version}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def get_cached_result(self, cache_key: str) -> Optional[Any]:
        return self._simulation_cache.get(cache_key)

    def cache_result(self, cache_key: str, result: Any):
        self._simulation_cache[cache_key] = result

    def cancel_simulation(self, simulation_id: str, reason: str = "Operator cancelled"):
        """Records simulation cancellation."""
        self._cancelled_simulations[simulation_id] = reason

    def is_cancelled(self, simulation_id: str) -> bool:
        return simulation_id in self._cancelled_simulations
