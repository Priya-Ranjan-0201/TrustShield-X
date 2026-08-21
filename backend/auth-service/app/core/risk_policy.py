"""Centralized Risk Policy Configuration (Phase 3.9 Part 1B).

Contains configurable numeric parameters, thresholds, risk bands, ceilings, floors, and modifiers.
"""

from typing import Dict, Any


class RiskPolicy:
    """Centralized Enterprise Risk Policy."""

    POLICY_VERSION: str = "1.0.0"

    # Configurable Risk Band Thresholds
    BAND_THRESHOLDS: Dict[str, tuple[float, float]] = {
        "TRUSTED": (0.0, 20.0),
        "LOW_RISK": (20.01, 40.0),
        "MODERATE_RISK": (40.01, 60.0),
        "HIGH_RISK": (60.01, 80.0),
        "CRITICAL_RISK": (80.01, 100.0),
    }

    # Confidence Modifiers
    CONFIDENCE_MODIFIERS: Dict[str, float] = {
        "VERY_HIGH": 1.0,
        "HIGH": 0.9,
        "MEDIUM": 0.7,
        "LOW": 0.4,
        "VERY_LOW": 0.2,
        "UNKNOWN": 0.5,
    }

    # Freshness Modifiers
    FRESHNESS_MODIFIERS: Dict[str, float] = {
        "CURRENT": 1.0,
        "RECENT": 0.8,
        "STALE": 0.5,
        "EXPIRED": 0.1,
        "UNKNOWN": 0.5,
    }

    # Risk Caps & Ceilings
    MAX_SCORE: float = 100.0
    MIN_SCORE: float = 0.0
    MAX_CATEGORY_SCORE: float = 40.0
    MAX_INTERACTION_BONUS: float = 15.0
    UNRESOLVED_REFLECTION_CAP: float = 60.0
    UNRESOLVED_JNI_CAP: float = 60.0
