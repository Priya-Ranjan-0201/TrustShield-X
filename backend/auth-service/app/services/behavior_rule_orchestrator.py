"""Behavior Rule Orchestrator (Phase 3.9 Part 1A.24).

Orchestrates loading analysis snapshots, executing behavior rules against active rule packs,
generating execution traces, summaries, cards, and multi-format exports.
"""

import csv
import io
import json
import time
from typing import List, Dict, Any, Optional
from app.schemas.behavior_rule_models import (
    BehaviorRuleDTO,
    BehaviorRulePackDTO,
    BehaviorRuleEvaluationDTO,
    RuleExecutionTraceDTO,
    RuleEvidenceDTO,
    RuleSuppressionDTO,
    RuleExceptionDTO,
    RuleConflictDTO,
    RuleSummaryDTO,
    RuleCardDTO,
    RuleGraphDTO,
    RuleMetricsDTO,
    RuleResultDTO,
)
from app.services.rule_registry import RuleRegistry
from app.services.rule_validator import RuleValidator
from app.services.behavior_rule_engine import BehaviorRuleEngine


class BehaviorRuleOrchestrator:
    """Orchestrates Behavior Rule Engine execution."""

    def __init__(self):
        self.registry = RuleRegistry()
        self.validator = RuleValidator()
        self.engine = BehaviorRuleEngine()

    def run_rule_evaluation(
        self,
        manifest_intelligence_dto: Any = None,
        permission_intelligence_dto: Any = None,
        api_intelligence_dto: Any = None,
        network_intelligence_dto: Any = None,
        cryptography_intelligence_dto: Any = None,
        storage_intelligence_dto: Any = None,
        dataflow_intelligence_dto: Any = None,
        behavioral_correlation_dto: Any = None,
        threat_intelligence_dto: Any = None,
    ) -> RuleResultDTO:
        start_time = time.time()

        context = {
            "MANIFEST_INTELLIGENCE": manifest_intelligence_dto,
            "PERMISSION_INTELLIGENCE": permission_intelligence_dto,
            "API_INTELLIGENCE": api_intelligence_dto,
            "NETWORK_INTELLIGENCE": network_intelligence_dto,
            "CRYPTOGRAPHY_INTELLIGENCE": cryptography_intelligence_dto,
            "STORAGE_INTELLIGENCE": storage_intelligence_dto,
            "DATAFLOW_INTELLIGENCE": dataflow_intelligence_dto,
            "BEHAVIORAL_CORRELATION": behavioral_correlation_dto,
            "THREAT_INTELLIGENCE": threat_intelligence_dto,
        }

        active_rules = self.registry.list_active_rules()
        pack = self.registry.get_rule_pack()

        evaluations: List[BehaviorRuleEvaluationDTO] = []
        traces: List[RuleExecutionTraceDTO] = []
        evidence_list: List[RuleEvidenceDTO] = []
        suppressions: List[RuleSuppressionDTO] = []
        exceptions: List[RuleExceptionDTO] = []
        conflicts: List[RuleConflictDTO] = []
        summaries: List[RuleSummaryDTO] = []
        cards: List[RuleCardDTO] = []

        matched_count = 0
        partially_count = 0
        not_evaluable_count = 0

        for r in active_rules:
            e_dto, t_dto, ev_list = self.engine.evaluate_rule(r, context)
            evaluations.append(e_dto)
            traces.append(t_dto)
            evidence_list.extend(ev_list)

            if e_dto.state == "MATCHED":
                matched_count += 1
            elif e_dto.state == "PARTIALLY_MATCHED":
                partially_count += 1
            elif e_dto.state == "NOT_EVALUABLE":
                not_evaluable_count += 1

            cards.append(
                RuleCardDTO(
                    card_id=f"card_{r.rule_id}",
                    title=r.name,
                    rule_id=r.rule_id,
                    state=e_dto.state,
                    confidence=e_dto.confidence,
                )
            )

        summaries.append(
            RuleSummaryDTO(
                title="Behavior Rule Evaluation Summary",
                summary_text=f"Evaluated {len(active_rules)} security behavior rules ({matched_count} matched, {partially_count} partially matched, {not_evaluable_count} not evaluable).",
                matched_count=matched_count,
            )
        )

        metrics = RuleMetricsDTO(
            rules_loaded=len(active_rules),
            rules_evaluated=len(active_rules),
            rules_matched=matched_count,
            rules_partially_matched=partially_count,
            rules_not_evaluable=not_evaluable_count,
            rules_suppressed=len(suppressions),
            rules_conflicted=len(conflicts),
        )

        r_graph = RuleGraphDTO(
            nodes_count=len(active_rules) + len(evaluations),
            edges_count=len(evidence_list),
        )

        # Multi-format Exporters (JSON, CSV, GraphML, DOT, Mermaid)
        json_exp = json.dumps([e.model_dump() for e in evaluations], indent=2)

        csv_buf = io.StringIO()
        writer = csv.writer(csv_buf)
        writer.writerow(["Evaluation ID", "Rule ID", "Version", "Namespace", "State", "Confidence"])
        for e in evaluations:
            writer.writerow([e.evaluation_id, e.rule_id, e.rule_version, e.namespace, e.state, e.confidence])
        csv_exp = csv_buf.getvalue()

        dot_exp = "digraph BehaviorRuleGraph {\n"
        mermaid_exp = "graph TD\n"
        graphml_exp = '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">\n  <graph id="G" edgedefault="directed">\n'

        for e in evaluations[:50]:
            dot_exp += f'  "{e.evaluation_id}" -> "{e.rule_id}" [label="{e.state}"];\n'
            mermaid_exp += f'  "{e.evaluation_id}" -->|{e.state}| "{e.rule_id}"\n'
            graphml_exp += f'    <edge source="{e.evaluation_id}" target="{e.rule_id}"/>\n'

        dot_exp += "}"
        graphml_exp += "  </graph>\n</graphml>"

        analysis_time_ms = int((time.time() - start_time) * 1000)

        return RuleResultDTO(
            evaluations=evaluations[:500],
            traces=traces[:500],
            evidence=evidence_list[:500],
            suppressions=suppressions[:100],
            exceptions=exceptions[:100],
            conflicts=conflicts[:100],
            rules=active_rules[:100],
            packs=[pack],
            summaries=summaries[:100],
            cards=cards[:500],
            rule_graph=r_graph,
            metrics=metrics,
            json_export=json_exp,
            csv_export=csv_exp,
            graphml_export=graphml_exp,
            dot_export=dot_exp,
            mermaid_export=mermaid_exp,
            analysis_time_ms=analysis_time_ms,
        )
