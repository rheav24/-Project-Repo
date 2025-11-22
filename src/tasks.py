"""Task implementations: Assignment, Exam, Project (inherit from AbstractTask)."""

from datetime import datetime
from typing import Tuple
from .abstract_task import AbstractTask


class Assignment(AbstractTask):
    """Concrete assignment class."""

    def __init__(self, title: str, due_date: str, course_code: str, weight: float,
                 assignment_type: str = "homework", status: str = "not_started",
                 estimated_hours: float = 2.0):
        super().__init__(title, due_date, course_code, weight)
        self.assignment_type = assignment_type
        self.status = status
        self.estimated_hours = float(estimated_hours)
        self.score = None

    def get_priority(self) -> str:
        if self.status == "completed":
            return "low"
        try:
            due = datetime.strptime(self.due_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
        days_until_due = (due.date() - datetime.now().date()).days

        if days_until_due < 0:
            return "critical"
        elif days_until_due <= 2 and self.weight >= 20:
            return "critical"
        elif days_until_due <= 5 or self.weight >= 30:
            return "high"
        elif days_until_due <= 10 or self.weight >= 15:
            return "medium"
        else:
            return "low"

    def calculate_time_remaining(self) -> Tuple[int, str]:
        try:
            due = datetime.strptime(self.due_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
        now = datetime.now()
        delta = due - now
        if delta.total_seconds() < 0:
            return (abs(delta.days), "overdue")
        elif delta.days > 0:
            return (delta.days, "days")
        else:
            hours = int(delta.total_seconds() / 3600)
            return (hours, "hours")


class Exam(Assignment):
    """Exam: specialized Assignment — lower thresholds for critical priority."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.assignment_type = "exam"

    def get_priority(self) -> str:
        if self.status == "completed":
            return "low"
        try:
            due = datetime.strptime(self.due_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
        days_until_due = (due.date() - datetime.now().date()).days

        # Exams are treated more critically earlier
        if days_until_due < 0:
            return "critical"
        elif days_until_due <= 4 or self.weight >= 20:
            return "critical"
        elif days_until_due <= 7 or self.weight >= 15:
            return "high"
        elif days_until_due <= 14:
            return "medium"
        else:
            return "low"


class Project(Assignment):
    """Project: long-running assignment with estimated hours considered."""

    def __init__(self, *args, estimated_hours: float = 10.0, **kwargs):
        super().__init__(*args, **kwargs)
        self.assignment_type = "project"
        self.estimated_hours = float(estimated_hours)

    def get_priority(self) -> str:
        base = super().get_priority()
        # If project takes a lot of time, bump priority earlier
        if base == "low" and self.estimated_hours >= 15:
            return "medium"
        return base
