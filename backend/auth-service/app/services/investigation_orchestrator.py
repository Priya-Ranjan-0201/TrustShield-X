"""Investigation Orchestrator Service (Phase 4.0 Part 4 — Section 73).

Coordinates the investigation workspace, evidence graph construction, timeline synthesis,
cross-modal correlation, role-based views, search, and report comparisons.
Strictly acts as a PRESENTATION & INVESTIGATION layer without recalculating risk.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid

from app.schemas.digital_trust_report_models import ReportDocumentDTO, ReportFindingDTO, ReportEvidenceCardDTO
from app.schemas.investigation_models import (
    InvestigationWorkspaceDTO,
    WorkspaceContextDTO,
    GraphNodeDTO,
    GraphEdgeDTO,
    InvestigationGraphResponseDTO,
    TimelineEventDTO,
    TimelineResponseDTO,
    InvestigationSearchResultDTO,
    InvestigationSearchResponseDTO,
    RoleAwareViewDTO,
    InvestigationCorrelationDTO,
    CrossModalCorrelationResponseDTO,
)


class InvestigationOrchestrator:
    """Master orchestrator for digital trust investigation workspace."""

    # -----------------------------------------------------------------------
    # Section 39-43: Role-Aware View Construction
    # -----------------------------------------------------------------------

    def get_role_view_config(self, role: str) -> RoleAwareViewDTO:
        role_upper = (role or "ANALYST").upper()
        if role_upper == "EXECUTIVE":
            return RoleAwareViewDTO(
                role="EXECUTIVE",
                visible_panels=["overview", "risk", "major_findings", "recommendations"],
                show_raw_technical_data=False,
                show_audit_metadata=False,
                show_provenance_links=False,
                permissions=["report:view", "report:export"],
            )
        elif role_upper == "TECHNICAL":
            return RoleAwareViewDTO(
                role="TECHNICAL",
                visible_panels=["overview", "findings", "evidence", "dataflow", "behavior", "technical_appendix", "graph"],
                show_raw_technical_data=True,
                show_audit_metadata=False,
                show_provenance_links=True,
                permissions=["report:view", "evidence:view", "technical:view", "dataflow:view"],
            )
        elif role_upper == "AUDITOR":
            return RoleAwareViewDTO(
                role="AUDITOR",
                visible_panels=["overview", "risk", "findings", "evidence", "provenance", "lineage", "signatures", "audit_log", "comparison"],
                show_raw_technical_data=False,
                show_audit_metadata=True,
                show_provenance_links=True,
                permissions=["report:view", "report:verify", "audit:view", "provenance:view"],
            )
        elif role_upper == "ADMIN":
            return RoleAwareViewDTO(
                role="ADMIN",
                visible_panels=["overview", "risk", "findings", "evidence", "graph", "timeline", "dataflow", "behavior", "threat_intel", "contradictions", "cases", "notes", "tasks", "shares", "audit_log"],
                show_raw_technical_data=True,
                show_audit_metadata=True,
                show_provenance_links=True,
                permissions=["*"],
            )
        else:  # ANALYST (Default)
            return RoleAwareViewDTO(
                role="ANALYST",
                visible_panels=["overview", "risk", "findings", "evidence", "graph", "timeline", "dataflow", "behavior", "threat_intel", "contradictions", "notes", "bookmarks", "cases"],
                show_raw_technical_data=True,
                show_audit_metadata=False,
                show_provenance_links=True,
                permissions=["report:view", "evidence:view", "finding:view", "finding:annotate", "case:view", "note:create"],
            )

    # -----------------------------------------------------------------------
    # Section 13-16: Interactive Evidence Graph Construction
    # -----------------------------------------------------------------------

    def build_evidence_graph(
        self,
        doc: ReportDocumentDTO,
        depth: int = 2,
        focused_node_id: Optional[str] = None,
        limit: int = 200,
    ) -> InvestigationGraphResponseDTO:
        nodes: List[GraphNodeDTO] = []
        edges: List[GraphEdgeDTO] = []
        node_ids = set()

        # 1. Root Analysis Node
        root_id = f"analysis_{doc.analysis_id}"
        nodes.append(
            GraphNodeDTO(
                id=root_id,
                label=f"Analysis: {doc.analysis_id}",
                type="ANALYSIS",
                category="ROOT",
                confidence="HIGH",
                risk_contribution=doc.trust_overview.risk_score,
                properties={"risk_band": doc.trust_overview.risk_band, "status": doc.status},
            )
        )
        node_ids.add(root_id)

        # 2. Risk Assessment Node
        risk_node_id = f"risk_{doc.analysis_id}"
        nodes.append(
            GraphNodeDTO(
                id=risk_node_id,
                label=f"Risk: {doc.trust_overview.risk_band} ({doc.trust_overview.risk_score:.1f})",
                type="RISK_FACTOR",
                category="DECISION",
                confidence=doc.trust_overview.confidence,
                risk_contribution=doc.trust_overview.risk_score,
                properties={"evidence_sufficiency": doc.trust_overview.evidence_sufficiency},
            )
        )
        node_ids.add(risk_node_id)
        edges.append(
            GraphEdgeDTO(
                id=f"edge_{root_id}_{risk_node_id}",
                source=root_id,
                target=risk_node_id,
                relationship="DERIVED_FROM",
                resolution_status="RESOLVED",
                confidence="HIGH",
            )
        )

        # 3. Finding Nodes
        for f in doc.major_findings[:limit]:
            f_node_id = f"finding_{f.finding_id}"
            sev = getattr(f, "severity_reference", getattr(f, "severity", "MEDIUM"))
            contrib = getattr(f, "risk_contribution", 0.0) or 0.0
            nodes.append(
                GraphNodeDTO(
                    id=f_node_id,
                    label=f.title,
                    type="FINDING",
                    category=f.category,
                    confidence=f.confidence,
                    risk_contribution=contrib,
                    properties={"severity": sev, "description": f.description},
                )
            )
            node_ids.add(f_node_id)

            edges.append(
                GraphEdgeDTO(
                    id=f"edge_{risk_node_id}_{f_node_id}",
                    source=f_node_id,
                    target=risk_node_id,
                    relationship="CONTRIBUTES_TO",
                    resolution_status="RESOLVED",
                    confidence=f.confidence,
                )
            )

        # 4. Evidence Nodes
        for ev in doc.evidence_cards[:limit]:
            ev_node_id = f"evidence_{ev.card_id}"
            nodes.append(
                GraphNodeDTO(
                    id=ev_node_id,
                    label=ev.title,
                    type="EVIDENCE",
                    category=ev.category,
                    confidence=ev.confidence,
                    properties={
                        "observation": ev.observation,
                        "strength": ev.evidence_strength,
                        "source": ev.source,
                        "provenance": ev.provenance,
                    },
                )
            )
            node_ids.add(ev_node_id)

            # Link evidence to finding if reference exists
            if ev.finding_reference:
                target_f_id = f"finding_{ev.finding_reference}"
                if target_f_id in node_ids:
                    edges.append(
                        GraphEdgeDTO(
                            id=f"edge_{ev_node_id}_{target_f_id}",
                            source=ev_node_id,
                            target=target_f_id,
                            relationship="SUPPORTS",
                            resolution_status="RESOLVED",
                            confidence=ev.confidence,
                        )
                    )
            else:
                # Link to root analysis if no specific finding
                edges.append(
                    GraphEdgeDTO(
                        id=f"edge_{ev_node_id}_{root_id}",
                        source=ev_node_id,
                        target=root_id,
                        relationship="DERIVED_FROM",
                        resolution_status="RESOLVED",
                        confidence=ev.confidence,
                    )
                )

        # 5. Threat Intelligence Nodes
        if doc.threat_intelligence and doc.threat_intelligence.observed_indicators:
            for ioc in doc.threat_intelligence.observed_indicators[:limit]:
                ioc_node_id = f"ioc_{ioc.indicator_value}"
                nodes.append(
                    GraphNodeDTO(
                        id=ioc_node_id,
                        label=f"{ioc.indicator_type}: {ioc.indicator_value}",
                        type="IOC",
                        category="THREAT_INTEL",
                        confidence=ioc.confidence,
                        properties={"match_type": ioc.match_type, "freshness": ioc.freshness},
                    )
                )
                node_ids.add(ioc_node_id)

                # Link IOC to risk node
                edges.append(
                    GraphEdgeDTO(
                        id=f"edge_{ioc_node_id}_{risk_node_id}",
                        source=ioc_node_id,
                        target=risk_node_id,
                        relationship="MATCHES",
                        resolution_status="RESOLVED",
                        confidence=ioc.confidence,
                    )
                )

        return InvestigationGraphResponseDTO(
            analysis_id=doc.analysis_id,
            nodes=nodes,
            edges=edges,
            total_nodes=len(nodes),
            total_edges=len(edges),
            truncated=len(nodes) >= limit,
        )

    # -----------------------------------------------------------------------
    # Sections 19-20: Chronological Investigation Timeline
    # -----------------------------------------------------------------------

    def build_timeline(self, doc: ReportDocumentDTO, additional_events: Optional[List[Dict[str, Any]]] = None) -> TimelineResponseDTO:
        events: List[TimelineEventDTO] = []

        # 1. Analysis Started
        gen_time = doc.generated_at or datetime.now(timezone.utc).isoformat()
        events.append(
            TimelineEventDTO(
                event_id=f"evt_start_{doc.analysis_id}",
                analysis_id=doc.analysis_id,
                timestamp=gen_time,
                event_type="ANALYSIS_STARTED",
                title="Analysis Initialized",
                description=f"Automated multi-module security scan started for analysis {doc.analysis_id}.",
                severity="INFORMATIONAL",
                source_module="ENGINE",
            )
        )

        # 2. Evidence Observed
        for idx, ev in enumerate(doc.evidence_cards):
            events.append(
                TimelineEventDTO(
                    event_id=f"evt_ev_{ev.card_id}_{idx}",
                    analysis_id=doc.analysis_id,
                    timestamp=gen_time,
                    event_type="EVIDENCE_OBSERVED",
                    title=f"Evidence Observed: {ev.title}",
                    description=ev.observation,
                    severity="LOW" if ev.evidence_strength in ["WEAK", "INDIRECT"] else "MEDIUM",
                    source_module=ev.source or "CORE",
                    related_entity_id=ev.card_id,
                )
            )

        # 3. Findings Created
        for idx, f in enumerate(doc.major_findings):
            sev = getattr(f, "severity_reference", getattr(f, "severity", "MEDIUM"))
            events.append(
                TimelineEventDTO(
                    event_id=f"evt_f_{f.finding_id}_{idx}",
                    analysis_id=doc.analysis_id,
                    timestamp=gen_time,
                    event_type="FINDING_CREATED",
                    title=f"Finding Flagged: {f.title}",
                    description=f.description,
                    severity=sev,
                    source_module=f.category,
                    related_entity_id=f.finding_id,
                )
            )

        # 4. Threat Intel Matches
        if doc.threat_intelligence and doc.threat_intelligence.threat_feed_matches:
            for idx, tf in enumerate(doc.threat_intelligence.threat_feed_matches):
                events.append(
                    TimelineEventDTO(
                        event_id=f"evt_ti_{idx}",
                        analysis_id=doc.analysis_id,
                        timestamp=gen_time,
                        event_type="THREAT_MATCH",
                        title=f"Threat Match: {tf.indicator_value}",
                        description=f"Correlated with threat feed {tf.threat_feed_name} ({tf.threat_type}).",
                        severity=tf.severity,
                        source_module="THREAT_INTEL",
                    )
                )

        # 5. Risk Assessment Decision
        events.append(
            TimelineEventDTO(
                event_id=f"evt_risk_{doc.analysis_id}",
                analysis_id=doc.analysis_id,
                timestamp=gen_time,
                event_type="RISK_ASSESSMENT",
                title=f"Risk Evaluated: {doc.trust_overview.risk_band} ({doc.trust_overview.risk_score:.1f}/100)",
                description=f"Cybersecurity Decision Engine assessed confidence at {doc.trust_overview.confidence}.",
                severity="HIGH" if doc.trust_overview.risk_band in ["HIGH_RISK", "CRITICAL_RISK"] else "MEDIUM",
                source_module="RISK_ENGINE",
            )
        )

        # 6. Report Generated
        rep_ver = getattr(doc, "report_version", getattr(doc, "version", "1.0.0"))
        events.append(
            TimelineEventDTO(
                event_id=f"evt_report_{doc.report_id}",
                analysis_id=doc.analysis_id,
                timestamp=gen_time,
                event_type="REPORT_GENERATED",
                title=f"Digital Trust Report v{rep_ver} Generated",
                description=f"Authoritative report document {doc.report_id} finalized and sealed.",
                severity="INFORMATIONAL",
                source_module="REPORT_GENERATOR",
                related_entity_id=doc.report_id,
            )
        )


        # Sort chronologically
        events.sort(key=lambda x: x.timestamp)

        return TimelineResponseDTO(
            analysis_id=doc.analysis_id,
            events=events,
            total_events=len(events),
        )

    # -----------------------------------------------------------------------
    # Sections 52-54: Unified Investigation Search
    # -----------------------------------------------------------------------

    def search_investigation(
        self,
        query: str,
        doc: ReportDocumentDTO,
        notes: Optional[List[Dict[str, Any]]] = None,
        limit: int = 50,
    ) -> InvestigationSearchResponseDTO:
        q = (query or "").lower().strip()
        results: List[InvestigationSearchResultDTO] = []
        if not q:
            return InvestigationSearchResponseDTO(query=query, results=[], total_results=0)

        # 1. Search Findings
        for f in doc.major_findings:
            if (
                q in f.finding_id.lower()
                or q in f.title.lower()
                or q in f.description.lower()
                or q in f.category.lower()
            ):
                sev = getattr(f, "severity_reference", getattr(f, "severity", "MEDIUM"))
                results.append(
                    InvestigationSearchResultDTO(
                        object_type="FINDING",
                        object_id=f.finding_id,
                        title=f.title,
                        summary=f.description[:120],
                        risk_reference=sev,
                        timestamp=doc.generated_at,
                        source_module=f.category,
                    )
                )


        # 2. Search Evidence
        for ev in doc.evidence_cards:
            if (
                q in ev.card_id.lower()
                or q in ev.title.lower()
                or q in ev.observation.lower()
                or q in ev.category.lower()
                or (ev.source and q in ev.source.lower())
            ):
                results.append(
                    InvestigationSearchResultDTO(
                        object_type="EVIDENCE",
                        object_id=ev.card_id,
                        title=ev.title,
                        summary=ev.observation[:120],
                        risk_reference=ev.evidence_strength,
                        timestamp=doc.generated_at,
                        source_module=ev.source or "CORE",
                    )
                )

        # 3. Search Threat Intel
        if doc.threat_intelligence and doc.threat_intelligence.observed_indicators:
            for ioc in doc.threat_intelligence.observed_indicators:
                if q in ioc.indicator_value.lower() or q in ioc.indicator_type.lower():
                    results.append(
                        InvestigationSearchResultDTO(
                            object_type="IOC",
                            object_id=ioc.indicator_value,
                            title=f"{ioc.indicator_type}: {ioc.indicator_value}",
                            summary=f"Threat Match: {ioc.match_type} (Confidence: {ioc.confidence})",
                            risk_reference=ioc.confidence,
                            timestamp=doc.generated_at,
                            source_module="THREAT_INTEL",
                        )
                    )

        # 4. Search Notes
        if notes:
            for n in notes:
                content = n.get("content", "")
                if q in content.lower():
                    results.append(
                        InvestigationSearchResultDTO(
                            object_type="NOTE",
                            object_id=n.get("note_id", ""),
                            title=f"Analyst Note ({n.get('note_type', 'GENERAL')})",
                            summary=content[:120],
                            risk_reference=None,
                            timestamp=n.get("created_at", doc.generated_at),
                            source_module="ANALYST",
                        )
                    )

        return InvestigationSearchResponseDTO(
            query=query,
            results=results[:limit],
            total_results=len(results),
        )

    # -----------------------------------------------------------------------
    # Section 17-18: Cross-Modal Synthetic Correlations
    # -----------------------------------------------------------------------

    def build_cross_modal_correlations(
        self,
        case_id: str,
        analyses: List[Dict[str, Any]],
        reports: List[ReportDocumentDTO],
    ) -> CrossModalCorrelationResponseDTO:
        correlations: List[InvestigationCorrelationDTO] = []
        if len(reports) < 2:
            return CrossModalCorrelationResponseDTO(case_id=case_id, correlations=[], total_correlations=0)

        # Correlate findings across reports based on shared categories or IOCs
        for i in range(len(reports)):
            for j in range(i + 1, len(reports)):
                rep_a = reports[i]
                rep_b = reports[j]

                for fa in rep_a.major_findings:
                    for fb in rep_b.major_findings:
                        if fa.category == fb.category:
                            corr = InvestigationCorrelationDTO(
                                correlation_id=f"corr_{uuid.uuid4().hex[:12]}",
                                case_id=case_id,
                                source_analysis_id=rep_a.analysis_id,
                                target_analysis_id=rep_b.analysis_id,
                                source_module=fa.category,
                                target_module=fb.category,
                                source_finding_id=fa.finding_id,
                                target_finding_id=fb.finding_id,
                                relationship="CORRELATED_WITH",
                                confidence="HIGH",
                                evidence_reference=f"{fa.finding_id} <-> {fb.finding_id}",
                                created_at=datetime.now(timezone.utc).isoformat(),
                            )
                            correlations.append(corr)

        return CrossModalCorrelationResponseDTO(
            case_id=case_id,
            correlations=correlations,
            total_correlations=len(correlations),
        )
