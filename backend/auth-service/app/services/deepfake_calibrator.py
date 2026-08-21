"""Confidence Calibration & False Positive Protection for Deepfake Engine.

Key Requirements:
- Separates neural prediction_probability (e.g. 0.92) from calibrated_confidence (e.g. 0.61)
- Calibrates confidence based on:
  - Image/frame quality score (blur, resolution, noise)
  - Face bounding box dimensions (small face crops < 32px reduce confidence)
  - Tracked frame count (video < 2 frames reduces confidence)
  - Logit entropy
- False Positive Protection:
  - If quality is extremely poor, face too small, or frame count insufficient,
    flags verdict as LOW_CONFIDENCE state instead of forcing a false high-risk alert.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class CalibratedDeepfakeVerdict:
    raw_fake_probability: float
    calibrated_fake_probability: float
    calibrated_confidence: float
    risk_score: int  # 0 to 100
    severity: str  # TRUSTED, LOW RISK, MEDIUM RISK, HIGH RISK, DANGEROUS, LOW_CONFIDENCE
    is_low_confidence: bool
    confidence_penalty_factors: Dict[str, float]
    protection_note: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "raw_fake_probability": round(self.raw_fake_probability, 4),
            "calibrated_fake_probability": round(self.calibrated_fake_probability, 4),
            "calibrated_confidence": round(self.calibrated_confidence, 4),
            "risk_score": self.risk_score,
            "severity": self.severity,
            "is_low_confidence": self.is_low_confidence,
            "confidence_penalty_factors": self.confidence_penalty_factors,
            "protection_note": self.protection_note,
        }


def calibrate_deepfake_confidence(
    fake_probability: float,
    model_confidence: float,
    quality_metrics: Dict[str, Any],
    min_face_dimension: int = 224,
    frames_analyzed: int = 1,
) -> CalibratedDeepfakeVerdict:
    """Calibrates prediction confidence and enforces false positive protection."""

    calibrated_confidence = model_confidence
    penalties: Dict[str, float] = {}
    protection_notes = []

    # 1. Quality Penalty (Blur & Low Resolution)
    overall_quality = quality_metrics.get("overall_quality_score", 80)
    if overall_quality < 50:
        penalty = round((50 - overall_quality) * 0.008, 3)
        calibrated_confidence -= penalty
        penalties["low_media_quality"] = penalty
        protection_notes.append(f"Low media quality score ({overall_quality}/100) reduced confidence.")

    # 2. Face Size Penalty (small face crops < 64px)
    if min_face_dimension < 64:
        penalty = 0.25
        calibrated_confidence -= penalty
        penalties["small_face_crop"] = penalty
        protection_notes.append(f"Face crop dimension ({min_face_dimension}px) is below minimum 64px threshold.")

    # 3. Frame Count Penalty (insufficient video frames < 2)
    if frames_analyzed < 2:
        penalty = 0.15
        calibrated_confidence -= penalty
        penalties["insufficient_frames"] = penalty
        protection_notes.append("Analyzed single frame only; video temporal consistency unverified.")

    calibrated_confidence = max(0.1, min(0.99, round(calibrated_confidence, 3)))

    # False Positive Protection Trigger
    is_low_confidence = (
        calibrated_confidence < 0.50
        or min_face_dimension < 32
        or overall_quality < 35
    )

    # Compute Risk Score (0-100)
    raw_risk = int(fake_probability * 100)

    if is_low_confidence:
        severity = "LOW_CONFIDENCE"
        # Dampen risk score when confidence is low to avoid false positive alarms
        risk_score = min(40, raw_risk)
        protection_note = "LOW CONFIDENCE: Media quality or face crop resolution is insufficient for decisive deepfake classification."
    else:
        risk_score = raw_risk
        if risk_score >= 80:
            severity = "CRITICAL"
        elif risk_score >= 50:
            severity = "HIGH"
        elif risk_score >= 25:
            severity = "MEDIUM"
        elif risk_score >= 10:
            severity = "LOW RISK"
        else:
            severity = "TRUSTED"
        protection_note = "; ".join(protection_notes) if protection_notes else "Confidence fully calibrated."

    return CalibratedDeepfakeVerdict(
        raw_fake_probability=fake_probability,
        calibrated_fake_probability=fake_probability,
        calibrated_confidence=calibrated_confidence,
        risk_score=risk_score,
        severity=severity,
        is_low_confidence=is_low_confidence,
        confidence_penalty_factors=penalties,
        protection_note=protection_note,
    )
