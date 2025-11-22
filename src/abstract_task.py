"""AbstractTask: abstract base class for tasks/assignments/exams/projects."""

from abc import ABC, abstractmethod
from typing import Tuple


class AbstractTask(ABC):
    """Abstract base for course tasks.

    Subclasses must implement:
      - get_priority() -> str
      - calculate_time_remaining() -> Tuple[int, str]
    """

    def __init__(self, title: str, due_date: str, course_code: str, weight: float):
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Title must be a non-empty string")
        if not isinstance(due_date, str) or not due_date.strip():
            raise ValueError("Due date must be a non-empty 'YYYY-MM-DD' string")
        if not isinstance(course_code, str) or not course_code.strip():
            raise ValueError("Course code must be a non-empty string")
        if not isinstance(weight, (int, float)) or weight < 0:
            raise ValueError("Weight must be a non-negative number")

        self.title = title.strip()
        self.due_date = due_date.strip()
        self.course_code = course_code.strip().upper()
        self.weight = float(weight)

    @abstractmethod
    def get_priority(self) -> str:
        """Return priority: 'critical'|'high'|'medium'|'low'."""
        raise NotImplementedError

    @abstractmethod
    def calculate_time_remaining(self) -> Tuple[int, str]:
        """Return tuple (number, unit) where unit is 'days','hours','overdue'."""
        raise NotImplementedError
