"""Unit Tests — Case Notes, Bookmarks & Tasks (Phase 4.0 Part 4 — Sections 34-37, 50, 83)."""

import pytest
from app.schemas.investigation_models import CaseNoteDTO, CaseBookmarkDTO, CaseTaskDTO


class TestCaseArtifacts:
    def test_case_note_types_distinction(self):
        valid_note_types = [
            "OBSERVATION",
            "HYPOTHESIS",
            "FOLLOW_UP",
            "INVESTIGATION",
            "FALSE_POSITIVE_REVIEW",
            "ESCALATION",
            "GENERAL",
        ]
        note = CaseNoteDTO(
            note_id="note_01",
            case_id="case_101",
            author_id="usr_analyst",
            note_type="HYPOTHESIS",
            content="Likely C2 server communication pattern",
        )
        assert note.note_type in valid_note_types
        assert note.note_type != "CONFIRMED_FACT"

    def test_case_bookmark_dto(self):
        bm = CaseBookmarkDTO(
            bookmark_id="bm_01",
            case_id="case_101",
            user_id="usr_analyst",
            item_type="FINDING",
            item_id="F_01",
            label="Key Cryptographic Failure",
        )
        assert bm.bookmark_id == "bm_01"
        assert bm.item_type == "FINDING"

    def test_case_task_dto(self):
        task = CaseTaskDTO(
            task_id="task_01",
            case_id="case_101",
            title="Inspect Domain Registration",
            priority="HIGH",
            status="IN_PROGRESS",
        )
        assert task.task_id == "task_01"
        assert task.status == "IN_PROGRESS"
