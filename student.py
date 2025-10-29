Student Class Module
INST326 - Project 2: OOP Class Implementation

Team: Class Tracker
Members: Kayla Fuentes, Rhea Vyragaram, Jocelyn DeHenzel, Vinindi Withanage

This module contains the Student class for managing student information.
Integrates functions from Project 1: validate_email, calculate_credits_total, 
filter_assignments_by_status
"""

from datetime import datetime, timedelta
from typing import List
import re


class Student:
    """
    Represents a student with courses, assignments, and academic tracking.
    
    This class serves as the central hub for managing a student's academic life,
    including course enrollment, assignment tracking, and academic progress.
    
    Attributes:
        name (str): Student's full name
        email (str): Student's email address
        student_id (str): Unique student identifier
        
    Example:
        >>> student = Student('John Doe', 'jdoe@umd.edu', 'UID123456')
        >>> from course import Course
        >>> course = Course('INST326', 'Dr. Smith', 3.0, 'TuTh 2:00-3:15')
        >>> student.enroll_course(course)
        >>> print(student.get_total_credits())
        3.0
        >>> assignments = student.get_assignments_by_status('in_progress')
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
        # Input validation
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        if not isinstance(student_id, str) or not student_id.strip():
            raise ValueError("Student ID must be a non-empty string")
        if not self._validate_email(email):
            raise ValueError("Invalid email format")
        
        # Private attributes with encapsulation
        self._name = name.strip()
        self._email = email.strip().lower()
        self._student_id = student_id.strip()
        self._courses = []
        self._assignments = []
        self._major = ""
        self._gpa = 0.0
    
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
            
        Raises:
            TypeError: If email is not a string
        """
        if not isinstance(email, str):
            raise TypeError("Email must be a string")
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
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
            
        Raises:
            ValueError: If not enrolled in the course
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
            
        Raises:
            TypeError: If credit_list is not a list or contains non-numeric values
            ValueError: If any credit value is negative
        """
        credit_list = [course.credits for course in self._courses]
        
        # Validation from Project 1 function
        if not isinstance(credit_list, list):
            raise TypeError("Credit list must be a list")
        for credit in credit_list:
            if not isinstance(credit, (int, float)):
                raise TypeError("All credits must be numeric")
            if credit < 0:
                raise ValueError("Credits cannot be negative")
        
        return sum(credit_list)
    
    def add_assignment(self, assignment):
        """
        Add an assignment to the student's list.
        
        Args:
            assignment: Assignment object to add
            
        Raises:
            TypeError: If not an Assignment object
        """
        # Avoid circular import - check type by duck typing
        if not hasattr(assignment, 'title') or not hasattr(assignment, 'due_date'):
            raise TypeError("Must provide a valid Assignment object")
        self._assignments.append(assignment)
    
    def get_assignments_by_status(self, status: str) -> List:
        """
        Get assignments filtered by status.
        Integrates filter_assignments_by_status from Project 1.
        
        Args:
            status (str): Status to filter by ('completed', 'in_progress', 'not_started')
            
        Returns:
            List: Filtered assignments
            
        Raises:
            TypeError: If assignments is not a list
            ValueError: If status is invalid
        """
        # Validation from Project 1 function
        valid_statuses = ['completed', 'in_progress', 'not_started']
        if status not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")
        
        return [a for a in self._assignments if a.status == status]
    
    def get_upcoming_assignments(self, days_ahead: int = 7) -> List:
        """
        Get assignments due within specified days.
        
        Args:
            days_ahead (int): Number of days to look ahead
            
        Returns:
            List: Upcoming assignments sorted by due date
            
        Raises:
            ValueError: If days_ahead is not positive
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
    
    def get_courses(self) -> List:
        """
        Get all enrolled courses.
        
        Returns:
            List: Copy of enrolled courses
        """
        return self._courses.copy()
    
    def get_assignments(self) -> List:
        """
        Get all assignments.
        
        Returns:
            List: Copy of all assignments
        """
        return self._assignments.copy()
    
    def get_course_by_code(self, course_code: str):
        """
        Get a specific course by course code.
        
        Args:
            course_code (str): Course code to find
            
        Returns:
            Course object if found, None otherwise
        """
        course_code = course_code.upper()
        for course in self._courses:
            if course.course_code == course_code:
                return course
        return None
    
    def __str__(self) -> str:
        """Return a readable string representation."""
        return f"{self._name} ({self._student_id}) - {len(self._courses)} courses, {self.get_total_credits()} credits"
    
    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return f"Student(name='{self._name}', email='{self._email}', student_id='{self._student_id}')"


if __name__ == "__main__":
    # Test the Student class
    print("=" * 60)
    print("Testing Student Class")
    print("=" * 60)
    
    # Create student
    student = Student('Alice Johnson', 'ajohnson@umd.edu', 'UID123456')
    print(f"\n1. Created student: {student}")
    print(f"   Repr: {repr(student)}")
    
    # Test email validation
    print("\n2. Email validation:")
    print(f"   Valid email (test@umd.edu): {student._validate_email('test@umd.edu')}")
    print(f"   Invalid email (invalid): {student._validate_email('invalid-email')}")
    
    # Test setting major and GPA
    print("\n3. Set major and GPA:")
    student.major = "Information Science"
    student.gpa = 3.75
    print(f"   Major: {student.major}")
    print(f"   GPA: {student.gpa}")
    
    # Test credit calculation with empty course list
    print("\n4. Total credits (no courses):")
    print(f"   Total credits: {student.get_total_credits()}")
    
    # Note: Full testing with Course and Assignment classes
    print("\n5. Testing with mock course data:")
    print("   (Full testing requires importing Course and Assignment classes)")
    
    # Test property access
    print("\n6. Test property access:")
    print(f"   Name: {student.name}")
    print(f"   Email: {student.email}")
    print(f"   Student ID: {student.student_id}")
    
    # Test email update
    print("\n7. Update email:")
    student.email = "alice.j@umd.edu"
    print(f"   New email: {student.email}")
    
    # Test error handling
    print("\n8. Test error handling:")
    try:
        invalid_student = Student("", "email@umd.edu", "UID789")
    except ValueError as e:
        print(f"   Caught expected error: {e}")
    
    try:
        student.email = "invalid-email"
    except ValueError as e:
        print(f"   Caught expected error: {e}")
    
    try:
        student.gpa = 5.0
    except ValueError as e:
        print(f"   Caught expected error: {e}")
    
    print("\n" + "=" * 60)
    print("All Student class tests passed!")
    print("=" * 60)
