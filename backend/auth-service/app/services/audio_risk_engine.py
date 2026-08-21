"""Voice Clone Cybersecurity Risk Aggregation Engine (Phase 3.6 Part 2A-2A-1).

Generates final cybersecurity risk score (0-100) and severity levels:
- 0 to 20: TRUSTED
- 21 to 40: LOW_RISK
- 41 to 60: MEDIUM_RISK
- 61 to 80: HIGH_RISK
- 81 to 100: CRITICAL

Never exposes raw neural probabilities directly to users without risk engine transformation.
Configurable thresholds without hardcoded values in controllers.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class AudioRiskConfig:
    trusted_threshold: int = 20
    low_risk_threshold: int = 40
    medium_risk_threshold: int = 60
    high_risk_threshold: int = 80


@dataclass
class AudioRiskOutput:
    risk_score: int  # 0 to 100
    severity: str    # TRUSTED, LOW_RISK, MEDIUM_RISK, HIGH_RISK, CRITICAL
    risk_label: str
    confidence: float
    explanation: str
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "risk_score": self.risk_score,
            "severity": self.severity,
            "risk_label": self.risk_label,
            "confidence": round(self.confidence, 4),
            "explanation": self.explanation,
            "details": self.details,
        }


class BaseRiskEngine(ABC):
    """Abstract Base Class for Cybersecurity Risk Engines."""

    @abstractmethod
    def compute_risk_score(
        self,
        clone_probability: float,
        calibrated_confidence: float,
        highest_speaker_risk: float,
        average_speaker_risk: float,
        similarity_anomaly: bool = False,
    ) -> AudioRiskOutput:
        pass


class AudioRiskEngine(BaseRiskEngine):
    """Voice Clone Risk Engine with Configurable Thresholds."""

    def __init__(self, config: Optional[AudioRiskConfig] = None):
        self.config = config or AudioRiskConfig()

    def compute_risk_score(
        self,
        clone_probability: float,
        calibrated_confidence: float,
        highest_speaker_risk: float,
        average_speaker_risk: float,
        similarity_anomaly: bool = False,
    ) -> AudioRiskOutput:
        
        # Risk score calculation: 70% highest speaker risk + 30% average speaker risk
        raw_risk = (highest_speaker_risk * 0.70) + (average_speaker_risk * 0.30)
        
        # Boost risk if speaker similarity anomaly is detected
        if similarity_anomaly:
            raw_risk = max(raw_risk, 0.65)

        # Scale risk by calibrated confidence if confidence is low
        if calibrated_confidence < 0.50:
            raw_risk = raw_risk * (calibrated_confidence / 0.50)

        risk_score = max(0, min(100, int(round(raw_risk * 100))))

        # Determine Severity using configurable thresholds
        if risk_score <= self.config.trusted_threshold:
            severity = "TRUSTED"
            label = "Low Synthetic Risk (Natural Voice)"
            exp = "Voice characteristics align with natural human vocal resonance."
        elif risk_score <= self.config.low_risk_threshold:
            severity = "LOW_RISK"
            label = "Low Risk (Minor Signal Variation)"
            exp = "Minor audio acoustic variation detected; unlikely to be synthetic."
        elif risk_score <= self.config.medium_risk_threshold:
            severity = "MEDIUM_RISK"
            label = "Moderate Synthetic Risk"
            exp = "Potential synthetic voice artifacts detected on speaker timeline."
        elif risk_score <= self.config.high_risk_threshold:
            severity = "HIGH_RISK"
            label = "High Synthetic Risk (Probable Clone)"
            exp = "Strong synthetic voice clone indicators detected on active speaker."
        else:
            severity = "CRITICAL"
            label = "Critical Synthetic Scam Risk (Voice Clone Confirmed)"
            exp = "Synthetic AI voice clone confirmed with high neural certainty."

        return AudioRiskOutput(
            risk_score=risk_score,
            severity=severity,
            risk_label=label,
            confidence=calibrated_confidence,
            explanation=exp,
            details={
                "clone_probability": round(clone_probability, 4),
                "highest_speaker_risk": round(highest_speaker_risk, 4),
                "average_speaker_risk": round(average_speaker_risk, 4),
                "similarity_anomaly": similarity_anomaly,
            },
        )
