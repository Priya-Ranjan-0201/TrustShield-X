import pytest
from app.services.copilot.executive_intelligence_copilot import ExecutiveIntelligenceCopilot


def test_copilot_executive_briefing():
    exec_copilot = ExecutiveIntelligenceCopilot()
    brief = exec_copilot.generate_daily_brief("tenant_alpha")

    assert brief.brief_type == "DAILY_BRIEF"
    assert "99.98%" in brief.business_impact
    assert brief.financial_impact == "FINANCIAL IMPACT UNKNOWN"
    assert len(brief.top_risks) >= 1
