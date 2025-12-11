"""
Student Class Module - REFACTORED for Projects 3 & 4
INST326 - Project 3 & 4: Inheritance, Polymorphism, and System Integration

Team: Class Tracker
Members: Kayla Fuentes, Rhea Vyragaram, Jocelyn DeHenzel, Vinindi Withanage

Project 4 Additions:
- Student now composes an AcademicPlanner instance (_planner)
- Convenience methods to save/load planner state (data persistence)
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import List
import re

from academic_planner import AcademicPlanner  # NEW: explicit composition


class Student:
    """
    Represents a student with courses, assignments, and academic tracking.

    Uses composition:
        Student HAS-A AcademicPlanner to manage AcademicItem objects.
    """

    def __init__(self, name: str, email: str, student_id: str):
        """
        Initialize a Student object.

        Args:
            name (str): Student's full name
            email (str): Valid email address
            student_id (str): Unique student ID

        Raises:
            ValueError: If parameters are invalid
            TypeError: If arguments are not correct types
        """
        # Input validation (from Project 2)
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        if not isinstance(student_id, str) or not student_id.strip():
            raise ValueError("Student ID must be a non-empty string")
        if not self._validate_email(email):
            raise ValueError("Invalid email format")

        # Private attributes with encapsulation (from Project 2)
        self._name = name.strip()
        self._email = email.strip().lower()
        self._student_id = student_id.strip()
        self._courses = []
        self._assignments = []  # Kept for backward compatibility
        self._major = ""
        self._gpa = 0.0

        # NEW: composition with AcademicPlanner for Projects 3 & 4
        self._planner = AcademicPlanner(self._name)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------
    @property
    def name(self) -> str:
        """str: Get student name."""
        return self._name

    @property
    def email(self) -> str:
        """str: Get student email."""
        return self._email

    @email.setter
    def email(self, value: str):
        """Set email with validation."""
        if not self._validate_email(value):
            raise ValueError("Invalid email format")
        self._email = value.strip().lower()

    @property
    def student_id(self) -> str:
        """str: Get student ID (read-only)."""
        return self._student_id

    @property
    def major(self) -> str:
        """str: Get student major."""
        return self._major

    @major.setter
    def major(self, value: str):
        """Set student major."""
        self._major = value.strip()

    @property
    def gpa(self) -> float:
        """float: Get student GPA."""
        return self._gpa

    @gpa.setter
    def gpa(self, value: float):
        """Set GPA with validation."""
        if not isinstance(value, (int, float)) or not 0.0 <= value <= 4.0:
            raise ValueError("GPA must be between 0.0 and 4.0")
        self._gpa = float(value)

    @property
    def planner(self) -> AcademicPlanner:
        """
        AcademicPlanner: read-only access to the student's planner.

        This exposes the composition relationship:
            Student HAS-A AcademicPlanner.
        """
        return self._planner

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _validate_email(self, email: str) -> bool:
        """
        Validate email format.
        Integrates validate_email from Project 1.

        Args:
            email (str): Email to validate

        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(email, str):
            raise TypeError("Email must be a string")
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    # ------------------------------------------------------------------
    # Course management (unchanged from Project 2)
    # ------------------------------------------------------------------
    def enroll_course(self, course):
        """
        Enroll in a course.

        Args:
            course: Course object to enroll in

        Raises:
            TypeError: If course is not a Course object
            ValueError: If already enrolled in the course
        """
        # Avoid circular import - check type by duck typing
        if not hasattr(course, 'course_code') or not hasattr(course, 'credits'):
            raise TypeError("Must provide a valid Course object")

        # Check if already enrolled
        for enrolled in self._courses:
            if enrolled.course_code == course.course_code:
                raise ValueError(f"Already enrolled in {course.course_code}")

        self._courses.append(course)

    def drop_course(self, course_code: str):
        """
        Drop a course by course code.

        Args:
            course_code (str): Course code to drop
        """
        course_code = course_code.upper()
        for i, course in enumerate(self._courses):
            if course.course_code == course_code:
                self._courses.pop(i)
                # Remove associated assignments
                self._assignments = [
                    a for a in self._assignments if a.course_code != course_code
                ]
                return

        raise ValueError(f"Not enrolled in {course_code}")

    def get_total_credits(self) -> float:
        """
        Calculate total enrolled credits.
        Integrates calculate_credits_total from Project 1.

        Returns:
            float: Total credit hours
        """
        credit_list = [course.credits for course in self._courses]

        if not isinstance(credit_list, list):
            raise TypeError("Credit list must be a list")
        for credit in credit_list:
            if not isinstance(credit, (int, float)):
                raise TypeError("All credits must be numeric")
            if credit < 0:
                raise ValueError("Credits cannot be negative")

        return sum(credit_list)

    # ------------------------------------------------------------------
    # Assignment / AcademicItem handling (polymorphic)
    # ------------------------------------------------------------------
    def add_assignment(self, assignment):
        """
        Add an assignment to the student's list.

        ENHANCED: Now accepts any AcademicItem subclass (Assignment, Project, Exam).
        Also mirrors items into the student's AcademicPlanner for end-to-end workflows.

        Args:
            assignment: AcademicItem object to add (Assignment, Project, or Exam)

        Raises:
            TypeError: If not an AcademicItem-like object
        """
        # Polymorphic duck-typing
        if not hasattr(assignment, 'title') or not hasattr(assignment, 'due_date'):
            raise TypeError("Must provide a valid AcademicItem object")
        if not hasattr(assignment, 'get_priority'):
            raise TypeError("Must provide a valid AcademicItem object")

        self._assignments.append(assignment)
        # NEW: keep planner in sync (system integration)
        self._planner.add_item(assignment)

    def get_assignments_by_status(self, status: str) -> List:
        """
        Get assignments filtered by status.
        Integrates filter_assignments_by_status from Project 1.

        ENHANCED: Works polymorphically with Assignment, Project, and Exam objects.

        Args:
            status (str): Status to filter by

        Returns:
            List: Filtered assignments
        """
        valid_statuses = ['completed', 'in_progress', 'not_started']
        if status not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")

        return [a for a in self._assignments if a.status == status]

    def get_upcoming_assignments(self, days_ahead: int = 7) -> List:
        """
        Get assignments due within specified days.

        ENHANCED: Works polymorphically with all AcademicItem types.

        Args:
            days_ahead (int): Number of days to look ahead

        Returns:
            List: Upcoming assignments sorted by due date
        """
        if not isinstance(days_ahead, int) or days_ahead <= 0:
            raise ValueError("Days ahead must be a positive integer")

        upcoming = []
        today = datetime.now().date()
        cutoff = today + timedelta(days=days_ahead)

        for assignment in self._assignments:
            if assignment.status != 'completed':
                due = datetime.strptime(assignment.due_date, '%Y-%m-%d').date()
                if today <= due <= cutoff:
                    upcoming.append(assignment)

        upcoming.sort(key=lambda a: a.due_date)
        return upcoming

    def get_total_workload(self) -> float:
        """
        Calculate total workload across all incomplete assignments.

        Delegates to the planner so behavior stays consistent.
        """
        return self._planner.get_total_workload()

    def get_assignments_by_priority(self, priority: str) -> List:
        """
        Get all assignments with specified priority.

        Delegates to the planner's polymorphic priority logic.
        """
        return self._planner.get_items_by_priority(priority)

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------
    def get_courses(self) -> List:
        """Get all enrolled courses."""
        return self._courses.copy()

    def get_assignments(self) -> List:
        """
        Get all assignments.

        ENHANCED: Now returns all AcademicItem types (Assignment, Project, Exam).
        """
        return self._assignments.copy()

    def get_course_by_code(self, course_code: str):
        """Get a specific course by course code."""
        course_code = course_code.upper()
        for course in self._courses:
            if course.course_code == course_code:
                return course
        return None

    # ------------------------------------------------------------------
    # Project 4: persistence helpers delegating to planner
    # ------------------------------------------------------------------
    def save_planner(self, path: str | Path) -> None:
        """
        Save the student's planner state to JSON.

        This is a thin wrapper around AcademicPlanner.save_to_json().
        """
        self._planner.save_to_json(path)

    def load_planner(self, path: str | Path) -> None:
        """
        Load the student's planner state from JSON.

        This replaces the planner's current items with those from the file.
        """
        self._planner.load_from_json(path)

    # ------------------------------------------------------------------
    # String representations
    # ------------------------------------------------------------------
    def __str__(self) -> str:
        """Return a readable string representation."""
        return (
            f"{self._name} ({self._student_id}) - "
            f"{len(self._courses)} courses, {self.get_total_credits()} credits, "
            f"{len(self._planner.get_all_items())} planner items"
        )

    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return (
            f"Student(name='{self._name}', email='{self._email}', "
            f"student_id='{self._student_id}')"
        )


if __name__ == "__main__":
    # Quick sanity check
    print("=" * 60)
    print("Testing Refactored Student Class (Project 4)")
    print("=" * 60)

    student = Student('Alice Johnson', 'ajohnson@umd.edu', 'UID123456')
    print(f"Created student: {student}")
    print(f"Planner: {student.planner}")
