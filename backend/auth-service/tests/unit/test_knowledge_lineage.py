import pytest
from app.services.knowledge_fabric.knowledge_lineage_engine import KnowledgeLineageEngine


def test_knowledge_lineage_traceability():
    engine = KnowledgeLineageEngine()

    lineage = engine.record_lineage(
        conclusion_id="conc_rce_exploit",
        created_by_model="SecurityReasoningEngine_v2",
        source_data=["raw_pcap_dump", "vuln_db_export"],
        supporting_evidence=["ev_pcap_trace_88"],
        transformations=["PACKET_DECODE", "IOC_MATCH"],
        models_used=["SNORT_SIGNATURE_PARSER", "MITRE_ATTACK_MAPPER"],
        dependent_conclusions=["conc_campaign_attribution"],
    )

    assert lineage.conclusion_id == "conc_rce_exploit"
    assert "PACKET_DECODE" in lineage.transformations
    assert len(lineage.supporting_evidence) == 1
