"""Unit Tests — Response Playbooks, Selection & Immutability (Phase 4.0 Part 7 — Sections 27-30, 93).

Implements:
- Mandatory Test 13: Playbook changes after execution begins -> execution continues against original immutable version.
- Mandatory Test 25: Phishing incident -> PHISHING_RESPONSE candidate.
- Mandatory Test 26: Malware incident -> MALWARE_RESPONSE candidate.
- Mandatory Test 27: Voice scam incident -> VOICE_SCAM_RESPONSE candidate.
- Mandatory Test 28: Unknown incident -> generic investigation / None without fabricating specialized response.
"""

import pytest
from app.services.soc.response_playbook_engine import ResponsePlaybookEngine
from app.schemas.soc_operations_models import PlaybookStepDTO


class TestResponsePlaybookSelectionAndVersioning:
    def test_25_26_27_mandatory_playbook_selection(self):
        engine = ResponsePlaybookEngine()

        # 25. Phishing incident
        pb_phish = engine.select_playbook_for_incident("PHISHING_INCIDENT")
        assert pb_phish is not None
        assert pb_phish.playbook_id == "pbk_phishing"

        # 26. Malware incident
        pb_malware = engine.select_playbook_for_incident("MALWARE_INCIDENT")
        assert pb_malware is not None
        assert pb_malware.playbook_id == "pbk_malware"

        # 27. Voice scam incident
        pb_voice = engine.select_playbook_for_incident("VOICE_SCAM_INCIDENT")
        assert pb_voice is not None
        assert pb_voice.playbook_id == "pbk_voice_scam"

    def test_28_mandatory_unknown_incident_yields_none_without_fabrication(self):
        engine = ResponsePlaybookEngine()
        # Invariant: Unknown incident must not return a fabricated specialized playbook
        pb_unknown = engine.select_playbook_for_incident("UNKNOWN_INCIDENT")
        assert pb_unknown is None

    def test_13_mandatory_playbook_versioning_immutability(self):
        engine = ResponsePlaybookEngine()

        # Version 1 published
        v1_steps = [
            PlaybookStepDTO(
                playbook_id="pbk_test",
                step_number=1,
                name="Initial Step",
                description="Step 1",
                action_type="NOTIFY_ANALYST",
            )
        ]
        pb, v1 = engine.publish_playbook("pbk_test", "Test PB", "Desc", ["PHISHING_INCIDENT"], v1_steps)
        assert pb.current_version == 1
        assert v1.version_number == 1

        # Version 2 published
        v2_steps = v1_steps + [
            PlaybookStepDTO(
                playbook_id="pbk_test",
                step_number=2,
                name="Secondary Step",
                description="Step 2",
                action_type="BLOCK_DOMAIN",
            )
        ]
        pb_v2, v2 = engine.publish_playbook("pbk_test", "Test PB", "Desc", ["PHISHING_INCIDENT"], v2_steps)
        assert pb_v2.current_version == 2
        assert v2.version_number == 2

        # Invariant (Test 13): Historical execution referencing v1 gets v1 immutable snapshot
        v1_snapshot = engine.get_playbook_version("pbk_test", 1)
        assert v1_snapshot is not None
        assert len(v1_snapshot.steps) == 1
        assert len(v2.steps) == 2
