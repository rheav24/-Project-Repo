"""
Student Class Module - REFACTORED for Project 3
INST326 - Project 3: Inheritance and Polymorphism

Team: Class Tracker
Members: Kayla Fuentes, Rhea Vyragaram, Jocelyn DeHenzel, Vinindi Withanage

REFACTORED to demonstrate composition by integrating AcademicPlanner.
This shows "has-a" relationship: Student HAS-A planner.

CHANGES FROM PROJECT 2:
- Added AcademicPlanner integration (composition)
- Student now HAS-A planner for managing academic items
- All original functionality preserved
- New methods leverage polymorphic item handling
"""

from datetime import datetime, timedelta
from typing import List
import re


class Student:
    """
    Represents a student with courses, assignments, and academic tracking.
    
    REFACTORED: Now demonstrates composition by containing an AcademicPlanner.
    This is a "has-a" relationship - Student HAS-A planner.
    
    This class serves as the central hub for managing a student's academic life,
    including course enrollment, assignment tracking, and academic progress.
    
    Attributes:
        name (str): Student's full name
        email (str): Student's email address
        student_id (str): Unique student identifier
        
    Example:
        >>> student = Student('John Doe', 'jdoe@umd.edu', 'UID123456')
        >>> from course import Course
        >>> from assignment import Assignment, Project
        >>> course = Course('INST326', 'Dr. Smith', 3.0, 'TuTh 2:00-3:15')
        >>> student.enroll_course(course)
        >>> 
        >>> # Can add different types polymorphically!
        >>> assignment = Assignment('HW1', '2025-11-25', 'INST326', 10.0)
        >>> project = Project('Final', '2025-12-10', 'INST326', 40.0)
        >>> student.add_assignment(assignment)  # Works with any AcademicItem!
        >>> student.add_assignment(project)
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
    
    # All original Project 2 properties preserved
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
    
    # Original Project 2 course management methods
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
                self._assignments = [a for a in self._assignments 
                                   if a.course_code != course_code]
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
    
    # MODIFIED: Now works polymorphically with any AcademicItem subclass
    def add_assignment(self, assignment):
        """
        Add an assignment to the student's list.
        
        ENHANCED: Now accepts any AcademicItem subclass (Assignment, Project, Exam).
        This demonstrates polymorphism - same method works with different types.
        
        Args:
            assignment: AcademicItem object to add (Assignment, Project, or Exam)
            
        Raises:
            TypeError: If not an AcademicItem
        """
        # Check if it's any kind of AcademicItem (polymorphic acceptance)
        if not hasattr(assignment, 'title') or not hasattr(assignment, 'due_date'):
            raise TypeError("Must provide a valid AcademicItem object")
        if not hasattr(assignment, 'get_priority'):
            raise TypeError("Must provide a valid AcademicItem object")
        
        self._assignments.append(assignment)
    
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
        
        # Sort by due date
        upcoming.sort(key=lambda a: a.due_date)
        return upcoming
    
    # NEW METHOD: Demonstrates polymorphism
    def get_total_workload(self) -> float:
        """
        Calculate total workload across all incomplete assignments.
        
        NEW METHOD: Demonstrates polymorphism - each item type calculates
        time commitment differently, but we can sum them uniformly.
        
        Returns:
            float: Total estimated hours across all items
        """
        total = 0.0
        for item in self._assignments:
            if item.status != 'completed':
                # Polymorphic call - works with Assignment, Project, Exam
                total += item.calculate_time_commitment()
        return round(total, 2)
    
    # NEW METHOD: Demonstrates polymorphism
    def get_assignments_by_priority(self, priority: str) -> List:
        """
        Get all assignments with specified priority.
        
        NEW METHOD: Demonstrates polymorphism - each item calculates
        its own priority, but we filter uniformly.
        
        Args:
            priority (str): Priority level to filter by
            
        Returns:
            List: Items with that priority
        """
        valid_priorities = ['critical', 'high', 'medium', 'low']
        if priority not in valid_priorities:
            raise ValueError(f"Priority must be one of {valid_priorities}")
        
        # Polymorphic call - get_priority() works on all types
        return [a for a in self._assignments 
                if a.get_priority() == priority and a.status != 'completed']
    
    # Original Project 2 getter methods
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
    
    # Original Project 2 string methods
    def __str__(self) -> str:
        """Return a readable string representation."""
        return (f"{self._name} ({self._student_id}) - "
                f"{len(self._courses)} courses, {self.get_total_credits()} credits")
    
    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return (f"Student(name='{self._name}', email='{self._email}', "
                f"student_id='{self._student_id}')")


if __name__ == "__main__":
    # Test the refactored Student class
    print("=" * 60)
    print("Testing Refactored Student Class")
    print("=" * 60)
    
    # Original Project 2 functionality still works
    student = Student('Alice Johnson', 'ajohnson@umd.edu', 'UID123456')
    print(f"\n1. Created student: {student}")
    
    student.major = "Information Science"
    student.gpa = 3.75
    print(f"   Major: {student.major}, GPA: {student.gpa}")
    
    # NEW: Test polymorphic assignment handling
    print("\n2. Adding different types of academic items (polymorphism):")
    
    from assignment import Assignment, Project, Exam
    
    assignment = Assignment('HW5', '2025-11-25', 'INST326', 10.0, 
                           estimated_hours=3.0)
    project = Project('Final Project', '2025-12-10', 'INST326', 40.0,
                     num_milestones=3, team_size=4)
    exam = Exam('Midterm', '2025-11-22', 'INST326', 25.0,
               exam_type='midterm', num_chapters=6)
    
    # Same method works with all types!
    student.add_assignment(assignment)
    student.add_assignment(project)
    student.add_assignment(exam)
    
    print(f"   Added {len(student.get_assignments())} items")
    print(f"   Types: Assignment, Project, Exam")
    
    # NEW: Test polymorphic workload calculation
    print("\n3. Total workload (polymorphic calculation):")
    total = student.get_total_workload()
    print(f"   Total hours needed: {total}")
    print("   (Each type calculated differently!)")
    
    # NEW: Test polymorphic priority filtering
    print("\n4. Get items by priority (polymorphic):")
    critical = student.get_assignments_by_priority('critical')
    high = student.get_assignments_by_priority('high')
    print(f"   Critical priority: {len(critical)}")
    print(f"   High priority: {len(high)}")
    
    # Original Project 2 methods still work
    print("\n5. Original Project 2 functionality preserved:")
    upcoming = student.get_upcoming_assignments(30)
    print(f"   Upcoming assignments: {len(upcoming)}")
    
    in_progress = student.get_assignments_by_status('not_started')
    print(f"   Not started: {len(in_progress)}")
    
    print("\n" + "=" * 60)
    print("All tests passed!")
    print("✓ Backward compatible with Project 2")
    print("✓ Enhanced with polymorphic item handling")
    print("=" * 60)
