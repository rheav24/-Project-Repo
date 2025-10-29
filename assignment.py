"""
Assignment Class Module
INST326 - Project 2: OOP Class Implementation

Team: Class Tracker
Members: Kayla Fuentes, Rhea Vyragaram, Jocelyn DeHenzel, Vinindi Withanage

This module contains the Assignment class for managing course assignments.
Integrates functions from Project 1: is_assignment_overdue, calculate_assignment_priority, 
calculate_time_until_due
"""

from datetime import datetime
from typing import Optional, Tuple


class Assignment:
    """
    Represents a course assignment with due date, priority, and completion tracking.
    
    This class manages individual assignments, calculates priorities and time
    remaining, and tracks completion status and scores.
    
    Attributes:
        title (str): Assignment title
        due_date (str): Due date in 'YYYY-MM-DD' format
        course_code (str): Associated course code
        weight (float): Assignment weight/percentage (0-100)
        assignment_type (str): Type of assignment
        status (str): Completion status
        
    Example:
        >>> assignment = Assignment('Project 1', '2025-11-15', 'INST326', 
        ...                         25.0, 'project', 'not_started')
        >>> print(assignment.get_priority())
        'high'
        >>> time_left = assignment.calculate_time_remaining()
        >>> assignment.mark_completed(95.0)
        >>> print(assignment.is_completed())
        True
    """
    
    def __init__(self, title: str, due_date: str, course_code: str,
                 weight: float, assignment_type: str = 'homework',
                 status: str = 'not_started', estimated_hours: float = 2.0):
        """
        Initialize an Assignment object.
        
        Args:
            title (str): Assignment title
            due_date (str): Due date in 'YYYY-MM-DD' format
            course_code (str): Course identifier
            weight (float): Weight/percentage (0-100)
            assignment_type (str, optional): Type (homework, project, exam, quiz, etc.)
            status (str, optional): Initial status (not_started, in_progress, completed)
            estimated_hours (float, optional): Estimated completion time
            
        Raises:
            ValueError: If parameters are invalid
            TypeError: If arguments are not correct types
        """
        # Input validation
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Title must be a non-empty string")
        if not isinstance(course_code, str) or not course_code.strip():
            raise ValueError("Course code must be a non-empty string")
        if not isinstance(weight, (int, float)) or not 0 <= weight <= 100:
            raise ValueError("Weight must be between 0 and 100")
        if status not in ['not_started', 'in_progress', 'completed']:
            raise ValueError("Status must be 'not_started', 'in_progress', or 'completed'")
        if not isinstance(estimated_hours, (int, float)) or estimated_hours < 0:
            raise ValueError("Estimated hours must be a non-negative number")
        
        # Validate date format
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Due date must be in YYYY-MM-DD format")
        
        # Private attributes with encapsulation
        self._title = title.strip()
        self._due_date = due_date
        self._course_code = course_code.upper()
        self._weight = float(weight)
        self._assignment_type = assignment_type.lower()
        self._status = status
        self._estimated_hours = float(estimated_hours)
        self._score = None
        self._submission_date = None
        self._notes = ""
        self._instructions = ""
    
    @property
    def title(self) -> str:
        """str: Get assignment title."""
        return self._title
    
    @property
    def due_date(self) -> str:
        """str: Get due date."""
        return self._due_date
    
    @property
    def course_code(self) -> str:
        """str: Get course code (read-only)."""
        return self._course_code
    
    @property
    def weight(self) -> float:
        """float: Get assignment weight."""
        return self._weight
    
    @property
    def assignment_type(self) -> str:
        """str: Get assignment type."""
        return self._assignment_type
    
    @property
    def status(self) -> str:
        """str: Get completion status."""
        return self._status
    
    @status.setter
    def status(self, value: str):
        """Set status with validation."""
        valid_statuses = ['not_started', 'in_progress', 'completed']
        if value not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")
        self._status = value
    
    @property
    def score(self) -> Optional[float]:
        """Optional[float]: Get assignment score if completed."""
        return self._score
    
    @property
    def estimated_hours(self) -> float:
        """float: Get estimated hours."""
        return self._estimated_hours
    
    def is_overdue(self, current_date: str = None) -> bool:
        """
        Check if assignment is overdue.
        Integrates is_assignment_overdue from Project 1.
        
        Args:
            current_date (str, optional): Current date in 'YYYY-MM-DD' format.
                                         Defaults to today.
        
        Returns:
            bool: True if overdue, False otherwise
            
        Raises:
            ValueError: If date format is invalid
        """
        try:
            due = datetime.strptime(self._due_date, '%Y-%m-%d')
            current = datetime.strptime(current_date, '%Y-%m-%d') if current_date else datetime.now()
            return current.date() > due.date()
        except ValueError as e:
            raise ValueError(f"Invalid date format. Use YYYY-MM-DD: {e}")
    
    def get_priority(self) -> str:
        """
        Calculate priority level for this assignment.
        Integrates calculate_assignment_priority from Project 1.
        
        Returns:
            str: Priority level ('critical', 'high', 'medium', 'low')
        """
        if self._status == 'completed':
            return 'low'
        
        try:
            due = datetime.strptime(self._due_date, '%Y-%m-%d')
            days_until_due = (due.date() - datetime.now().date()).days
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
        
        if days_until_due < 0:
            return 'critical'
        elif days_until_due <= 2 and self._weight >= 20:
            return 'critical'
        elif days_until_due <= 5 or self._weight >= 30:
            return 'high'
        elif days_until_due <= 10 or self._weight >= 15:
            return 'medium'
        else:
            return 'low'
    
    def calculate_time_remaining(self) -> Tuple[int, str]:
        """
        Calculate time remaining until due date.
        Integrates calculate_time_until_due from Project 1.
        
        Returns:
            Tuple[int, str]: (number, unit) where unit is 'days', 'hours', or 'overdue'
        """
        try:
            due = datetime.strptime(self._due_date, '%Y-%m-%d')
            now = datetime.now()
            delta = due - now
            
            if delta.total_seconds() < 0:
                days_overdue = abs(delta.days)
                return (days_overdue, 'overdue')
            elif delta.days > 0:
                return (delta.days, 'days')
            else:
                hours = int(delta.total_seconds() / 3600)
                return (hours, 'hours')
        except ValueError as e:
            raise ValueError(f"Invalid date format. Use YYYY-MM-DD: {e}")
    
    def mark_completed(self, score: float, submission_date: str = None):
        """
        Mark assignment as completed with a score.
        
        Args:
            score (float): Score earned (0-100)
            submission_date (str, optional): Submission date in 'YYYY-MM-DD' format.
                                            Defaults to today.
            
        Raises:
            ValueError: If score is invalid or date format is wrong
        """
        if not isinstance(score, (int, float)) or not 0 <= score <= 100:
            raise ValueError("Score must be between 0 and 100")
        
        self._status = 'completed'
        self._score = float(score)
        
        if submission_date:
            try:
                datetime.strptime(submission_date, '%Y-%m-%d')
                self._submission_date = submission_date
            except ValueError:
                raise ValueError("Submission date must be in YYYY-MM-DD format")
        else:
            self._submission_date = datetime.now().strftime('%Y-%m-%d')
    
    def is_completed(self) -> bool:
        """
        Check if assignment is completed.
        
        Returns:
            bool: True if completed, False otherwise
        """
        return self._status == 'completed'
    
    def add_notes(self, notes: str):
        """
        Add or update notes for the assignment.
        
        Args:
            notes (str): Notes to add
        """
        self._notes = notes.strip()
    
    def get_notes(self) -> str:
        """
        Get assignment notes.
        
        Returns:
            str: Current notes
        """
        return self._notes
    
    def set_instructions(self, instructions: str):
        """
        Set assignment instructions.
        
        Args:
            instructions (str): Assignment instructions or description
        """
        self._instructions = instructions.strip()
    
    def get_instructions(self) -> str:
        """
        Get assignment instructions.
        
        Returns:
            str: Assignment instructions
        """
        return self._instructions
    
    def __str__(self) -> str:
        """Return a readable string representation."""
        time_info = self.calculate_time_remaining()
        if time_info[1] == 'overdue':
            time_str = f"OVERDUE by {time_info[0]} days"
        else:
            time_str = f"Due in {time_info[0]} {time_info[1]}"
        
        return f"{self._title} [{self._course_code}] - {time_str} (Priority: {self.get_priority()})"
    
    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return (f"Assignment(title='{self._title}', due_date='{self._due_date}', "
                f"course_code='{self._course_code}', weight={self._weight}, "
                f"status='{self._status}')")


if __name__ == "__main__":
    # Test the Assignment class
    print("=" * 60)
    print("Testing Assignment Class")
    print("=" * 60)
    
    # Create assignment
    assignment = Assignment('Project 1', '2025-11-15', 'INST326', 25.0, 
                           'project', 'in_progress', 8.0)
    print(f"\n1. Created assignment: {assignment}")
    print(f"   Repr: {repr(assignment)}")
    
    # Test priority calculation
    print("\n2. Priority calculation:")
    print(f"   Priority: {assignment.get_priority()}")
    
    # Test time remaining
    print("\n3. Time remaining:")
    time_remaining = assignment.calculate_time_remaining()
    print(f"   {time_remaining[0]} {time_remaining[1]} until due")
    
    # Test overdue check
    print("\n4. Overdue check:")
    print(f"   Is overdue: {assignment.is_overdue()}")
    
    # Test adding notes and instructions
    print("\n5. Add notes and instructions:")
    assignment.add_notes("Remember to test all edge cases")
    assignment.set_instructions("Create a Python function library with 15 functions")
    print(f"   Notes: {assignment.get_notes()}")
    print(f"   Instructions: {assignment.get_instructions()[:50]}...")
    
    # Test marking completed
    print("\n6. Mark assignment completed:")
    assignment.mark_completed(95.0)
    print(f"   Completed: {assignment.is_completed()}")
    print(f"   Score: {assignment.score}%")
    print(f"   New priority: {assignment.get_priority()}")
    print(f"   Updated string: {assignment}")
    
    # Test overdue assignment
    print("\n7. Test overdue assignment:")
    overdue = Assignment('Late Assignment', '2025-10-01', 'INST314', 10.0, 
                        'homework', 'not_started')
    print(f"   Assignment: {overdue}")
    print(f"   Is overdue: {overdue.is_overdue()}")
    print(f"   Priority: {overdue.get_priority()}")
    
    # Test high-priority assignment
    print("\n8. Test high-priority assignment:")
    urgent = Assignment('Final Exam', '2025-11-02', 'CMSC131', 40.0, 
                       'exam', 'not_started')
    print(f"   Assignment: {urgent}")
    print(f"   Priority: {urgent.get_priority()}")
    
    # Test property access
    print("\n9. Test property access:")
    print(f"   Title: {assignment.title}")
    print(f"   Due date: {assignment.due_date}")
    print(f"   Course code: {assignment.course_code}")
    print(f"   Weight: {assignment.weight}%")
    print(f"   Type: {assignment.assignment_type}")
    print(f"   Estimated hours: {assignment.estimated_hours}")
    
    # Test status updates
    print("\n10. Test status updates:")
    new_assignment = Assignment('Quiz 1', '2025-11-20', 'INST326', 5.0)
    print(f"    Initial status: {new_assignment.status}")
    new_assignment.status = 'in_progress'
    print(f"    Updated status: {new_assignment.status}")
    
    print("\n" + "=" * 60)
    print("All Assignment class tests passed!")
    print("=" * 60)