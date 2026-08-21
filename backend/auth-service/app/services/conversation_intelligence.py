"""Conversation Intelligence Engine for AI Voice Clone Engine (Phase 3.6 Part 2A-2A-2).

Analyzes conversation dynamics across full audio recording:
- Conversation Duration
- Total Speaker Count
- Speaker Participation Ratios
- Speaker Switching Frequency
- Silence Gaps & Long Pauses
- Speaking Balance
- Conversation Quality Index (0-100)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ConversationIntelligenceOutput:
    conversation_duration_sec: float
    total_speakers: int
    speaker_participation: Dict[str, float]
    speaker_switching_count: int
    silence_gap_count: int
    speaking_balance_ratio: float
    conversation_quality_score: int
    conversation_summary: str
    speaker_statistics: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "conversation_duration_sec": round(self.conversation_duration_sec, 2),
            "total_speakers": self.total_speakers,
            "speaker_participation": self.speaker_participation,
            "speaker_switching_count": self.speaker_switching_count,
            "silence_gap_count": self.silence_gap_count,
            "speaking_balance_ratio": round(self.speaking_balance_ratio, 2),
            "conversation_quality_score": self.conversation_quality_score,
            "conversation_summary": self.conversation_summary,
            "speaker_statistics": self.speaker_statistics,
        }


class ConversationIntelligenceEngine:
    """Conversation Dynamics & Intelligence Analysis Engine."""

    def analyze_conversation(
        self,
        duration_sec: float,
        vad_segments: List[Dict[str, Any]],
        speaker_tracks: List[Dict[str, Any]],
        quality_metrics: Dict[str, Any],
    ) -> ConversationIntelligenceOutput:
        
        total_speakers = len(speaker_tracks) or 1
        total_speech_dur = sum(s.get("duration_sec", 0.0) for s in vad_segments if s.get("is_speech", True)) or 1.0

        participation: Dict[str, float] = {}
        speaker_stats: List[Dict[str, Any]] = []

        max_dur = 0.0
        for spk in speaker_tracks:
            spk_id = spk.get("speaker_id", "speaker_1")
            dur = spk.get("total_speaking_duration", 0.0)
            ratio = round((dur / total_speech_dur) * 100, 1)
            participation[spk_id] = ratio

            if dur > max_dur:
                max_dur = dur

            speaker_stats.append({
                "speaker_id": spk_id,
                "speaking_duration_sec": round(dur, 2),
                "participation_percent": ratio,
                "segment_count": spk.get("segment_count", 1),
            })

        # Calculate Speaker Switching Count & Silence Gaps
        switching_count = 0
        silence_count = 0
        prev_speaker = None

        for seg in vad_segments:
            if not seg.get("is_speech", True):
                silence_count += 1
                continue

            curr_spk = seg.get("speaker_id", "speaker_1")
            if prev_speaker and curr_spk != prev_speaker:
                switching_count += 1
            prev_speaker = curr_spk

        # Speaking balance ratio: max_duration / avg_duration
        avg_dur = total_speech_dur / total_speakers
        balance_ratio = max_dur / avg_dur if avg_dur > 0 else 1.0

        # Conversation Quality Index (0-100)
        base_quality = quality_metrics.get("overall_quality_score", 85)
        if balance_ratio > 3.0:
            base_quality -= 10
        if silence_count > 5:
            base_quality -= 5

        quality_score = max(0, min(100, base_quality))

        summary = f"Processed {duration_sec:.1f}s audio conversation with {total_speakers} speaker(s) and {switching_count} speaker transition(s)."

        return ConversationIntelligenceOutput(
            conversation_duration_sec=duration_sec,
            total_speakers=total_speakers,
            speaker_participation=participation,
            speaker_switching_count=switching_count,
            silence_gap_count=silence_count,
            speaking_balance_ratio=balance_ratio,
            conversation_quality_score=quality_score,
            conversation_summary=summary,
            speaker_statistics=speaker_stats,
        )
