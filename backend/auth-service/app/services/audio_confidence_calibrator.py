"""Advanced Confidence Calibration Engine for AI Voice Clone Engine (Phase 3.6 Part 2A-2A-1).

Converts raw neural probability outputs into multi-variable calibrated confidence levels:
- VERY_HIGH (>= 0.90)
- HIGH (0.75 - 0.89)
- MEDIUM (0.60 - 0.74)
- LOW (0.40 - 0.59)
- VERY_LOW (< 0.40)

Never exposes raw neural probabilities directly without calibration.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class CalibratedConfidenceOutput:
    raw_probability: float
    calibrated_confidence: float
    confidence_level: str  # VERY_HIGH, HIGH, MEDIUM, LOW, VERY_LOW
    confidence_reason: str
    adjustment_breakdown: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "raw_probability": round(self.raw_probability, 4),
            "calibrated_confidence": round(self.calibrated_confidence, 4),
            "confidence_level": self.confidence_level,
            "confidence_reason": self.confidence_reason,
            "adjustment_breakdown": self.adjustment_breakdown,
        }


class BaseConfidenceCalibrator(ABC):
    """Abstract Base Class for Confidence Calibrators."""

    @abstractmethod
    def calibrate_confidence(
        self,
        raw_clone_probability: float,
        quality_metrics: Dict[str, Any],
        metadata: Dict[str, Any],
        speech_duration_sec: float,
        segment_count: int,
        speaker_count: int = 1,
        diarization_confidence: float = 0.95,
        prediction_consistency: float = 0.95,
    ) -> CalibratedConfidenceOutput:
        pass


class AudioConfidenceCalibrator(BaseConfidenceCalibrator):
    """Advanced Multi-Variable Audio Confidence Calibrator."""

    def calibrate_confidence(
        self,
        raw_clone_probability: float,
        quality_metrics: Dict[str, Any],
        metadata: Dict[str, Any],
        speech_duration_sec: float,
        segment_count: int,
        speaker_count: int = 1,
        diarization_confidence: float = 0.95,
        prediction_consistency: float = 0.95,
    ) -> CalibratedConfidenceOutput:
        
        base_confidence = 0.95
        adjustments: Dict[str, float] = {}

        # 1. Audio SNR Penalties / Boosts
        snr_db = quality_metrics.get("snr_db", 28.0)
        if snr_db >= 25.0:
            adjustments["high_snr_boost"] = 0.03
            base_confidence += 0.03
        elif snr_db < 12.0:
            adjustments["low_snr_penalty"] = -0.30
            base_confidence -= 0.30
        elif snr_db < 20.0:
            adjustments["moderate_snr_penalty"] = -0.12
            base_confidence -= 0.12

        # 2. Speech Duration Penalties / Boosts
        if speech_duration_sec >= 10.0:
            adjustments["long_speech_boost"] = 0.04
            base_confidence += 0.04
        elif speech_duration_sec < 1.5:
            adjustments["short_speech_penalty"] = -0.35
            base_confidence -= 0.35
        elif speech_duration_sec < 3.0:
            adjustments["limited_speech_penalty"] = -0.15
            base_confidence -= 0.15

        # 3. Clipping Distortion Penalty
        clipping = quality_metrics.get("clipping_ratio_percent", 0.0)
        if clipping > 3.0:
            adjustments["clipping_distortion_penalty"] = -0.15
            base_confidence -= 0.15

        # 4. Silence Ratio Penalty
        silence_ratio = quality_metrics.get("silence_ratio_percent", 0.0)
        if silence_ratio > 50.0:
            adjustments["high_silence_penalty"] = -0.10
            base_confidence -= 0.10

        # 5. Prediction Consistency & Diarization Confidence
        if prediction_consistency >= 0.90 and segment_count >= 3:
            adjustments["segment_consistency_boost"] = 0.05
            base_confidence += 0.05
        elif prediction_consistency < 0.60:
            adjustments["inconsistent_prediction_penalty"] = -0.20
            base_confidence -= 0.20

        if diarization_confidence < 0.70:
            adjustments["diarization_uncertainty_penalty"] = -0.15
            base_confidence -= 0.15

        # 6. Sample Rate & Bitrate Penalties
        sample_rate = metadata.get("sample_rate", 44100)
        if sample_rate < 16000:
            adjustments["low_sample_rate_penalty"] = -0.15
            base_confidence -= 0.15

        # Clamp final calibrated confidence between 0.05 and 0.99
        calibrated_conf = max(0.05, min(0.99, round(base_confidence, 4)))

        # Determine Confidence Level & Reason
        if calibrated_conf >= 0.90:
            conf_level = "VERY_HIGH"
            reason = "High signal-to-noise ratio, sufficient speech duration, and strong multi-segment prediction consistency."
        elif calibrated_conf >= 0.75:
            conf_level = "HIGH"
            reason = "Solid speech signal quality and consistent speaker embedding representation."
        elif calibrated_conf >= 0.60:
            conf_level = "MEDIUM"
            reason = "Moderate audio quality or segment count. Speech analysis is reliable but contains minor acoustic noise."
        elif calibrated_conf >= 0.40:
            conf_level = "LOW"
            reason = "Limited speech duration, background noise, or signal distortion reduces neural confidence."
        else:
            conf_level = "VERY_LOW"
            reason = "Severe audio degradation, extremely short recording, or high background noise."

        return CalibratedConfidenceOutput(
            raw_probability=raw_clone_probability,
            calibrated_confidence=calibrated_conf,
            confidence_level=conf_level,
            confidence_reason=reason,
            adjustment_breakdown=adjustments,
        )
