"""Student class that composes Schedule and holds tasks (AbstractTask instances)."""

from typing import List
from .utils import validate_email


class Student:
    """Represents a student; composition: student has assignments and schedule."""

    def __init__(self, name: str, email: str, student_id: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        if not isinstance(student_id, str) or not student_id.strip():
            raise ValueError("Student ID must be a non-empty string")
        if not validate_email(email):
            raise ValueError("Invalid email format")

        self.name = name.strip()
        self.email = email.strip().lower()
        self.student_id = student_id.strip()

        self._courses: List = []       # Course objects
        self._assignments: List = []   # AbstractTask objects
        self._major = ""
        self._gpa = 0.0

    def enroll_course(self, course):
        if not hasattr(course, "course_code"):
            raise TypeError("Must provide a valid Course object")
        # prevent duplicate enrollment
        for c in self._courses:
            if c.course_code == course.course_code:
                raise ValueError("Already enrolled")
        self._courses.append(course)
        # composition: link student into course as well
        try:
            course.enroll_student(self)
        except Exception:
            # if course doesn't support enroll_student, ignore (duck-typing tolerant)
            pass

    def add_assignment(self, assignment):
        if not hasattr(assignment, "title") or not hasattr(assignment, "due_date"):
            raise TypeError("Must provide a valid Assignment/Task object")
        self._assignments.append(assignment)

    def get_assignments(self) -> List:
        return self._assignments.copy()

    def get_assignments_by_status(self, status: str) -> List:
        valid = ["completed", "in_progress", "not_started"]
        if status not in valid:
            raise ValueError(f"Status must be one of {valid}")
        return [a for a in self._assignments if getattr(a, "status", None) == status]

    def get_total_credits(self) -> float:
        total = 0.0
        for c in self._courses:
            if not hasattr(c, "credits"):
                continue
            total += float(getattr(c, "credits", 0.0))
        return total

    def __str__(self):
        return f"{self.name} ({self.student_id}) - {len(self._courses)} courses"

    def __repr__(self):
        return f"Student(name='{self.name}', student_id='{self.student_id}', email='{self.email}')"
