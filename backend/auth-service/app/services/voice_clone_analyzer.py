"""Multi-Speaker & Segment Voice Clone Analyzer for Phase 3.6 Part 2A-1.

Analyzes voice clone probability per speaker, per segment, and across conversation:
- Clone Probability
- Real Voice Probability
- Unknown Probability
- Highest Risk Speaker
- Conversation Risk Summary
"""

from typing import Dict, Any, List
from app.services.voice_model_adapter import BaseVoiceCloneModelAdapter, VoiceCloneInferenceOutput


def analyze_voice_clone_multi_speaker(
    audio_bytes: bytes,
    metadata: Dict[str, Any],
    speaker_tracks: List[Dict[str, Any]],
    model_adapter: BaseVoiceCloneModelAdapter,
) -> Dict[str, Any]:
    """Runs neural voice clone inference across all tracked speakers and conversation timeline."""

    prep_data = model_adapter.preprocess(audio_bytes, metadata)

    per_speaker_results: List[Dict[str, Any]] = []
    highest_risk_speaker = "speaker_1"
    highest_risk_score = 0.0

    if not speaker_tracks:
        # Fallback single speaker analysis
        inf_out = model_adapter.infer(prep_data)
        post_res = model_adapter.postprocess(inf_out)
        clone_prob = post_res.get("clone_probability", 0.05)
        real_prob = post_res.get("real_probability", 0.95)

        return {
            "overall_clone_probability": clone_prob,
            "overall_real_probability": real_prob,
            "overall_unknown_probability": round(max(0.0, 1.0 - (clone_prob + real_prob)), 4),
            "highest_risk_speaker": "speaker_1",
            "highest_speaker_clone_prob": clone_prob,
            "average_speaker_risk": clone_prob,
            "per_speaker_results": [{
                "speaker_id": "speaker_1",
                "clone_probability": clone_prob,
                "real_probability": real_prob,
                "speaking_duration": metadata.get("duration_sec", 10.0),
                "is_clone": clone_prob >= 0.50,
            }],
            "raw_inference_output": {
                "model_name": inf_out.model_name,
                "version": inf_out.model_version,
                "execution_time_ms": inf_out.execution_time_ms,
                "device_used": inf_out.device_used,
            },
        }

    total_clone_accum = 0.0
    for idx, spk in enumerate(speaker_tracks):
        spk_id = spk.get("speaker_id", f"speaker_{idx+1}")
        duration = spk.get("total_speaking_duration", 5.0)

        # Per-speaker inference
        spk_prep = dict(prep_data)
        spk_prep["speaker_id"] = spk_id
        spk_prep["duration_sec"] = duration

        inf_out = model_adapter.infer(spk_prep)
        post_res = model_adapter.postprocess(inf_out)

        clone_prob = post_res.get("clone_probability", 0.05)
        real_prob = post_res.get("real_probability", 0.95)

        total_clone_accum += clone_prob
        if clone_prob > highest_risk_score:
            highest_risk_score = clone_prob
            highest_risk_speaker = spk_id

        per_speaker_results.append({
            "speaker_id": spk_id,
            "clone_probability": clone_prob,
            "real_probability": real_prob,
            "speaking_duration": duration,
            "segment_count": spk.get("segment_count", 1),
            "is_clone": clone_prob >= 0.50,
        })

    avg_clone_prob = round(total_clone_accum / len(speaker_tracks), 4)
    overall_clone_prob = highest_risk_score  # Max speaker risk strategy
    overall_real_prob = round(1.0 - overall_clone_prob, 4)
    overall_unknown_prob = round(max(0.0, 1.0 - (overall_clone_prob + overall_real_prob)), 4)

    return {
        "overall_clone_probability": overall_clone_prob,
        "overall_real_probability": overall_real_prob,
        "overall_unknown_probability": overall_unknown_prob,
        "highest_risk_speaker": highest_risk_speaker,
        "highest_speaker_clone_prob": highest_risk_score,
        "average_speaker_risk": avg_clone_prob,
        "per_speaker_results": per_speaker_results,
        "raw_inference_output": {
            "model_name": model_adapter.model_name,
            "version": model_adapter.version,
            "framework": model_adapter.framework,
            "device_used": getattr(model_adapter, "_device", "cpu"),
        },
    }
