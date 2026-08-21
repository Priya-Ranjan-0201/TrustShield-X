"""Speaker Tracking Service across Timeline for AI Voice Clone Infrastructure.

Tracks unique speakers across the audio recording:
- Assigns persistent speaker_ids (speaker_1, speaker_2)
- Calculates total speaking duration per speaker
- Records timeline segment entries per speaker
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from app.services.speaker_diarizer import DiarizationSegment


@dataclass
class SpeakerTrackRecord:
    speaker_id: str
    total_speaking_duration: float
    segment_count: int
    timeline_entries: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "speaker_id": self.speaker_id,
            "total_speaking_duration": round(self.total_speaking_duration, 2),
            "segment_count": self.segment_count,
            "timeline_entries": self.timeline_entries,
        }


def track_speakers_across_timeline(
    diarized_segments: List[DiarizationSegment]
) -> List[SpeakerTrackRecord]:
    """Aggregates diarized segments into persistent SpeakerTrackRecord objects."""
    speaker_map: Dict[str, Dict[str, Any]] = {}

    for seg in diarized_segments:
        spk_id = seg.speaker_id
        if spk_id not in speaker_map:
            speaker_map[spk_id] = {
                "total_duration": 0.0,
                "segments": [],
            }

        speaker_map[spk_id]["total_duration"] += seg.duration_sec
        speaker_map[spk_id]["segments"].append(seg.to_dict())

    records: List[SpeakerTrackRecord] = []
    for spk_id, data in speaker_map.items():
        records.append(
            SpeakerTrackRecord(
                speaker_id=spk_id,
                total_speaking_duration=data["total_duration"],
                segment_count=len(data["segments"]),
                timeline_entries=data["segments"],
            )
        )

    return records
