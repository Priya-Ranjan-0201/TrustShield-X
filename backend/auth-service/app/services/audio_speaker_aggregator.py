"""Speaker & Conversation Aggregation Engine (Phase 3.6 Part 2A-2A-1).

Aggregates per-speaker predictions, duration, and embedding quality into conversation-level risk summaries:
- highest_risk_speaker
- average_risk
- conversation_risk
- conversation_confidence
- speaker_count

Supports Single Speaker, Two Speaker, and Multi-Speaker recordings.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class SpeakerAggregateOutput:
    highest_risk_speaker: str
    highest_risk_score: float
    average_risk_score: float
    conversation_risk_score: int
    conversation_confidence: float
    speaker_count: int
    per_speaker_breakdown: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "highest_risk_speaker": self.highest_risk_speaker,
            "highest_risk_score": round(self.highest_risk_score, 4),
            "average_risk_score": round(self.average_risk_score, 4),
            "conversation_risk_score": self.conversation_risk_score,
            "conversation_confidence": round(self.conversation_confidence, 4),
            "speaker_count": self.speaker_count,
            "per_speaker_breakdown": self.per_speaker_breakdown,
        }


class BaseSpeakerAggregator(ABC):
    """Abstract Base Class for Speaker Aggregators."""

    @abstractmethod
    def aggregate_speakers(
        self,
        per_speaker_results: List[Dict[str, Any]],
        overall_confidence: float,
    ) -> SpeakerAggregateOutput:
        pass


class AudioSpeakerAggregator(BaseSpeakerAggregator):
    """Speaker and Conversation Aggregation Engine."""

    def aggregate_speakers(
        self,
        per_speaker_results: List[Dict[str, Any]],
        overall_confidence: float,
    ) -> SpeakerAggregateOutput:
        
        if not per_speaker_results:
            return SpeakerAggregateOutput(
                highest_risk_speaker="speaker_1",
                highest_risk_score=0.05,
                average_risk_score=0.05,
                conversation_risk_score=5,
                conversation_confidence=overall_confidence,
                speaker_count=1,
                per_speaker_breakdown=[{
                    "speaker_id": "speaker_1",
                    "clone_probability": 0.05,
                    "risk_score": 5,
                    "speaking_duration": 10.0,
                    "is_clone": False,
                }],
            )

        highest_spk = per_speaker_results[0].get("speaker_id", "speaker_1")
        highest_score = 0.0
        total_risk = 0.0
        breakdown = []

        for spk in per_speaker_results:
            spk_id = spk.get("speaker_id", "speaker_1")
            clone_prob = spk.get("clone_probability", 0.05)
            duration = spk.get("speaking_duration", 5.0)

            total_risk += clone_prob
            if clone_prob > highest_score:
                highest_score = clone_prob
                highest_spk = spk_id

            breakdown.append({
                "speaker_id": spk_id,
                "clone_probability": round(clone_prob, 4),
                "risk_score": int(clone_prob * 100),
                "speaking_duration": round(duration, 2),
                "segment_count": spk.get("segment_count", 1),
                "is_clone": clone_prob >= 0.50,
            })

        avg_risk = total_risk / len(per_speaker_results)
        conv_risk_score = int(highest_score * 100)

        return SpeakerAggregateOutput(
            highest_risk_speaker=highest_spk,
            highest_risk_score=highest_score,
            average_risk_score=avg_risk,
            conversation_risk_score=conv_risk_score,
            conversation_confidence=overall_confidence,
            speaker_count=len(per_speaker_results),
            per_speaker_breakdown=breakdown,
        )
