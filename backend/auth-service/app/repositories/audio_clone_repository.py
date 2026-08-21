"""Database Repository for Voice Clone Production Integration (Phase 3.6 Part 2B-1).

Persists audio_metadata, voice_clone_results, and conversation_analysis records.
Async bulk insertion with zero controller SQL logic.
"""

import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audio_metadata import AudioMetadata, SpeechSegment, SpeakerTrack
from app.models.voice_clone_result import VoiceCloneResult, ConversationAnalysis


class AudioCloneRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_voice_clone_analysis(
        self,
        scan_id: uuid.UUID,
        metadata_dict: Dict[str, Any],
        quality_metrics: Dict[str, Any],
        speech_segments_list: List[Dict[str, Any]],
        speaker_tracks_list: List[Dict[str, Any]],
        inference_results: Dict[str, Any],
        evidence_list: List[Dict[str, Any]],
        recommendations_list: List[str],
    ) -> AudioMetadata:
        """Persists full voice clone analysis: metadata, speech segments, speaker tracks, per-speaker clone results, and conversation analysis."""

        clone_prob = inference_results.get("clone_probability", 0.05)
        real_prob = inference_results.get("real_probability", 0.95)
        confidence = inference_results.get("confidence", 0.95)
        calibrated_conf = inference_results.get("calibrated_confidence", confidence)
        verdict = inference_results.get("verdict", "REAL")
        risk_score = inference_results.get("risk_score", int(clone_prob * 100))

        # 1. Extended AudioMetadata
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
            # Production Inference & Version Tracking Columns
            clone_probability=clone_prob,
            real_probability=real_prob,
            confidence=confidence,
            calibrated_confidence=calibrated_conf,
            prediction=verdict,
            prediction_reason=inference_results.get("prediction_reason", "Acoustic resonance verification"),
            model_name=inference_results.get("model_name", "ECAPA-TDNN-VoiceClone"),
            model_version=inference_results.get("model_version", "2.1-Production"),
            inference_time_ms=inference_results.get("execution_time_ms", 0),
            embedding_dimension=inference_results.get("embedding_dimension", 192),
            embedding_model=inference_results.get("embedding_model", "ECAPA-TDNN"),
            device_used=inference_results.get("device_used", "cpu"),
            explanation_available=True,
            evidence_available=len(evidence_list) > 0,
            recommendation_available=len(recommendations_list) > 0,
        )
        self.session.add(meta)

        # 2. SpeechSegments (VAD)
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

        # 4. VoiceCloneResults (Per-Speaker & Segment Results)
        per_speaker = inference_results.get("per_speaker_results", [])
        if not per_speaker:
            per_speaker = [{
                "speaker_id": "speaker_1",
                "clone_probability": clone_prob,
                "confidence": calibrated_conf,
                "is_clone": clone_prob >= 0.50,
            }]

        for spk in per_speaker:
            spk_id = spk.get("speaker_id", "speaker_1")
            spk_prob = spk.get("clone_probability", clone_prob)
            spk_verdict = "VOICE_CLONE" if spk_prob >= 0.50 else "REAL"

            spk_evidence = [e for e in evidence_list if e.get("speaker_id") == spk_id or e.get("speaker_id") == "all"]

            vc_res = VoiceCloneResult(
                scan_id=scan_id,
                speaker_id=spk_id,
                segment_id=spk.get("segment_id"),
                clone_probability=spk_prob,
                similarity_score=spk.get("similarity_score", 0.95),
                confidence=calibrated_conf,
                verdict=spk_verdict,
                evidence_json=spk_evidence or evidence_list,
                recommendation_json=recommendations_list,
            )
            self.session.add(vc_res)

        # 5. ConversationAnalysis
        conv_analysis = ConversationAnalysis(
            scan_id=scan_id,
            total_speakers=len(speaker_tracks_list) or 1,
            conversation_duration=metadata_dict.get("duration_sec", 0.0),
            conversation_quality=quality_metrics.get("overall_quality_score", 85),
            conversation_risk=risk_score,
            conversation_confidence=calibrated_conf,
            dominant_speaker=per_speaker[0].get("speaker_id", "speaker_1") if per_speaker else "speaker_1",
            summary_json={
                "verdict": verdict,
                "risk_score": risk_score,
                "total_segments": len(speech_segments_list),
                "model_used": inference_results.get("model_name", "ECAPA-TDNN-VoiceClone"),
            },
        )
        self.session.add(conv_analysis)

        await self.session.commit()
        return meta

    async def get_analysis_by_scan_id(self, scan_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """Retrieves full voice clone analysis record for scan history."""
        stmt_meta = select(AudioMetadata).where(AudioMetadata.scan_id == scan_id)
        res_meta = await self.session.execute(stmt_meta)
        meta = res_meta.scalar_one_or_none()

        if not meta:
            return None

        stmt_results = select(VoiceCloneResult).where(VoiceCloneResult.scan_id == scan_id)
        res_results = await self.session.execute(stmt_results)
        results = res_results.scalars().all()

        stmt_conv = select(ConversationAnalysis).where(ConversationAnalysis.scan_id == scan_id)
        res_conv = await self.session.execute(stmt_conv)
        conv = res_conv.scalar_one_or_none()

        return {
            "metadata": meta,
            "voice_clone_results": results,
            "conversation_analysis": conv,
        }
