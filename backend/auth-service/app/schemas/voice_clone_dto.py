"""Pydantic DTO Schemas for Voice Clone Detection Engine (Phase 3.6 Part 2B-1).

API-ready Response DTOs:
- VoiceCloneResultResponse
- ConversationAnalysisResponse
- EvidenceResponse
- RecommendationResponse
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict


class EvidenceResponse(BaseModel):
    id: Optional[str] = None
    module: str = "voice-clone"
    type: str
    category: str
    severity: str
    title: str
    description: str
    recommendation: Optional[str] = None
    confidence: float
    speaker_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class RecommendationResponse(BaseModel):
    recommendations: List[str] = []

    model_config = ConfigDict(from_attributes=True)


class VoiceCloneResultResponse(BaseModel):
    speaker_id: str
    segment_id: Optional[str] = None
    clone_probability: float
    similarity_score: Optional[float] = None
    confidence: Optional[float] = None
    verdict: str
    evidence: List[Dict[str, Any]] = []
    recommendations: List[str] = []

    model_config = ConfigDict(from_attributes=True)


class ConversationAnalysisResponse(BaseModel):
    total_speakers: int
    conversation_duration: float
    conversation_quality: Optional[int] = None
    conversation_risk: int
    conversation_confidence: Optional[float] = None
    dominant_speaker: Optional[str] = None
    summary: Dict[str, Any] = {}

    model_config = ConfigDict(from_attributes=True)
