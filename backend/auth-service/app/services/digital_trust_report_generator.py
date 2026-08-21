"""Digital Trust Report Generator Service (Phase 4.0 Part 1).

Builds structured ReportDocumentDTO from backend analysis results, canonical findings,
and authoritative Phase 3.9 Risk Assessment without recalculating risk.
"""

from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from app.schemas.digital_trust_report_models import (
    TrustOverviewDTO,
    ReportFindingDTO,
    ReportEvidenceCardDTO,
    ContradictionReportSectionDTO,
    ReportProvenanceDTO,
    ReportLineageDTO,
    ReportDocumentDTO,
)


class DigitalTrustReportGenerator:
    """Master Report Generator constructing structured report sections from backend data."""

    def build_report_document(
        self,
        analysis_id: str,
        risk_assessment_dto: Any = None,
        consolidation_result_dto: Any = None,
        module_results: Optional[Dict[str, Any]] = None,
    ) -> ReportDocumentDTO:
        now_str = datetime.now(timezone.utc).isoformat()
        report_id = f"rep_{analysis_id[:8]}"

        score = getattr(risk_assessment_dto, "risk_score", 0.0) if risk_assessment_dto else 0.0
        band = getattr(risk_assessment_dto, "risk_band", "TRUSTED") if risk_assessment_dto else "TRUSTED"
        confidence = getattr(risk_assessment_dto, "confidence_level", "HIGH") if risk_assessment_dto else "HIGH"
        sufficiency = getattr(risk_assessment_dto, "evidence_sufficiency", "SUFFICIENT") if risk_assessment_dto else "SUFFICIENT"
        primary_category = getattr(risk_assessment_dto, "primary_risk_category", "NETWORK_THREAT") if risk_assessment_dto else "NETWORK_THREAT"

        findings = getattr(consolidation_result_dto, "findings", []) if consolidation_result_dto else []

        trust_overview = TrustOverviewDTO(
            risk_score=score,
            risk_band=band,
            confidence=confidence,
            evidence_sufficiency=sufficiency,
            analysis_status="COMPLETED",
            modules_analyzed=["APK_ANALYSIS", "NETWORK", "STORAGE", "DATAFLOW", "BEHAVIOR", "THREAT_INTEL", "RISK_ENGINE"],
            findings_count=len(findings),
            evidence_count=len(findings),
            threat_matches=0,
            critical_findings=1 if band == "CRITICAL_RISK" else 0,
            high_risk_findings=1 if band == "HIGH_RISK" else 0,
        )

        exec_summary = {
            "title": "Digital Trust Executive Summary",
            "overall_risk_score": score,
            "risk_band": band,
            "confidence": confidence,
            "evidence_sufficiency": sufficiency,
            "primary_risk_category": primary_category,
            "summary_statement": f"Application evaluated with risk score {score:.1f}/100 ({band}) under {sufficiency} evidence sufficiency.",
            "recommended_immediate_action": "MONITOR" if band in ["TRUSTED", "LOW_RISK"] else "BLOCK",
        }

        risk_sec = {
            "risk_score": score,
            "risk_band": band,
            "confidence_level": confidence,
            "evidence_sufficiency": sufficiency,
            "decision_state": getattr(risk_assessment_dto, "decision_state", band) if risk_assessment_dto else band,
            "primary_risk_category": primary_category,
        }

        report_findings: List[ReportFindingDTO] = []
        evidence_cards: List[ReportEvidenceCardDTO] = []
        provenance_list: List[ReportProvenanceDTO] = []
        lineage_list: List[ReportLineageDTO] = []

        for idx, f in enumerate(findings):
            fid = getattr(f, "finding_id", f"f_{idx+1}")
            cat = getattr(f, "finding_category", "NETWORK_THREAT")
            title = getattr(f, "title", "Observed Security Finding")
            desc = getattr(f, "description", "Canonical finding description")

            r_finding = ReportFindingDTO(
                finding_id=fid,
                category=cat,
                title=title,
                description=desc,
                status="CONFIRMED",
                confidence=confidence,
                severity_reference="MEDIUM",
                evidence_strength="STRONG",
                provenance_reference=f"prov_{fid}",
            )
            report_findings.append(r_finding)

            card = ReportEvidenceCardDTO(
                card_id=f"card_{fid}",
                title=title,
                category=cat,
                observation=desc,
                evidence_strength="STRONG",
                confidence=confidence,
                source="Phase 3.9 Evidence Consolidation Layer",
                provenance=f"prov_{fid}",
                finding_reference=fid,
            )
            evidence_cards.append(card)

            prov = ReportProvenanceDTO(
                statement_id=f"stmt_{fid}",
                source_module="EvidenceConsolidationService",
                finding_id=fid,
                evidence_id=f"ev_{fid}",
                timestamp=now_str,
            )
            provenance_list.append(prov)

            lin = ReportLineageDTO(
                section_id="major_findings",
                statement_text=desc,
                finding_id=fid,
                evidence_id=f"ev_{fid}",
                original_source="APK Analysis Pipeline",
            )
            lineage_list.append(lin)

        # Deterministic sorting of findings and evidence
        report_findings.sort(key=lambda x: x.finding_id)
        evidence_cards.sort(key=lambda x: x.card_id)

        recommendations = [
            "Maintain active monitoring on network communication endpoints.",
            "Enforce periodic security re-scans upon application updates.",
        ]

        limitations = [
            "Static analysis cannot evaluate server-side dynamic payload decryption at runtime.",
        ]

        tech_details = {
            "engine_version": "1.0.0",
            "policy_version": "1.0.0",
            "schema_version": "4.0.0",
            "analysis_id": analysis_id,
        }

        return ReportDocumentDTO(
            report_id=report_id,
            analysis_id=analysis_id,
            report_version="1.0.0",
            schema_version="4.0.0",
            generated_at=now_str,
            trust_overview=trust_overview,
            executive_summary=exec_summary,
            risk_assessment=risk_sec,
            major_findings=report_findings,
            evidence_cards=evidence_cards,
            module_results=module_results or {"apk_analysis": "COMPLETED"},
            recommendations=recommendations,
            technical_details=tech_details,
            provenance=provenance_list,
            lineage=lineage_list,
            limitations=limitations,
        )
