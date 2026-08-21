"""Master Audio Processing Pipeline Orchestrator for Phase 3.6 Part 1.

Orchestrates complete audio preprocessing, VAD, and speaker diarization pipeline:
1. Audio Validation (MIME, extension, sample rate, corruption TSX-AUDIO-001)
2. Technical Metadata Extraction (Sample Rate, Bit Depth, Duration, Channels, LUFS)
3. Audio Quality Analysis (SNR dB, Clipping %, Silence %, Dynamic Range)
4. Voice Activity Detection (VAD timestamps: Speech vs Silence vs Noise)
5. Intelligent Audio Segmentation (Speech boundary windowing)
6. Speaker Diarization (pyannote.audio abstraction provider)
7. Speaker Tracking across timeline (speaker_1, speaker_2 timeline entries)
8. Speaker Embedding Extraction Interface & Model Registry (ECAPA-TDNN 192-dim)

Returns structured result ready for Part 2 Voice Clone neural inference.
"""

import time
from typing import Dict, Any, List, Optional

from app.services.audio_validator import validate_audio_file
from app.services.audio_metadata_extractor import extract_audio_metadata
from app.services.audio_quality_analyzer import analyze_audio_quality
from app.services.voice_activity_detector import detect_voice_activity
from app.services.audio_segmenter import segment_audio_intelligently
from app.services.speaker_diarizer import PyannoteSpeakerDiarizer
from app.services.speaker_tracker import track_speakers_across_timeline
from app.services.audio_model_registry import AudioModelRegistry


class AudioPipelineResult:
    def __init__(
        self,
        module: str,
        status: str,
        metadata: Dict[str, Any],
        quality_metrics: Dict[str, Any],
        speech_segments: List[Dict[str, Any]],
        audio_chunks: List[Dict[str, Any]],
        speaker_tracks: List[Dict[str, Any]],
        speaker_embeddings_summary: List[Dict[str, Any]],
        total_speech_duration_sec: float,
        total_speakers_detected: int,
        risk_score: int,
        confidence_score: float,
        severity: str,
        evidence: List[Dict[str, str]],
        recommendations: List[str],
        pipeline_status: str,
        execution_time_ms: int,
    ):
        self.module = module
        self.status = status
        self.metadata = metadata
        self.quality_metrics = quality_metrics
        self.speech_segments = speech_segments
        self.audio_chunks = audio_chunks
        self.speaker_tracks = speaker_tracks
        self.speaker_embeddings_summary = speaker_embeddings_summary
        self.total_speech_duration_sec = total_speech_duration_sec
        self.total_speakers_detected = total_speakers_detected
        self.risk_score = risk_score
        self.confidence_score = confidence_score
        self.severity = severity
        self.evidence = evidence
        self.recommendations = recommendations
        self.pipeline_status = pipeline_status
        self.execution_time_ms = execution_time_ms

    def to_dict(self) -> Dict[str, Any]:
        return {
            "module": self.module,
            "status": self.status,
            "metadata": self.metadata,
            "quality_metrics": self.quality_metrics,
            "speech_segments": self.speech_segments,
            "audio_chunks": self.audio_chunks,
            "speaker_tracks": self.speaker_tracks,
            "speaker_embeddings_summary": self.speaker_embeddings_summary,
            "total_speech_duration_sec": round(self.total_speech_duration_sec, 2),
            "total_speakers_detected": self.total_speakers_detected,
            "risk_score": self.risk_score,
            "confidence_score": round(self.confidence_score, 4),
            "severity": self.severity,
            "evidence": self.evidence,
            "recommendations": self.recommendations,
            "pipeline_status": self.pipeline_status,
            "execution_time_ms": self.execution_time_ms,
        }


class AudioProcessingOrchestrator:
    def __init__(self):
        self.diarizer = PyannoteSpeakerDiarizer()
        self.model_registry = AudioModelRegistry()

    async def analyze_audio(
        self, file_bytes: bytes, filename: str, content_type: Optional[str] = None
    ) -> AudioPipelineResult:
        start_time = time.time()

        evidence: List[Dict[str, str]] = []
        recommendations: List[str] = []

        # 1. Audio Validation
        val_res = validate_audio_file(file_bytes, filename, content_type)
        if not val_res.is_valid:
            execution_time_ms = int((time.time() - start_time) * 1000)
            return AudioPipelineResult(
                module="audio-voice-ai",
                status="failed",
                metadata={},
                quality_metrics={},
                speech_segments=[],
                audio_chunks=[],
                speaker_tracks=[],
                speaker_embeddings_summary=[],
                total_speech_duration_sec=0.0,
                total_speakers_detected=0,
                risk_score=100,
                confidence_score=0.0,
                severity="DANGEROUS",
                evidence=[{
                    "type": "AUDIO_VALIDATION",
                    "severity": "CRITICAL",
                    "title": f"Audio Validation Failed ({val_res.error_code})",
                    "description": val_res.error_message or "Unsupported or corrupted audio file.",
                }],
                recommendations=["Upload a valid WAV, MP3, M4A, AAC, FLAC, OGG, or OPUS file under 25MB."],
                pipeline_status="FAILED",
                execution_time_ms=execution_time_ms,
            )

        # 2. Technical Metadata Extraction
        meta_res = extract_audio_metadata(file_bytes, val_res.extension)
        meta_dict = meta_res.to_dict()

        # 3. Audio Quality Analysis (SNR, Clipping, Silence)
        quality_dict = analyze_audio_quality(
            file_bytes, meta_res.duration_sec, meta_res.sample_rate
        )

        # 4. Voice Activity Detection (VAD)
        vad_segments = detect_voice_activity(
            file_bytes, meta_res.duration_sec, meta_res.sample_rate
        )
        vad_summary = [s.to_dict() for s in vad_segments]

        # Calculate speech duration
        speech_duration = sum(s.duration_sec for s in vad_segments if s.is_speech)

        # 5. Intelligent Audio Segmentation
        chunks_summary = segment_audio_intelligently(
            vad_segments, meta_res.duration_sec, strategy="SPEECH_BOUNDARY"
        )

        # 6. Speaker Diarization & Speaker Tracking
        diarized_segs = self.diarizer.diarize_audio(file_bytes, vad_segments)
        speaker_records = track_speakers_across_timeline(diarized_segs)
        tracks_summary = [st.to_dict() for st in speaker_records]

        # 7. Speaker Embedding Extraction Interface
        extractor = self.model_registry.get_active_extractor()
        prep_data = extractor.preprocess(file_bytes)

        embeddings_summary = []
        for spk in speaker_records:
            emb_out = extractor.extract_embedding(prep_data, speaker_id=spk.speaker_id)
            embeddings_summary.append(emb_out.to_dict())

        # 8. Speaker Similarity Engine
        from app.services.speaker_similarity_engine import analyze_speaker_embedding_similarity
        similarity_metrics = analyze_speaker_embedding_similarity(embeddings_summary)

        # 9. Neural Voice Clone Classifier Inference
        from app.services.voice_clone_analyzer import analyze_voice_clone_multi_speaker
        voice_adapter = self.model_registry.get_active_voice_adapter()
        clone_results = analyze_voice_clone_multi_speaker(
            file_bytes, meta_dict, tracks_summary, voice_adapter
        )

        overall_clone_prob = clone_results.get("overall_clone_probability", 0.05)
        overall_real_prob = clone_results.get("overall_real_probability", 0.95)
        risk_score = int(overall_clone_prob * 100)

        # 10. Advanced Confidence Calibration Engine
        from app.services.audio_confidence_calibrator import AudioConfidenceCalibrator
        calibrator = AudioConfidenceCalibrator()
        cal_out = calibrator.calibrate_confidence(
            raw_clone_probability=overall_clone_prob,
            quality_metrics=quality_dict,
            metadata=meta_dict,
            speech_duration_sec=speech_duration,
            segment_count=len(vad_segments),
            speaker_count=len(speaker_records),
        )

        # 11. Speaker & Conversation Aggregation Engine
        from app.services.audio_speaker_aggregator import AudioSpeakerAggregator
        aggregator = AudioSpeakerAggregator()
        spk_agg_out = aggregator.aggregate_speakers(
            per_speaker_results=clone_results.get("per_speaker_results", []),
            overall_confidence=cal_out.calibrated_confidence,
        )

        # 12. Voice Clone Risk Aggregation Engine
        from app.services.audio_risk_engine import AudioRiskEngine
        risk_engine = AudioRiskEngine()
        risk_out = risk_engine.compute_risk_score(
            clone_probability=overall_clone_prob,
            calibrated_confidence=cal_out.calibrated_confidence,
            highest_speaker_risk=spk_agg_out.highest_risk_score,
            average_speaker_risk=spk_agg_out.average_risk_score,
            similarity_anomaly=similarity_metrics.get("similarity_anomaly_detected", False),
        )

        # 13. Conversation Decision Engine
        from app.services.audio_decision_engine import AudioDecisionEngine
        decision_engine = AudioDecisionEngine()
        decision_out = decision_engine.make_decision(
            risk_score=risk_out.risk_score,
            calibrated_confidence=cal_out.calibrated_confidence,
            confidence_level=cal_out.confidence_level,
            clone_probability=overall_clone_prob,
            quality_metrics=quality_dict,
            speech_duration_sec=speech_duration,
        )

        # 14. Conversation Intelligence Engine
        from app.services.conversation_intelligence import ConversationIntelligenceEngine
        conv_intel_engine = ConversationIntelligenceEngine()
        conv_intel_out = conv_intel_engine.analyze_conversation(
            duration_sec=meta_res.duration_sec,
            vad_segments=vad_summary,
            speaker_tracks=tracks_summary,
            quality_metrics=quality_dict,
        )

        # 15. Factual Voice Behavior Analyzer
        from app.services.voice_behavior_analyzer import VoiceBehaviorAnalyzer
        behavior_analyzer = VoiceBehaviorAnalyzer()
        behavior_out = behavior_analyzer.analyze_behavior(
            vad_segments=vad_summary,
            quality_metrics=quality_dict,
            duration_sec=meta_res.duration_sec,
        )

        # 16. Rule-based Audio Scam Detector
        from app.services.audio_scam_detector import AudioScamDetector
        scam_detector = AudioScamDetector()
        scam_matches = scam_detector.detect_scam_indicators(transcript_text="")

        # 17. Structured Audio Explainability Engine
        from app.services.audio_explainability import AudioExplainabilityEngine
        exp_engine = AudioExplainabilityEngine()
        explanations_list = exp_engine.generate_explanations(
            verdict=decision_out.verdict,
            clone_probability=overall_clone_prob,
            calibrated_confidence=cal_out.calibrated_confidence,
            quality_metrics=quality_dict,
            speaker_tracks=tracks_summary,
            similarity_metrics=similarity_metrics,
            duration_sec=meta_res.duration_sec,
        )

        # 18. Standardized Platform Evidence Generator
        from app.services.audio_evidence_generator import AudioEvidenceGenerator
        evidence_gen = AudioEvidenceGenerator()
        evidence_cards = evidence_gen.generate_evidence_cards(
            verdict=decision_out.verdict,
            risk_score=risk_out.risk_score,
            calibrated_confidence=cal_out.calibrated_confidence,
            confidence_level=cal_out.confidence_level,
            explanations=explanations_list,
            scam_matches=scam_matches,
            quality_metrics=quality_dict,
        )

        # 19. Deterministic Recommendation Engine
        from app.services.audio_recommendation_engine import AudioRecommendationEngine
        rec_engine = AudioRecommendationEngine()
        deterministic_recs = rec_engine.generate_recommendations(evidence_cards)

        execution_time_ms = int((time.time() - start_time) * 1000)

        return AudioPipelineResult(
            module="audio-voice-ai",
            status="completed",
            metadata=meta_dict,
            quality_metrics=quality_dict,
            speech_segments=vad_summary,
            audio_chunks=chunks_summary,
            speaker_tracks=tracks_summary,
            speaker_embeddings_summary=embeddings_summary,
            total_speech_duration_sec=speech_duration,
            total_speakers_detected=len(speaker_records),
            risk_score=risk_out.risk_score,
            confidence_score=cal_out.calibrated_confidence,
            severity=risk_out.severity,
            evidence=evidence_cards,
            recommendations=deterministic_recs,
            pipeline_status="AI_CONVERSATION_INTELLIGENCE_COMPLETED",
            execution_time_ms=execution_time_ms,
        )
