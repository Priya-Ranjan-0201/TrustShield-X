"""Database Repository for Voice Clone & Audio Infrastructure.

Persists audio_metadata, speech_segments, and speaker_tracks records.
"""

import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audio_metadata import AudioMetadata, SpeechSegment, SpeakerTrack


class AudioRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_audio_record(
        self,
        scan_id: uuid.UUID,
        metadata_dict: Dict[str, Any],
        quality_metrics: Dict[str, Any],
        speech_segments_list: List[Dict[str, Any]],
        speaker_tracks_list: List[Dict[str, Any]],
    ) -> AudioMetadata:
        """Saves audio_metadata, speech_segments, and speaker_tracks records."""

        # 1. AudioMetadata
        meta = AudioMetadata(
            scan_id=scan_id,
            duration_sec=metadata_dict.get("duration_sec"),
            sample_rate=metadata_dict.get("sample_rate"),
            channels=metadata_dict.get("channels"),
            bit_depth=metadata_dict.get("bit_depth"),
            codec=metadata_dict.get("codec"),
            bitrate=metadata_dict.get("bitrate"),
            loudness_lufs=metadata_dict.get("loudness_lufs"),
            quality_metrics=quality_metrics,
        )
        self.session.add(meta)

        # 2. SpeechSegments
        for seg in speech_segments_list:
            ss = SpeechSegment(
                scan_id=scan_id,
                segment_index=seg.get("segment_index", 0),
                start_time_sec=seg.get("start_time_sec", 0.0),
                end_time_sec=seg.get("end_time_sec", 0.0),
                duration_sec=seg.get("duration_sec", 0.0),
                speaker_id=seg.get("speaker_id", "speaker_1"),
                is_speech=seg.get("is_speech", True),
                confidence=seg.get("confidence", 0.95),
            )
            self.session.add(ss)

        # 3. SpeakerTracks
        for track in speaker_tracks_list:
            st = SpeakerTrack(
                scan_id=scan_id,
                speaker_id=track.get("speaker_id", "speaker_1"),
                total_speaking_duration=track.get("total_speaking_duration", 0.0),
                segment_count=track.get("segment_count", 0),
                timeline_json=track.get("timeline_entries", []),
            )
            self.session.add(st)

        await self.session.commit()
        return meta

    async def get_by_scan_id(self, scan_id: uuid.UUID) -> Optional[AudioMetadata]:
        stmt = select(AudioMetadata).where(AudioMetadata.scan_id == scan_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
