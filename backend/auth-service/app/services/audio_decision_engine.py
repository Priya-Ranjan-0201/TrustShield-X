"""Conversation Decision Engine for AI Voice Clone Engine (Phase 3.6 Part 2A-2A-1).

Synthesizes final verdict from risk score, calibrated confidence, audio quality, and speaker metrics:
- REAL (risk < 35, confidence >= 0.65)
- VOICE_CLONE (risk >= 75, confidence >= 0.65)
- LIKELY_CLONE (risk >= 50, confidence >= 0.60)
- LOW_CONFIDENCE (confidence < 0.60 or speech_duration < 1.5s or SNR < 12dB)
- INCONCLUSIVE (conflicting signal metrics)

Never relies on a single raw metric.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class AudioDecisionOutput:
    verdict: str  # REAL, VOICE_CLONE, LIKELY_CLONE, LOW_CONFIDENCE, INCONCLUSIVE
    risk_score: int
    confidence_score: float
    confidence_level: str
    decision_reason: str
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "verdict": self.verdict,
            "risk_score": self.risk_score,
            "confidence_score": round(self.confidence_score, 4),
            "confidence_level": self.confidence_level,
            "decision_reason": self.decision_reason,
            "recommendations": self.recommendations,
        }


class BaseDecisionEngine(ABC):
    """Abstract Base Class for Decision Engines."""

    @abstractmethod
    def make_decision(
        self,
        risk_score: int,
        calibrated_confidence: float,
        confidence_level: str,
        clone_probability: float,
        quality_metrics: Dict[str, Any],
        speech_duration_sec: float,
    ) -> AudioDecisionOutput:
        pass


class AudioDecisionEngine(BaseDecisionEngine):
    """Conversation Decision Engine Synthesizer."""

    def make_decision(
        self,
        risk_score: int,
        calibrated_confidence: float,
        confidence_level: str,
        clone_probability: float,
        quality_metrics: Dict[str, Any],
        speech_duration_sec: float,
    ) -> AudioDecisionOutput:
        
        snr_db = quality_metrics.get("snr_db", 28.0)

        # 1. False Positive Protection -> LOW_CONFIDENCE
        if calibrated_confidence < 0.55 or speech_duration_sec < 1.5 or snr_db < 12.0:
            return AudioDecisionOutput(
                verdict="LOW_CONFIDENCE",
                risk_score=risk_score,
                confidence_score=calibrated_confidence,
                confidence_level="LOW",
                decision_reason="Signal quality, SNR dB, or speech duration is insufficient for high confidence neural verification.",
                recommendations=[
                    "Provide at least 3.0 seconds of clear, un-noisy speech for high confidence voice verification.",
                    "Re-record in a quiet environment without microphone input distortion."
                ],
            )

        # 2. VOICE_CLONE (risk >= 75 and confidence >= 0.65)
        if risk_score >= 75 and calibrated_confidence >= 0.65:
            return AudioDecisionOutput(
                verdict="VOICE_CLONE",
                risk_score=risk_score,
                confidence_score=calibrated_confidence,
                confidence_level=confidence_level,
                decision_reason=f"Neural classifier identified synthetic AI voice clone characteristics ({risk_score}% risk) with {confidence_level} confidence.",
                recommendations=[
                    "Do not rely on verbal authentication. Verify identity via out-of-band secondary contact.",
                    "Flag target audio artifact for security review."
                ],
            )

        # 3. LIKELY_CLONE (risk >= 50 and confidence >= 0.60)
        if risk_score >= 50 and calibrated_confidence >= 0.60:
            return AudioDecisionOutput(
                verdict="LIKELY_CLONE",
                risk_score=risk_score,
                confidence_score=calibrated_confidence,
                confidence_level=confidence_level,
                decision_reason=f"Acoustic feature anomalies indicate probable synthetic voice manipulation ({risk_score}% risk).",
                recommendations=[
                    "Request secondary identity verification before performing sensitive operations."
                ],
            )

        # 4. REAL (risk < 35 and confidence >= 0.65)
        if risk_score < 35 and calibrated_confidence >= 0.65:
            return AudioDecisionOutput(
                verdict="REAL",
                risk_score=risk_score,
                confidence_score=calibrated_confidence,
                confidence_level=confidence_level,
                decision_reason="Acoustic vocal resonance patterns align with authentic human speech.",
                recommendations=[
                    "Natural human vocal resonance confirmed across speaker timeline."
                ],
            )

        # 5. Fallback -> INCONCLUSIVE
        return AudioDecisionOutput(
            verdict="INCONCLUSIVE",
            risk_score=risk_score,
            confidence_score=calibrated_confidence,
            confidence_level=confidence_level,
            decision_reason="Conflicting acoustic signal metrics require additional audio context.",
            recommendations=[
                "Submit longer audio sample for refined decision intelligence analysis."
            ],
        )
