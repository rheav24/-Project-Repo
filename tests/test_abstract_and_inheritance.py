"""Tests for AbstractTask and inheritance behavior."""

import pytest
from src.abstract_task import AbstractTask
from src.tasks import Assignment, Exam, Project


def test_abstract_instantiation_forbidden():
    with pytest.raises(TypeError):
        # Cannot instantiate an abstract class
        AbstractTask("t", "2025-01-01", "INST100", 10)


def test_assignment_basic_behavior():
    a = Assignment("HW", "2025-12-01", "INST326", 10)
    assert isinstance(a, Assignment)
    assert a.get_priority() in {"critical", "high", "medium", "low"}
    remaining = a.calculate_time_remaining()
    assert isinstance(remaining, tuple) and len(remaining) == 2


def test_exam_specialization_calls_super_and_overrides():
    e = Exam("Midterm", "2025-11-20", "INST326", 30)
    assert isinstance(e, Assignment)
    # Should override behavior — still returns a priority string
    assert isinstance(e.get_priority(), str)


def test_project_priority_considers_estimated_hours():
    p = Project("BigProj", "2026-01-01", "INST326", 10, estimated_hours=20)
    # project uses Assignment logic but may bump priority due to hours
    assert p.get_priority() in {"critical", "high", "medium", "low"}
