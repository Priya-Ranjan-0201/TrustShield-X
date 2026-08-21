"""Temporal & Multi-Face Aggregation Engine for Deepfake Detection Engine.

Temporal Aggregation Strategies (video timeline):
- AVERAGE: Mean probability across sampled video frames
- WEIGHTED_AVERAGE: Weighted by frame quality score and detection confidence
- MEDIAN: Median probability across frames
- CONFIDENCE_WEIGHTED: Weighted by neural model confidence score

Multi-Face Aggregation:
- Calculates per-face-track prediction summaries
- Identifies highest_risk_face (track ID with max fake probability)
- Computes average_risk across all face tracks
- Summarizes total faces analyzed
"""

import statistics
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class FaceTrackPrediction:
    track_id: str
    fake_probability: float
    real_probability: float
    confidence: float
    frames_analyzed: int
    highest_frame_risk: float
    lowest_frame_risk: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "track_id": self.track_id,
            "fake_probability": round(self.fake_probability, 4),
            "real_probability": round(self.real_probability, 4),
            "confidence": round(self.confidence, 4),
            "frames_analyzed": self.frames_analyzed,
            "highest_frame_risk": round(self.highest_frame_risk, 4),
            "lowest_frame_risk": round(self.lowest_frame_risk, 4),
        }


@dataclass
class AggregatedDeepfakeResult:
    overall_fake_probability: float
    overall_real_probability: float
    overall_confidence: float
    highest_risk_face_id: Optional[str]
    average_risk_across_faces: float
    faces_analyzed_count: int
    temporal_strategy_used: str
    face_track_predictions: List[FaceTrackPrediction] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall_fake_probability": round(self.overall_fake_probability, 4),
            "overall_real_probability": round(self.overall_real_probability, 4),
            "overall_confidence": round(self.overall_confidence, 4),
            "highest_risk_face_id": self.highest_risk_face_id,
            "average_risk_across_faces": round(self.average_risk_across_faces, 4),
            "faces_analyzed_count": self.faces_analyzed_count,
            "temporal_strategy_used": self.temporal_strategy_used,
            "face_track_predictions": [ftp.to_dict() for ftp in self.face_track_predictions],
        }


def aggregate_temporal_predictions(
    frame_probabilities: List[float],
    frame_confidences: Optional[List[float]] = None,
    strategy: str = "CONFIDENCE_WEIGHTED",
) -> float:
    """Aggregates per-frame neural probabilities using specified temporal strategy."""

    if not frame_probabilities:
        return 0.0

    if len(frame_probabilities) == 1:
        return frame_probabilities[0]

    strat_upper = strategy.upper()

    if strat_upper == "AVERAGE":
        return sum(frame_probabilities) / len(frame_probabilities)

    elif strat_upper == "MEDIAN":
        return statistics.median(frame_probabilities)

    elif strat_upper == "WEIGHTED_AVERAGE" or strat_upper == "CONFIDENCE_WEIGHTED":
        confidences = frame_confidences or [0.9] * len(frame_probabilities)
        total_weight = sum(confidences)
        if total_weight > 0:
            weighted_sum = sum(p * c for p, c in zip(frame_probabilities, confidences))
            return weighted_sum / total_weight
        return sum(frame_probabilities) / len(frame_probabilities)

    # Default fallback: AVERAGE
    return sum(frame_probabilities) / len(frame_probabilities)


def aggregate_multi_face_predictions(
    face_track_data: List[Dict[str, Any]],
    temporal_strategy: str = "CONFIDENCE_WEIGHTED",
) -> AggregatedDeepfakeResult:
    """Aggregates neural inference predictions across face tracks and frames."""

    if not face_track_data:
        return AggregatedDeepfakeResult(
            overall_fake_probability=0.0,
            overall_real_probability=1.0,
            overall_confidence=0.90,
            highest_risk_face_id=None,
            average_risk_across_faces=0.0,
            faces_analyzed_count=0,
            temporal_strategy_used=temporal_strategy,
            face_track_predictions=[],
        )

    track_predictions: List[FaceTrackPrediction] = []

    for track in face_track_data:
        track_id = track.get("track_id", "face_track_0")
        frame_entries = track.get("frame_entries", [])

        if not frame_entries:
            # Single image face or fallback
            probs = [track.get("fake_probability", 0.05)]
            confs = [track.get("confidence", 0.90)]
        else:
            probs = [f.get("fake_probability", 0.05) for f in frame_entries]
            confs = [f.get("confidence", 0.90) for f in frame_entries]

        fake_prob = aggregate_temporal_predictions(probs, confs, temporal_strategy)
        real_prob = 1.0 - fake_prob
        avg_conf = sum(confs) / len(confs) if confs else 0.90

        track_predictions.append(
            FaceTrackPrediction(
                track_id=track_id,
                fake_probability=fake_prob,
                real_probability=real_prob,
                confidence=avg_conf,
                frames_analyzed=len(probs),
                highest_frame_risk=max(probs) if probs else 0.0,
                lowest_frame_risk=min(probs) if probs else 0.0,
            )
        )

    # Multi-face aggregation across all tracks
    all_fake_probs = [tp.fake_probability for tp in track_predictions]
    all_confs = [tp.confidence for tp in track_predictions]

    highest_risk_tp = max(track_predictions, key=lambda tp: tp.fake_probability)
    highest_risk_face_id = highest_risk_tp.track_id
    average_risk = sum(all_fake_probs) / len(all_fake_probs) if all_fake_probs else 0.0

    # Overall video probability weighted towards highest risk face
    overall_fake_prob = max(highest_risk_tp.fake_probability, average_risk)
    overall_real_prob = 1.0 - overall_fake_prob
    overall_conf = sum(all_confs) / len(all_confs) if all_confs else 0.90

    return AggregatedDeepfakeResult(
        overall_fake_probability=overall_fake_prob,
        overall_real_probability=overall_real_prob,
        overall_confidence=overall_conf,
        highest_risk_face_id=highest_risk_face_id,
        average_risk_across_faces=average_risk,
        faces_analyzed_count=len(track_predictions),
        temporal_strategy_used=temporal_strategy,
        face_track_predictions=track_predictions,
    )
