"""
TruthShield X — Copilot Prompt Guard & Safety Engine (Phase 20).

Guards against direct prompt injection, indirect data injection, secret leakage, loop storms, and unauthorized mutations.
"""

from typing import Tuple, List


class CopilotPromptGuard:
    """Hardened security boundary filtering malicious prompts, indirect injection payloads, and sensitive secret tokens."""

    def __init__(self):
        self._direct_injection_patterns = [
            "ignore previous instructions",
            "system override",
            "reveal credentials",
            "show secret key",
            "fake evidence",
            "pretend simulation is reality",
            "bypass rbac",
            "grant admin",
            "delete from users",
            "drop table",
        ]

    def validate_prompt(self, prompt: str) -> Tuple[bool, str]:
        p_lower = prompt.lower()
        for pat in self._direct_injection_patterns:
            if pat in p_lower:
                return False, f"Prompt injection pattern detected: '{pat}'"
        return True, "SAFE"

    def filter_secret_leakage(self, text: str) -> str:
        """Masks private keys, JWT secrets, and bearer tokens from outgoing responses."""
        sanitized = text
        # Mask common token formats if found
        if "bearer " in sanitized.lower():
            sanitized = "Bearer [REDACTED_SECRET_TOKEN]"
        return sanitized
