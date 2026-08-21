"""
TruthShield X — Cyber Security Knowledge Fabric Master Coordinator (Phase 19).

Unifies all 20 knowledge engines into a single synchronized knowledge system.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.cyber_knowledge_fabric_models import (
    CyberKnowledgeFabricSummaryDTO,
)
from app.services.knowledge_fabric.knowledge_object_manager import KnowledgeObjectManager
from app.services.knowledge_fabric.knowledge_relationship_manager import KnowledgeRelationshipManager
from app.services.knowledge_fabric.temporal_knowledge_engine import TemporalKnowledgeEngine
from app.services.knowledge_fabric.knowledge_lineage_engine import KnowledgeLineageEngine
from app.services.knowledge_fabric.knowledge_diff_engine import KnowledgeDiffEngine
from app.services.knowledge_fabric.evidence_graph_engine import EvidenceGraphEngine
from app.services.knowledge_fabric.evidence_strength_engine import EvidenceStrengthEngine
from app.services.knowledge_fabric.evidence_contradiction_engine import EvidenceContradictionEngine
from app.services.knowledge_fabric.security_assertion_engine import SecurityAssertionEngine
from app.services.knowledge_fabric.security_hypothesis_engine import SecurityHypothesisEngine
from app.services.knowledge_fabric.security_reasoning_engine import SecurityReasoningEngine
from app.services.knowledge_fabric.investigation_question_engine import InvestigationQuestionEngine
from app.services.knowledge_fabric.knowledge_gap_engine import KnowledgeGapEngine
from app.services.knowledge_fabric.historical_analog_engine import HistoricalAnalogEngine
from app.services.knowledge_fabric.security_memory_engine import SecurityMemoryEngine
from app.services.knowledge_fabric.knowledge_revocation_engine import KnowledgeRevocationEngine
from app.services.knowledge_fabric.decision_traceability_engine import DecisionTraceabilityEngine
from app.services.knowledge_fabric.knowledge_quality_engine import KnowledgeQualityEngine
from app.services.knowledge_fabric.security_knowledge_assistant import SecurityKnowledgeAssistant


class CyberSecurityKnowledgeFabric:
    """Master Coordinator for TruthShield X Cyber Security Knowledge Fabric (Phase 19)."""

    def __init__(self):
        self.objects = KnowledgeObjectManager()
        self.relationships = KnowledgeRelationshipManager()
        self.temporal = TemporalKnowledgeEngine()
        self.lineage = KnowledgeLineageEngine()
        self.diff = KnowledgeDiffEngine()
        self.evidence_graph = EvidenceGraphEngine()
        self.evidence_strength = EvidenceStrengthEngine()
        self.contradictions = EvidenceContradictionEngine()
        self.assertions = SecurityAssertionEngine()
        self.hypotheses = SecurityHypothesisEngine()
        self.reasoning = SecurityReasoningEngine()
        self.questions = InvestigationQuestionEngine()
        self.gaps = KnowledgeGapEngine()
        self.analogs = HistoricalAnalogEngine()
        self.memory = SecurityMemoryEngine()
        self.revocations = KnowledgeRevocationEngine()
        self.decisions = DecisionTraceabilityEngine()
        self.quality = KnowledgeQualityEngine()
        self.assistant = SecurityKnowledgeAssistant()

    def get_summary(self, tenant_id: str = "default_tenant") -> CyberKnowledgeFabricSummaryDTO:
        """Returns high-level summary metrics of the Knowledge Fabric for executive dashboard."""
        objs = self.objects.list_objects(tenant_id)
        rels = self.relationships.list_all()
        ev_graph = self.evidence_graph.build_graph()
        asrs = self.assertions.list_assertions()
        contras = self.contradictions.list_all_contradictions()
        gaps = self.gaps.list_gaps()
        scorecard = self.quality.compute_scorecard()

        return CyberKnowledgeFabricSummaryDTO(
            fabric_id=f"fabric_{tenant_id}",
            tenant_id=tenant_id,
            total_knowledge_objects=len(objs),
            total_relationships=len(rels),
            evidence_nodes_count=ev_graph.total_evidence_nodes,
            active_assertions_count=len(asrs),
            unresolved_contradictions_count=len(contras),
            identified_knowledge_gaps_count=len(gaps),
            overall_quality_score=scorecard.overall_health_score,
            last_synthesized=datetime.now(timezone.utc).isoformat(),
        )
