"""
Academic Item Abstract Base Class
INST326 - Project 3: Inheritance and Polymorphism

Team: Class Tracker
Members: Kayla Fuentes, Rhea Vyragaram, Jocelyn DeHenzel, Vinindi Withanage

This module refactors the existing Assignment class into an inheritance hierarchy.
The Assignment class from Project 2 now extends this abstract base class.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Tuple


class AcademicItem(ABC):
    """
    Abstract base class for all academic items with due dates and priorities.
    
    This refactors Project 2's Assignment class to be part of an inheritance
    hierarchy. The common functionality from Assignment is moved here, and
    specific implementations are in derived classes.
    
    Attributes:
        title (str): Item title
        due_date (str): Due date in 'YYYY-MM-DD' format
        course_code (str): Associated course code
        weight (float): Item weight/percentage (0-100)
        status (str): Completion status
    """
    
    def __init__(self, title: str, due_date: str, course_code: str,
                 weight: float, status: str = 'not_started'):
        """
        Initialize an AcademicItem.
        
        Args:
            title (str): Item title
            due_date (str): Due date in 'YYYY-MM-DD' format
            course_code (str): Course identifier
            weight (float): Weight/percentage (0-100)
            status (str): Initial status
            
        Raises:
            ValueError: If parameters are invalid
        """
        # Input validation (from original Assignment class)
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Title must be a non-empty string")
        if not isinstance(course_code, str) or not course_code.strip():
            raise ValueError("Course code must be a non-empty string")
        if not isinstance(weight, (int, float)) or not 0 <= weight <= 100:
            raise ValueError("Weight must be between 0 and 100")
        if status not in ['not_started', 'in_progress', 'completed']:
            raise ValueError("Status must be 'not_started', 'in_progress', or 'completed'")
        
        # Validate date format
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Due date must be in YYYY-MM-DD format")
        
        # Private attributes with encapsulation (from Project 2)
        self._title = title.strip()
        self._due_date = due_date
        self._course_code = course_code.upper()
        self._weight = float(weight)
        self._status = status
        self._score = None
        self._submission_date = None
    
    # Properties (from original Assignment class)
    @property
    def title(self) -> str:
        """str: Get item title."""
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
        """float: Get item weight."""
        return self._weight
    
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
        """Optional[float]: Get item score if completed."""
        return self._score
    
    # Abstract methods - must be implemented by subclasses
    @abstractmethod
    def get_priority(self) -> str:
        """
        Calculate priority level for this item.
        
        Must be implemented by all subclasses with their specific logic.
        Each type (Assignment, Project, Exam) calculates priority differently.
        
        Returns:
            str: Priority level ('critical', 'high', 'medium', 'low')
        """
        pass
    
    @abstractmethod
    def calculate_time_commitment(self) -> float:
        """
        Calculate estimated time commitment for this item.
        
        Must be implemented by all subclasses. Different item types
        calculate time requirements differently.
        
        Returns:
            float: Estimated hours needed
        """
        pass
    
    @abstractmethod
    def get_item_type(self) -> str:
        """
        Return the type of this academic item.
        
        Must be implemented by all subclasses to identify their type.
        
        Returns:
            str: Item type identifier (e.g., 'ASSIGNMENT', 'PROJECT', 'EXAM')
        """
        pass
    
    # Concrete methods - common implementation for all items (from Project 2 Assignment)
    def is_overdue(self, current_date: str = None) -> bool:
        """
        Check if item is overdue and not completed.
        Integrates is_assignment_overdue from Project 1.
        
        Args:
            current_date (str, optional): Current date in 'YYYY-MM-DD' format
            
        Returns:
            bool: True if overdue and not completed, False otherwise
        """
        # Completed items are never considered overdue
        if self._status == 'completed':
            return False
        
        try:
            due = datetime.strptime(self._due_date, '%Y-%m-%d')
            current = datetime.strptime(current_date, '%Y-%m-%d') if current_date else datetime.now()
            return current.date() > due.date()
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")
    
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
            raise ValueError(f"Invalid date format: {e}")
    
    def mark_completed(self, score: float, submission_date: str = None):
        """
        Mark item as completed with a score.
        
        Args:
            score (float): Score earned (0-100)
            submission_date (str, optional): Submission date
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
        """Check if item is completed."""
        return self._status == 'completed'
    
    def __str__(self) -> str:
        """Return a readable string representation."""
        time_info = self.calculate_time_remaining()
        if time_info[1] == 'overdue':
            time_str = f"OVERDUE by {time_info[0]} days"
        else:
            time_str = f"Due in {time_info[0]} {time_info[1]}"
        
        return f"{self._title} [{self._course_code}] - {time_str} (Priority: {self.get_priority()})"
    
    def __repr__(self) -> str:
        """Return detailed representation."""
        return (f"{self.__class__.__name__}(title='{self._title}', "
                f"due_date='{self._due_date}', course_code='{self._course_code}')")
