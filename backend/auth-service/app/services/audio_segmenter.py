"""Audio Segmentation Service for AI Voice Clone Infrastructure.

Segmentation Strategies:
- FIXED_WINDOW (equidistant fixed duration windows, e.g. 3.0s)
- ADAPTIVE_WINDOW (audio duration-dependent windowing)
- SPEECH_BOUNDARY (segmentation on VAD speech onset/offset)
- SILENCE_BOUNDARY (segmentation on natural pauses > 0.3s)
"""

from typing import List, Dict, Any
from app.services.voice_activity_detector import SpeechSegmentData


def segment_audio_intelligently(
    vad_segments: List[SpeechSegmentData],
    duration_sec: float = 10.0,
    strategy: str = "SPEECH_BOUNDARY",
    target_window_sec: float = 3.0,
) -> List[Dict[str, Any]]:
    """Splits audio into windowed chunks using selected segmentation strategy."""
    chunks: List[Dict[str, Any]] = []

    if strategy.upper() == "FIXED_WINDOW":
        curr = 0.0
        idx = 0
        while curr < duration_sec:
            end = min(duration_sec, curr + target_window_sec)
            chunks.append({
                "chunk_index": idx,
                "start_time_sec": round(curr, 2),
                "end_time_sec": round(end, 2),
                "duration_sec": round(end - curr, 2),
                "strategy": "FIXED_WINDOW",
            })
            idx += 1
            curr = end

    elif strategy.upper() == "SILENCE_BOUNDARY" or strategy.upper() == "SPEECH_BOUNDARY":
        # Group VAD speech segments
        speech_only = [s for s in vad_segments if s.is_speech]
        for idx, seg in enumerate(speech_only):
            chunks.append({
                "chunk_index": idx,
                "start_time_sec": seg.start_time_sec,
                "end_time_sec": seg.end_time_sec,
                "duration_sec": seg.duration_sec,
                "speaker_id": seg.speaker_id,
                "strategy": strategy.upper(),
            })

    else:  # ADAPTIVE_WINDOW
        window_size = 4.0 if duration_sec > 30.0 else 2.5
        curr = 0.0
        idx = 0
        while curr < duration_sec:
            end = min(duration_sec, curr + window_size)
            chunks.append({
                "chunk_index": idx,
                "start_time_sec": round(curr, 2),
                "end_time_sec": round(end, 2),
                "duration_sec": round(end - curr, 2),
                "strategy": "ADAPTIVE_WINDOW",
            })
            idx += 1
            curr = end

    return chunks
