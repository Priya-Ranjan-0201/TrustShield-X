import pytest
from app.services.copilot.threat_hunting_copilot import ThreatHuntingCopilot


def test_copilot_tool_injection_sql_drop_table():
    hunter = ThreatHuntingCopilot()

    # Tool execution query injection
    assert hunter.validate_query("SELECT * FROM logs; DROP TABLE users;") is False
    assert hunter.validate_query("UPDATE users SET is_admin=1;") is False
