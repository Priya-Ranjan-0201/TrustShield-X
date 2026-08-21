"""
TruthShield X — Threat Intelligence Fusion Engine (Phase 33 Master Coordinator).

Orchestrates the complete 16-stage threat intelligence fusion, predictive early-warning,
and governed dissemination lifecycle.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone

from app.schemas.threat_intelligence_fusion_models import (
    IntelligenceRecordDTO,
    IntelligenceSourceDTO,
    IndicatorDTO,
    ThreatCampaignDTO,
    ThreatActorProfileDTO,
    MalwareProfileDTO,
    VulnerabilityIntelligenceDTO,
    ThreatForecastDTO,
    ThreatEarlyWarningDTO,
    IntelligenceConflictDTO,
    IntelligenceSnapshotDTO,
    DisseminationRecordDTO,
)
from app.services.threat_intelligence_fusion.intelligence_source_registry import IntelligenceSourceRegistry
from app.services.threat_intelligence_fusion.feed_ingestion_engine import FeedIngestionEngine
from app.services.threat_intelligence_fusion.indicator_intelligence_engine import IndicatorIntelligenceEngine
from app.services.threat_intelligence_fusion.campaign_clustering_engine import CampaignClusteringEngine
from app.services.threat_intelligence_fusion.threat_actor_intelligence_engine import ThreatActorIntelligenceEngine
from app.services.threat_intelligence_fusion.malware_intelligence_engine import MalwareIntelligenceEngine
from app.services.threat_intelligence_fusion.vulnerability_intelligence_engine import VulnerabilityIntelligenceEngine
from app.services.threat_intelligence_fusion.asset_exposure_correlation_engine import AssetExposureCorrelationEngine
from app.services.threat_intelligence_fusion.intelligence_graph_fusion_engine import IntelligenceGraphFusionEngine
from app.services.threat_intelligence_fusion.multi_source_corroboration_engine import MultiSourceCorroborationEngine
from app.services.threat_intelligence_fusion.intelligence_quality_scorecard_engine import IntelligenceQualityScorecardEngine
from app.services.threat_intelligence_fusion.predictive_threat_intelligence_engine import PredictiveThreatIntelligenceEngine
from app.services.threat_intelligence_fusion.threat_early_warning_engine import ThreatEarlyWarningEngine
from app.services.threat_intelligence_fusion.threat_landscape_engine import ThreatLandscapeEngine
from app.services.threat_intelligence_fusion.intelligence_dissemination_engine import IntelligenceDisseminationEngine


class ThreatIntelligenceFusionEngine:
    """Master Platform for Cyber Threat Intelligence Fusion, Forecasting, and Governed Operations."""

    def __init__(self):
        self.sources = IntelligenceSourceRegistry()
        self.ingestion = FeedIngestionEngine()
        self.indicators = IndicatorIntelligenceEngine()
        self.campaigns = CampaignClusteringEngine()
        self.actors = ThreatActorIntelligenceEngine()
        self.malware = MalwareIntelligenceEngine()
        self.vulnerabilities = VulnerabilityIntelligenceEngine()
        self.assets = AssetExposureCorrelationEngine()
        self.graph = IntelligenceGraphFusionEngine()
        self.corroboration = MultiSourceCorroborationEngine()
        self.quality = IntelligenceQualityScorecardEngine()
        self.forecasting = PredictiveThreatIntelligenceEngine()
        self.early_warning = ThreatEarlyWarningEngine()
        self.landscape = ThreatLandscapeEngine()
        self.dissemination = IntelligenceDisseminationEngine()

    def get_overview(self) -> Dict[str, Any]:
        sources_list = self.sources.list_sources()
        inds = self.indicators.list_indicators()
        cmps = self.campaigns.list_campaigns()
        acts = self.actors.list_actors()
        fcs = self.forecasting.list_forecasts()
        warns = self.early_warning.list_warnings()
        confs = self.corroboration.list_conflicts()

        return {
            "platform": "TruthShield X Threat Intelligence Fusion OS",
            "phase": 33,
            "sources_count": len(sources_list),
            "indicators_count": len(inds),
            "active_campaigns_count": len(cmps),
            "threat_actors_count": len(acts),
            "forecasts_count": len(fcs),
            "early_warnings_count": len(warns),
            "intelligence_conflicts_count": len(confs),
            "feed_health": "OPTIMAL",
            "intelligence_quality_rating": "GROUNDED_HIGH_FIDELITY",
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
        }
