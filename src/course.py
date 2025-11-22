"""Course class with composition: a Course has tasks and study groups."""

from typing import List
from .utils import format_course_code


class Course:
    """Represents a course. Composition: contains tasks and study groups."""

    def __init__(self, course_code: str, course_name: str = ""):
        if not isinstance(course_code, str) or not course_code.strip():
            raise ValueError("Course code must be a non-empty string")
        self._course_code = format_course_code(course_code)
        self._course_name = course_name.strip() if isinstance(course_name, str) else ""
        # composition relationships
        self._tasks: List = []  # list of AbstractTask instances
        self._study_groups: List = []  # list of StudyGroup instances
        self._students: List = []  # enrolled students (duck-typed)

    @property
    def course_code(self) -> str:
        return self._course_code

    @property
    def course_name(self) -> str:
        return self._course_name

    def add_task(self, task):
        """Add an AbstractTask (Assignment/Exam/Project) to this course."""
        # duck-type check
        if not hasattr(task, "title") or not hasattr(task, "due_date"):
            raise TypeError("Task must have title and due_date attributes")
        self._tasks.append(task)

    def get_tasks(self) -> List:
        return self._tasks.copy()

    def add_study_group(self, group):
        if not hasattr(group, "group_id"):
            raise TypeError("StudyGroup missing group_id")
        self._study_groups.append(group)

    def get_study_groups(self) -> List:
        return self._study_groups.copy()

    def enroll_student(self, student):
        if not hasattr(student, "student_id"):
            raise TypeError("Invalid student")
        # prevent duplicates
        for s in self._students:
            if s.student_id == student.student_id:
                raise ValueError("Student already enrolled")
        self._students.append(student)

    def drop_student(self, student_id: str):
        for i, s in enumerate(self._students):
            if s.student_id == student_id:
                self._students.pop(i)
                return
        raise ValueError("Student not found")

    def get_students(self):
        return self._students.copy()

    def __str__(self):
        return f"{self._course_code} - {self._course_name}"
