"""Tests that polymorphism works: same method called on mixed types."""

from src.tasks import Assignment, Exam, Project


def test_polymorphic_priority_calls():
    tasks = [
        Assignment("A", "2025-12-01", "INST326", 5),
        Exam("E", "2025-11-20", "INST326", 30),
        Project("P", "2025-12-15", "INST326", 40, estimated_hours=20)
    ]
    priorities = [t.get_priority() for t in tasks]
    assert len(priorities) == 3
    # ensure we can iterate and call same method polymorphically
    assert all(isinstance(p, str) for p in priorities)
