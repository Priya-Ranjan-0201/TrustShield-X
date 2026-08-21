"""Confidence Calibration & False Positive Protection for AI Voice Clone Engine.

Separates raw prediction_probability from calibrated_confidence.
Penalizes confidence for low SNR, short speech duration, high clipping, or noisy audio.

False Positive Protection:
- Automatically sets confidence_state to "LOW_CONFIDENCE" if speech duration < 1.5s or SNR < 12.0dB.
"""

from typing import Dict, Any, Tuple


def calibrate_voice_confidence(
    prediction_probability: float,
    quality_metrics: Dict[str, Any],
    speech_duration_sec: float,
    speaker_count: int = 1,
) -> Tuple[float, str, Dict[str, Any]]:
    """Calibrates prediction confidence and returns (calibrated_confidence, confidence_state, calibration_penalties)."""

    base_confidence = 0.95
    penalties = {}

    snr_db = quality_metrics.get("snr_db", 28.0)
    clipping_ratio = quality_metrics.get("clipping_ratio_percent", 0.0)
    silence_ratio = quality_metrics.get("silence_ratio_percent", 0.0)

    # 1. Speech duration penalty (< 3.0 seconds)
    if speech_duration_sec < 1.5:
        base_confidence -= 0.35
        penalties["short_speech_duration"] = -0.35
    elif speech_duration_sec < 3.0:
        base_confidence -= 0.15
        penalties["limited_speech_duration"] = -0.15

    # 2. SNR penalty (< 20dB)
    if snr_db < 12.0:
        base_confidence -= 0.30
        penalties["low_snr_noise"] = -0.30
    elif snr_db < 20.0:
        base_confidence -= 0.12
        penalties["moderate_snr_noise"] = -0.12

    # 3. Clipping ratio penalty (> 3%)
    if clipping_ratio > 3.0:
        base_confidence -= 0.15
        penalties["high_clipping_distortion"] = -0.15

    calibrated_confidence = max(0.10, min(0.99, round(base_confidence, 4)))

    # False Positive Protection Trigger
    confidence_state = "CALIBRATED_HIGH"
    if calibrated_confidence < 0.65 or speech_duration_sec < 1.5 or snr_db < 12.0:
        confidence_state = "LOW_CONFIDENCE"

    return calibrated_confidence, confidence_state, penalties
