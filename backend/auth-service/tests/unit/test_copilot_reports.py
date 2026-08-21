import pytest
from app.services.copilot.post_incident_review_copilot import PostIncidentReviewCopilot


def test_copilot_post_incident_report():
    pir = PostIncidentReviewCopilot()
    report = pir.generate_review("inc_2026_0042")

    assert report["incident_id"] == "inc_2026_0042"
    assert len(report["root_cause_analysis"]["5_whys"]) == 5
    assert len(report["lessons_learned"]) >= 1
