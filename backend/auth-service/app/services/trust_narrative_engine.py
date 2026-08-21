"""Trust Narrative Engine — Core Service (Phase 4.0 Part 2).

Deterministic, evidence-grounded explanation engine that transforms authoritative
structured analysis results into human-readable narratives. Contains sub-generators
for executive summaries, risk, findings, evidence, dataflow, behavior, threat intel,
contradictions, mitigations, recommendations, technical/user/analyst summaries, and
module-specific narratives (Website, QR/UPI, Document, Deepfake, Audio, APK, NLP).

THIS MODULE IS NOT AN ANALYSIS ENGINE. It MUST NOT independently detect, classify,
calculate risk, recalculate confidence, create evidence, or override upstream findings.
"""

from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from app.schemas.trust_narrative_models import (
    NarrativeStatementDTO,
    ExecutiveSummaryNarrativeDTO,
    RiskNarrativeDTO,
    FindingNarrativeDTO,
    EvidenceNarrativeDTO,
    ContradictionNarrativeDTO,
    NarrativeLineageDTO,
    NarrativeDocumentDTO,
    NarrativeValidationDTO,
)


# ---------------------------------------------------------------------------
# Controlled Vocabulary (Section 5)
# ---------------------------------------------------------------------------

CONTROLLED_VOCABULARY = {
    "malicious": "potentially malicious behavior",
    "steals_data": "dataflow from [data category] toward an external network sink",
    "scam": "indicators associated with [scam category]",
    "no_malware": "no high-confidence malicious indicators were identified in the analyzed scope",
    "safe": "no high-confidence threats were identified within the analyzed scope",
}

# ---------------------------------------------------------------------------
# Certainty States (Section 6)
# ---------------------------------------------------------------------------

CERTAINTY_STATES = [
    "DETECTED", "NOT_DETECTED", "NOT_ANALYZED", "UNKNOWN",
    "UNRESOLVED", "PARTIALLY_RESOLVED", "CONFLICTED", "INSUFFICIENT_EVIDENCE",
]

# ---------------------------------------------------------------------------
# Claim Strength Hierarchy (Section 4)
# ---------------------------------------------------------------------------

CLAIM_STRENGTH_ORDER = [
    "DIRECTLY_OBSERVED", "STRONGLY_SUPPORTED", "SUPPORTED", "CORRELATED",
    "INFERRED", "PARTIALLY_SUPPORTED", "UNRESOLVED", "CONFLICTED", "UNKNOWN",
]

# ---------------------------------------------------------------------------
# Risk Band Language (Section 10)
# ---------------------------------------------------------------------------

RISK_BAND_LANGUAGE = {
    "TRUSTED": "The analysis identified no significant security concerns within the analyzed scope.",
    "LOW_RISK": "The analysis identified low-severity indicators. No immediate action is required.",
    "MODERATE_RISK": "The analysis identified moderate indicators warranting further review.",
    "HIGH_RISK": "The analysis identified high-confidence indicators associated with elevated security risk.",
    "CRITICAL_RISK": "The analysis identified critical indicators associated with severe security risk requiring immediate action.",
}

# ---------------------------------------------------------------------------
# Multilingual Translations (Section 34-35)
# ---------------------------------------------------------------------------

RISK_BAND_TRANSLATIONS = {
    "en": {"TRUSTED": "Trusted", "LOW_RISK": "Low Risk", "MODERATE_RISK": "Moderate Risk", "HIGH_RISK": "High Risk", "CRITICAL_RISK": "Critical Risk"},
    "hi": {"TRUSTED": "विश्वसनीय", "LOW_RISK": "कम जोखिम", "MODERATE_RISK": "मध्यम जोखिम", "HIGH_RISK": "उच्च जोखिम", "CRITICAL_RISK": "गंभीर जोखिम"},
    "pa": {"TRUSTED": "ਭਰੋਸੇਮੰਦ", "LOW_RISK": "ਘੱਟ ਖ਼ਤਰਾ", "MODERATE_RISK": "ਦਰਮਿਆਨਾ ਖ਼ਤਰਾ", "HIGH_RISK": "ਉੱਚ ਖ਼ਤਰਾ", "CRITICAL_RISK": "ਗੰਭੀਰ ਖ਼ਤਰਾ"},
}


# ============================================================================
# Sub-Generators
# ============================================================================

class ExecutiveSummaryGenerator:
    """Section 7-8: Executive Summary Generator."""

    def generate(self, risk_score: float, risk_band: str, confidence: str,
                 evidence_sufficiency: str, findings: list, limitations: list,
                 primary_category: str = "NETWORK_THREAT") -> ExecutiveSummaryNarrativeDTO:
        headline = f"Digital Trust Assessment — {risk_band.replace('_', ' ').title()}"
        overall = RISK_BAND_LANGUAGE.get(risk_band, "Assessment completed.")
        top = [f.title if hasattr(f, "title") else str(f) for f in findings[:5]]
        risk_expl = f"Risk Score: {risk_score:.1f} / 100 — Risk Band: {risk_band} — Confidence: {confidence} — Evidence Sufficiency: {evidence_sufficiency}."
        if risk_band in ("HIGH_RISK", "CRITICAL_RISK"):
            action = "Immediate review and remediation are recommended based on the analysis findings."
        elif risk_band == "MODERATE_RISK":
            action = "Further review is recommended to assess the identified indicators."
        else:
            action = "Continue monitoring. No immediate action is required."
        conf_stmt = f"The assessment confidence is {confidence} with {evidence_sufficiency.lower()} evidence."
        lim = limitations if limitations else ["Static analysis cannot evaluate server-side dynamic payload decryption at runtime."]
        primary = top[0] if top else ""
        return ExecutiveSummaryNarrativeDTO(
            headline=headline, overall_assessment=overall, primary_concern=primary,
            top_findings=top, risk_explanation=risk_expl, recommended_action=action,
            confidence_statement=conf_stmt, limitations=lim,
        )


class RiskNarrativeGenerator:
    """Section 9-11: Risk Narrative Generator."""

    def generate(self, risk_score: float, risk_band: str, confidence: str,
                 evidence_sufficiency: str, primary_category: str,
                 risk_factors: list, mitigations: list, protective: list,
                 uncertainties: list) -> RiskNarrativeDTO:
        stmt = f"Risk Score: {risk_score:.1f} / 100. Risk Band: {risk_band}. Confidence: {confidence}. Evidence Sufficiency: {evidence_sufficiency}."
        primary_expl = f"{risk_band} is primarily associated with {primary_category.replace('_', ' ').lower()} indicators."
        cats = [f"{rf}" for rf in risk_factors[:5]] if risk_factors else []
        mits = [str(m) for m in mitigations[:5]] if mitigations else []
        prots = [str(p) for p in protective[:5]] if protective else []
        unc = uncertainties[0] if uncertainties else "No significant unresolved uncertainty was identified."
        return RiskNarrativeDTO(
            risk_statement=stmt, primary_risk_explanation=primary_expl,
            category_explanations=cats, top_contributing_factors=cats,
            mitigating_factors=mits, protective_factors=prots, uncertainty=unc,
        )


class UncertaintyExplanationGenerator:
    """Section 12: Uncertainty Explanation Generator."""

    def explain(self, confidence: str, evidence_sufficiency: str,
                unresolved_items: list) -> str:
        parts = []
        if confidence in ("LOW", "VERY_LOW"):
            parts.append("Confidence is limited due to insufficient or conflicting evidence.")
        if evidence_sufficiency == "INSUFFICIENT":
            parts.append("Evidence sufficiency is insufficient for a definitive assessment.")
        for item in unresolved_items[:3]:
            parts.append(f"Unresolved: {item}.")
        return " ".join(parts) if parts else "No significant unresolved uncertainty was identified."


class FindingNarrativeGenerator:
    """Section 14: Finding Narrative Generator."""

    def generate(self, finding) -> FindingNarrativeDTO:
        fid = getattr(finding, "finding_id", "unknown")
        title = getattr(finding, "title", "Security Finding")
        desc = getattr(finding, "description", "")
        confidence = getattr(finding, "confidence", getattr(finding, "confidence_level", "HIGH"))
        cat = getattr(finding, "finding_category", getattr(finding, "category", "UNKNOWN"))
        why = f"This finding is relevant because it is associated with {cat.replace('_', ' ').lower()} indicators."
        not_est = "API usage alone does not establish that data was transmitted externally." if "API" in desc else ""
        action = "Further review recommended." if confidence in ("LOW", "VERY_LOW", "MEDIUM") else "Monitor and assess."
        return FindingNarrativeDTO(
            finding_id=fid, title=title, what_was_found=desc,
            confidence=confidence, why_it_matters=why,
            what_is_not_established=not_est, recommended_action=action,
            provenance=f"prov_{fid}",
        )


class EvidenceNarrativeGenerator:
    """Section 13: Evidence Narrative Generator."""

    def generate(self, evidence) -> EvidenceNarrativeDTO:
        eid = getattr(evidence, "evidence_id", getattr(evidence, "card_id", "ev_unknown"))
        obs = getattr(evidence, "observation", getattr(evidence, "description", "Evidence observed."))
        strength = getattr(evidence, "evidence_strength", "STRONG")
        source = getattr(evidence, "source", getattr(evidence, "source_module", "Analysis Engine"))
        why = f"This evidence is relevant because it supports a security finding."
        lims = ["Evidence alone does not establish malicious intent without additional context."]
        return EvidenceNarrativeDTO(
            evidence_id=eid, what_was_observed=obs, why_it_matters=why,
            evidence_strength=strength, source=source, limitations=lims,
        )


class DataflowNarrativeGenerator:
    """Section 15: Dataflow Narrative Generator."""

    def generate(self, dataflow_paths: list) -> List[NarrativeStatementDTO]:
        stmts = []
        for i, path in enumerate(dataflow_paths[:10]):
            resolved = getattr(path, "resolution_status", "RESOLVED") if hasattr(path, "resolution_status") else "RESOLVED"
            source = getattr(path, "source", "data source") if hasattr(path, "source") else "data source"
            sink = getattr(path, "sink", "network sink") if hasattr(path, "sink") else "network sink"
            if resolved == "RESOLVED":
                claim = f"Analysis identified a resolved path from {source} to {sink}."
                strength = "DIRECTLY_OBSERVED"
            else:
                claim = f"Analysis identified a potential path from {source}-related functionality, but the complete destination could not be resolved."
                strength = "PARTIALLY_SUPPORTED"
            stmts.append(NarrativeStatementDTO(
                statement_id=f"df_stmt_{i+1}", statement_type="DATAFLOW",
                source_type="DATAFLOW_PATH", source_id=getattr(path, "path_id", f"path_{i+1}"),
                claim=claim, claim_strength=strength, confidence="HIGH" if resolved == "RESOLVED" else "LOW",
            ))
        return stmts


class BehaviorNarrativeGenerator:
    """Section 16: Behavior Chain Narrative Generator."""

    def generate(self, behavior_chains: list) -> List[NarrativeStatementDTO]:
        stmts = []
        for i, chain in enumerate(behavior_chains[:10]):
            nodes = getattr(chain, "nodes", []) if hasattr(chain, "nodes") else []
            if nodes:
                node_str = " → ".join(str(n) for n in nodes[:5])
                claim = f"The analyzed application exhibits a behavior chain: {node_str}."
            else:
                claim = f"A behavioral correlation pattern was identified."
            stmts.append(NarrativeStatementDTO(
                statement_id=f"beh_stmt_{i+1}", statement_type="BEHAVIOR",
                source_type="BEHAVIOR_CHAIN", source_id=f"chain_{i+1}",
                claim=claim, claim_strength="CORRELATED",
            ))
        return stmts


class ThreatIntelNarrativeGenerator:
    """Section 17: Threat Intelligence Narrative Generator."""

    def generate(self, threat_matches: list) -> List[NarrativeStatementDTO]:
        stmts = []
        for i, match in enumerate(threat_matches[:10]):
            freshness = getattr(match, "freshness", "CURRENT") if hasattr(match, "freshness") else "CURRENT"
            indicator = getattr(match, "indicator", "endpoint") if hasattr(match, "indicator") else "endpoint"
            if freshness == "STALE":
                claim = f"The analyzed {indicator} matches an older threat-intelligence record, but the record is stale and therefore provides weaker current attribution."
                strength = "PARTIALLY_SUPPORTED"
            else:
                claim = f"The analyzed {indicator} matches a threat-intelligence indicator currently classified as malicious by the configured intelligence source."
                strength = "STRONGLY_SUPPORTED"
            stmts.append(NarrativeStatementDTO(
                statement_id=f"ti_stmt_{i+1}", statement_type="THREAT_INTELLIGENCE",
                source_type="THREAT_MATCH", source_id=f"match_{i+1}",
                claim=claim, claim_strength=strength,
            ))
        return stmts


class ContradictionNarrativeGenerator:
    """Section 18: Contradiction Narrative Generator."""

    def generate(self, contradictions: list) -> List[ContradictionNarrativeDTO]:
        narrs = []
        for i, c in enumerate(contradictions[:10]):
            ea = getattr(c, "evidence_a", "Source A") if hasattr(c, "evidence_a") else "Source A"
            eb = getattr(c, "evidence_b", "Source B") if hasattr(c, "evidence_b") else "Source B"
            narr = f"Two evidence sources provide conflicting assessments. Because the evidence is unresolved, confidence in this finding is reduced."
            narrs.append(ContradictionNarrativeDTO(
                contradiction_id=f"contr_{i+1}", narrative=narr,
                evidence_a=str(ea), evidence_b=str(eb), resolution_status="UNRESOLVED",
            ))
        return narrs


class MitigationNarrativeGenerator:
    """Section 19-20: Mitigation and Protective Control Narrative Generator."""

    def generate(self, mitigations: list) -> List[NarrativeStatementDTO]:
        stmts = []
        for i, m in enumerate(mitigations[:10]):
            mit_str = str(m) if not hasattr(m, "name") else m.name
            claim = f"{mit_str} provides a protective control, but it does not eliminate independently observed risk indicators."
            stmts.append(NarrativeStatementDTO(
                statement_id=f"mit_stmt_{i+1}", statement_type="MITIGATION",
                source_type="RISK_FACTOR", source_id=f"mit_{i+1}",
                claim=claim, claim_strength="SUPPORTED",
            ))
        return stmts


class RecommendationExplanationGenerator:
    """Section 21-22: Recommendation Explanation Generator."""

    def generate(self, recommendations: list, risk_band: str) -> List[NarrativeStatementDTO]:
        stmts = []
        for i, rec in enumerate(recommendations[:10]):
            rec_text = str(rec)
            if risk_band in ("HIGH_RISK", "CRITICAL_RISK"):
                priority = "IMMEDIATE"
            elif risk_band == "MODERATE_RISK":
                priority = "HIGH"
            else:
                priority = "MEDIUM"
            claim = f"Recommendation ({priority}): {rec_text}."
            stmts.append(NarrativeStatementDTO(
                statement_id=f"rec_stmt_{i+1}", statement_type="RECOMMENDATION",
                source_type="RECOMMENDATION", source_id=f"rec_{i+1}",
                claim=claim, claim_strength="SUPPORTED",
            ))
        return stmts


class TechnicalSummaryGenerator:
    """Section 31: Technical Summary Generator."""

    def generate(self, doc) -> str:
        score = getattr(doc, "trust_overview", None)
        rs = score.risk_score if score else 0.0
        rb = score.risk_band if score else "TRUSTED"
        return f"Technical Summary — Engine v1.0.0 — Risk Score: {rs:.1f}/100 — Risk Band: {rb} — Schema: 4.0.0."


class UserFriendlySummaryGenerator:
    """Section 32: User-Friendly Summary Generator."""

    def generate(self, doc) -> str:
        score = getattr(doc, "trust_overview", None)
        rs = score.risk_score if score else 0.0
        rb = score.risk_band if score else "TRUSTED"
        if rb in ("HIGH_RISK", "CRITICAL_RISK"):
            return f"This analysis found security concerns. The risk score is {rs:.1f} out of 100 ({rb.replace('_', ' ').lower()}). We recommend immediate review."
        elif rb == "MODERATE_RISK":
            return f"This analysis found some indicators worth reviewing. The risk score is {rs:.1f} out of 100. Further assessment may be helpful."
        else:
            return f"This analysis did not find significant security concerns. The risk score is {rs:.1f} out of 100. No immediate action is needed."


class AnalystSummaryGenerator:
    """Section 33: Security Analyst Summary Generator."""

    def generate(self, doc, findings: list) -> str:
        score = getattr(doc, "trust_overview", None)
        rs = score.risk_score if score else 0.0
        rb = score.risk_band if score else "TRUSTED"
        finding_ids = [getattr(f, "finding_id", str(f)) for f in findings[:10]]
        fids = ", ".join(finding_ids) if finding_ids else "None"
        return f"Analyst Summary — Risk: {rs:.1f}/100 ({rb}) — Findings: [{fids}] — Provenance references available for each finding."


# ---------------------------------------------------------------------------
# Module-Specific Generators (Section 23-30)
# ---------------------------------------------------------------------------

class WebsiteNarrativeGenerator:
    def generate(self, module_result: dict) -> str:
        return f"Website analysis: {module_result.get('status', 'COMPLETED')}."

class QRUPINarrativeGenerator:
    def generate(self, module_result: dict) -> str:
        return f"QR/UPI analysis: {module_result.get('status', 'COMPLETED')}."

class DocumentNarrativeGenerator:
    def generate(self, module_result: dict) -> str:
        return f"Document analysis: {module_result.get('status', 'COMPLETED')}."

class DeepfakeNarrativeGenerator:
    def generate(self, module_result: dict) -> str:
        return f"Deepfake analysis: {module_result.get('status', 'COMPLETED')}."

class AudioNarrativeGenerator:
    def generate(self, module_result: dict) -> str:
        return f"Audio analysis: {module_result.get('status', 'COMPLETED')}."

class APKMalwareNarrativeGenerator:
    def generate(self, module_result: dict) -> str:
        return f"APK malware analysis: {module_result.get('status', 'COMPLETED')}."

class NLPPhishingNarrativeGenerator:
    def generate(self, module_result: dict) -> str:
        return f"NLP phishing analysis: {module_result.get('status', 'COMPLETED')}."


# ============================================================================
# Master TrustNarrativeEngine
# ============================================================================

class TrustNarrativeEngine:
    """Master Narrative Engine composing all sub-generators into a full NarrativeDocument."""

    def __init__(self):
        self.exec_gen = ExecutiveSummaryGenerator()
        self.risk_gen = RiskNarrativeGenerator()
        self.uncertainty_gen = UncertaintyExplanationGenerator()
        self.finding_gen = FindingNarrativeGenerator()
        self.evidence_gen = EvidenceNarrativeGenerator()
        self.dataflow_gen = DataflowNarrativeGenerator()
        self.behavior_gen = BehaviorNarrativeGenerator()
        self.threat_gen = ThreatIntelNarrativeGenerator()
        self.contradiction_gen = ContradictionNarrativeGenerator()
        self.mitigation_gen = MitigationNarrativeGenerator()
        self.recommendation_gen = RecommendationExplanationGenerator()
        self.tech_gen = TechnicalSummaryGenerator()
        self.user_gen = UserFriendlySummaryGenerator()
        self.analyst_gen = AnalystSummaryGenerator()
        # Module-specific
        self.website_gen = WebsiteNarrativeGenerator()
        self.qr_gen = QRUPINarrativeGenerator()
        self.doc_gen = DocumentNarrativeGenerator()
        self.deepfake_gen = DeepfakeNarrativeGenerator()
        self.audio_gen = AudioNarrativeGenerator()
        self.apk_gen = APKMalwareNarrativeGenerator()
        self.nlp_gen = NLPPhishingNarrativeGenerator()

    def build_narrative(
        self,
        report_id: str,
        analysis_id: str,
        report_doc: Any = None,
        risk_assessment_dto: Any = None,
        findings: Optional[list] = None,
        evidence: Optional[list] = None,
        recommendations: Optional[list] = None,
        dataflow_paths: Optional[list] = None,
        behavior_chains: Optional[list] = None,
        threat_matches: Optional[list] = None,
        contradictions: Optional[list] = None,
        mitigations: Optional[list] = None,
        protective_factors: Optional[list] = None,
        limitations: Optional[list] = None,
        language: str = "en",
    ) -> NarrativeDocumentDTO:
        findings = findings or []
        evidence = evidence or []
        recommendations = recommendations or []
        dataflow_paths = dataflow_paths or []
        behavior_chains = behavior_chains or []
        threat_matches = threat_matches or []
        contradictions = contradictions or []
        mitigations = mitigations or []
        protective_factors = protective_factors or []
        limitations = limitations or ["Static analysis cannot evaluate server-side dynamic payload decryption at runtime."]

        # Extract authoritative values
        score = getattr(risk_assessment_dto, "risk_score", 0.0) if risk_assessment_dto else 0.0
        band = getattr(risk_assessment_dto, "risk_band", "TRUSTED") if risk_assessment_dto else "TRUSTED"
        conf = getattr(risk_assessment_dto, "confidence_level", "HIGH") if risk_assessment_dto else "HIGH"
        suff = getattr(risk_assessment_dto, "evidence_sufficiency", "SUFFICIENT") if risk_assessment_dto else "SUFFICIENT"
        pcat = getattr(risk_assessment_dto, "primary_risk_category", "NETWORK_THREAT") if risk_assessment_dto else "NETWORK_THREAT"

        # Executive Summary
        exec_summary = self.exec_gen.generate(score, band, conf, suff, findings, limitations, pcat)

        # Risk Narrative
        risk_factors_strs = [getattr(f, "title", str(f)) for f in findings[:5]]
        risk_narr = self.risk_gen.generate(score, band, conf, suff, pcat, risk_factors_strs, mitigations, protective_factors, [])

        # Finding Narratives
        finding_narrs = [self.finding_gen.generate(f) for f in findings]
        finding_narrs.sort(key=lambda x: x.finding_id)

        # Evidence Narratives
        evidence_narrs = [self.evidence_gen.generate(e) for e in evidence]
        evidence_narrs.sort(key=lambda x: x.evidence_id)

        # Dataflow
        df_stmts = self.dataflow_gen.generate(dataflow_paths)

        # Behavior
        beh_stmts = self.behavior_gen.generate(behavior_chains)

        # Threat Intel
        ti_stmts = self.threat_gen.generate(threat_matches)

        # Contradictions
        contr_narrs = self.contradiction_gen.generate(contradictions)

        # Mitigations
        mit_stmts = self.mitigation_gen.generate(mitigations)

        # Recommendations
        rec_stmts = self.recommendation_gen.generate(recommendations, band)

        # Summaries
        tech = self.tech_gen.generate(report_doc) if report_doc else f"Technical Summary — Risk Score: {score:.1f}/100 — Risk Band: {band}."
        user = self.user_gen.generate(report_doc) if report_doc else f"Risk score: {score:.1f}/100."
        analyst = self.analyst_gen.generate(report_doc, findings) if report_doc else f"Analyst Summary — Risk: {score:.1f}/100."

        # Collect all statements
        all_stmts: List[NarrativeStatementDTO] = []
        all_stmts.extend(df_stmts)
        all_stmts.extend(beh_stmts)
        all_stmts.extend(ti_stmts)
        all_stmts.extend(mit_stmts)
        all_stmts.extend(rec_stmts)

        # Lineage
        lineage: List[NarrativeLineageDTO] = []
        for stmt in all_stmts:
            lineage.append(NarrativeLineageDTO(
                statement_id=stmt.statement_id, report_id=report_id,
                section_id=stmt.statement_type.lower(), source_type=stmt.source_type,
                source_id=stmt.source_id, language=language,
            ))

        narrative_id = f"narr_{report_id}"
        now_str = datetime.now(timezone.utc).isoformat()

        return NarrativeDocumentDTO(
            narrative_id=narrative_id, report_id=report_id, analysis_id=analysis_id,
            language=language, executive_summary=exec_summary, risk_narrative=risk_narr,
            finding_narratives=finding_narrs, evidence_narratives=evidence_narrs,
            contradiction_narratives=contr_narrs, statements=all_stmts,
            lineage=lineage, technical_summary=tech, user_friendly_summary=user,
            analyst_summary=analyst, limitations=limitations, generated_at=now_str,
        )
