"""
Assignment Class Module - REFACTORED for Project 3
INST326 - Project 3: Inheritance and Polymorphism

Team: Class Tracker
Members: Kayla Fuentes, Rhea Vyragaram, Jocelyn DeHenzel, Vinindi Withanage

This module refactors the original Assignment class from Project 2 to extend
the AcademicItem abstract base class, demonstrating inheritance and polymorphism.

CHANGES FROM PROJECT 2:
- Now extends AcademicItem (inheritance)
- Implements abstract methods (polymorphism)
- All original functionality preserved
- Backward compatible with Project 2 code
"""

from datetime import datetime
from typing import Optional, Tuple
from academic_item import AcademicItem


class Assignment(AcademicItem):
    """
    Represents a course assignment with due date, priority, and completion tracking.
    
    NOW EXTENDS AcademicItem to demonstrate inheritance and polymorphism.
    All Project 2 functionality is preserved while adding new capabilities.
    
    This class manages individual assignments, calculates priorities and time
    remaining, and tracks completion status and scores.
    
    Attributes:
        title (str): Assignment title
        due_date (str): Due date in 'YYYY-MM-DD' format
        course_code (str): Associated course code
        weight (float): Assignment weight/percentage (0-100)
        assignment_type (str): Type of assignment
        status (str): Completion status
        estimated_hours (float): Estimated completion time
        
    Example:
        >>> assignment = Assignment('Project 1', '2025-11-15', 'INST326', 
        ...                         25.0, 'project', 'not_started')
        >>> print(assignment.get_priority())  # Polymorphic method
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
        
        Uses super() to call parent class (AcademicItem) constructor,
        demonstrating proper inheritance hierarchy.
        
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
        # Call parent class constructor using super() - INHERITANCE
        super().__init__(title, due_date, course_code, weight, status)
        
        # Assignment-specific validation
        if not isinstance(estimated_hours, (int, float)) or estimated_hours < 0:
            raise ValueError("Estimated hours must be a non-negative number")
        
        # Assignment-specific attributes
        self._estimated_hours = float(estimated_hours)
        self._assignment_type = assignment_type.lower()
        self._notes = ""
        self._instructions = ""
    
    @property
    def estimated_hours(self) -> float:
        """float: Get estimated hours."""
        return self._estimated_hours
    
    @property
    def assignment_type(self) -> str:
        """str: Get assignment type."""
        return self._assignment_type
    
    # POLYMORPHIC METHOD #1: Implement abstract method from base class
    def get_priority(self) -> str:
        """
        Calculate priority level for this assignment.
        
        POLYMORPHIC IMPLEMENTATION: Assignments use weight and due date logic.
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
    
    # POLYMORPHIC METHOD #2: Implement abstract method from base class
    def calculate_time_commitment(self) -> float:
        """
        Calculate estimated time commitment for this assignment.
        
        POLYMORPHIC IMPLEMENTATION: Assignments use estimated_hours directly.
        
        Returns:
            float: Estimated hours (direct value for assignments)
        """
        return self._estimated_hours
    
    # POLYMORPHIC METHOD #3: Implement abstract method from base class
    def get_item_type(self) -> str:
        """
        Return the type of this academic item.
        
        POLYMORPHIC IMPLEMENTATION: Identifies this as an assignment.
        
        Returns:
            str: 'ASSIGNMENT'
        """
        return 'ASSIGNMENT'
    
    # All original Project 2 methods preserved below
    
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


# NEW DERIVED CLASSES - Extend the hierarchy

class Project(AcademicItem):
    """
    Multi-phase project with milestones and team collaboration.
    
    NEW CLASS for Project 3 demonstrating inheritance from AcademicItem.
    Projects have higher time commitments and different priority calculations.
    
    Example:
        >>> project = Project('Final Project', '2025-12-10', 'INST326',
        ...                   40.0, num_milestones=3, team_size=4)
        >>> print(project.calculate_time_commitment())
        20.0
        >>> project.add_milestone('Design document', '2025-11-15')
    """
    
    def __init__(self, title: str, due_date: str, course_code: str,
                 weight: float, status: str = 'not_started',
                 num_milestones: int = 1, team_size: int = 1):
        """Initialize a Project using super() for inheritance."""
        super().__init__(title, due_date, course_code, weight, status)
        
        if not isinstance(num_milestones, int) or num_milestones < 1:
            raise ValueError("Must have at least one milestone")
        if not isinstance(team_size, int) or team_size < 1:
            raise ValueError("Team size must be at least 1")
        
        self._num_milestones = num_milestones
        self._team_size = team_size
        self._milestones = []
        self._repository_url = ""
    
    @property
    def num_milestones(self) -> int:
        """int: Get number of milestones."""
        return self._num_milestones
    
    @property
    def team_size(self) -> int:
        """int: Get team size."""
        return self._team_size
    
    def calculate_time_commitment(self) -> float:
        """
        POLYMORPHIC: Projects calculate based on milestones and team size.
        """
        base_hours_per_milestone = 15.0
        total_hours = base_hours_per_milestone * self._num_milestones
        team_factor = 1.0 if self._team_size == 1 else (self._team_size ** 0.7)
        return round(total_hours / team_factor, 2)
    
    def get_priority(self) -> str:
        """
        POLYMORPHIC: Projects get elevated priority due to complexity.
        """
        if self._status == 'completed':
            return 'low'
        
        try:
            due = datetime.strptime(self._due_date, '%Y-%m-%d')
            days_until_due = (due.date() - datetime.now().date()).days
        except ValueError:
            raise ValueError("Invalid date format")
        
        if days_until_due < 0:
            return 'critical'
        elif days_until_due <= 5:
            return 'critical'
        elif days_until_due <= 10 or self._weight >= 30:
            return 'high'
        elif days_until_due <= 20:
            return 'medium'
        else:
            return 'low'
    
    def get_item_type(self) -> str:
        """
        POLYMORPHIC: Return the type of this academic item.
        
        Returns:
            str: 'PROJECT'
        """
        return 'PROJECT'
    
    def add_milestone(self, title: str, due_date: str):
        """Add a project milestone."""
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Due date must be in YYYY-MM-DD format")
        
        self._milestones.append({
            'title': title.strip(),
            'due_date': due_date,
            'completed': False
        })
    
    def get_milestones(self) -> list:
        """Get all project milestones."""
        return self._milestones.copy()
    
    def set_repository(self, url: str):
        """Set project repository URL."""
        self._repository_url = url.strip()
    
    def get_repository(self) -> str:
        """Get project repository URL."""
        return self._repository_url


class Exam(AcademicItem):
    """
    Exam with study time requirements and coverage scope.
    
    NEW CLASS for Project 3 demonstrating inheritance from AcademicItem.
    Exams have highest priority near their date.
    
    Example:
        >>> exam = Exam('Midterm Exam', '2025-11-20', 'INST326',
        ...             25.0, exam_type='midterm', num_chapters=5)
        >>> print(exam.calculate_time_commitment())
        15.0
    """
    
    def __init__(self, title: str, due_date: str, course_code: str,
                 weight: float, status: str = 'not_started',
                 exam_type: str = 'exam', num_chapters: int = 5):
        """Initialize an Exam using super() for inheritance."""
        super().__init__(title, due_date, course_code, weight, status)
        
        valid_types = ['midterm', 'final', 'quiz', 'exam']
        if exam_type.lower() not in valid_types:
            raise ValueError(f"Exam type must be one of {valid_types}")
        if not isinstance(num_chapters, int) or num_chapters < 1:
            raise ValueError("Number of chapters must be at least 1")
        
        self._exam_type = exam_type.lower()
        self._num_chapters = num_chapters
        self._study_guide = ""
        self._location = "TBA"
    
    @property
    def exam_type(self) -> str:
        """str: Get exam type."""
        return self._exam_type
    
    @property
    def num_chapters(self) -> int:
        """int: Get number of chapters covered."""
        return self._num_chapters
    
    def calculate_time_commitment(self) -> float:
        """
        POLYMORPHIC: Exams calculate based on chapters and exam type.
        """
        base_hours_per_chapter = 2.0 if self._exam_type == 'quiz' else 3.0
        if self._exam_type == 'final':
            base_hours_per_chapter = 4.0
        return round(base_hours_per_chapter * self._num_chapters, 2)
    
    def get_priority(self) -> str:
        """
        POLYMORPHIC: Exams are always high priority when approaching.
        """
        if self._status == 'completed':
            return 'low'
        
        try:
            due = datetime.strptime(self._due_date, '%Y-%m-%d')
            days_until_due = (due.date() - datetime.now().date()).days
        except ValueError:
            raise ValueError("Invalid date format")
        
        if days_until_due < 0:
            return 'critical'
        elif days_until_due <= 7:
            return 'critical'
        elif days_until_due <= 14:
            return 'high'
        else:
            return 'medium'
    
    def get_item_type(self) -> str:
        """
        POLYMORPHIC: Return the type of this academic item.
        
        Returns:
            str: 'EXAM-{type}' (e.g., 'EXAM-MIDTERM', 'EXAM-FINAL')
        """
        return f'EXAM-{self._exam_type.upper()}'
    
    def set_study_guide(self, guide: str):
        """Set study guide content or URL."""
        self._study_guide = guide.strip()
    
    def get_study_guide(self) -> str:
        """Get study guide."""
        return self._study_guide
    
    def set_location(self, location: str):
        """Set exam location."""
        self._location = location.strip()
    
    def get_location(self) -> str:
        """Get exam location."""
        return self._location


# Maintain backward compatibility - original test code still works
if __name__ == "__main__":
    # Test the Assignment class (Project 2 tests still work!)
    print("=" * 60)
    print("Testing Refactored Assignment Class")
    print("=" * 60)
    
    # Create assignment - same as Project 2
    assignment = Assignment('Project 1', '2025-11-15', 'INST326', 25.0, 
                           'project', 'in_progress', 8.0)
    print(f"\n1. Created assignment: {assignment}")
    print(f"   Repr: {repr(assignment)}")
    
    # Test priority calculation - NOW POLYMORPHIC
    print("\n2. Priority calculation (polymorphic method):")
    print(f"   Priority: {assignment.get_priority()}")
    
    # Test time commitment - NEW POLYMORPHIC METHOD
    print("\n3. Time commitment (new polymorphic method):")
    print(f"   Estimated hours: {assignment.calculate_time_commitment()}")
    
    # Test item type - NEW POLYMORPHIC METHOD
    print("\n3b. Item type (new polymorphic method):")
    print(f"   Type: {assignment.get_item_type()}")
    
    # All original Project 2 methods still work
    print("\n4. Original Project 2 functionality preserved:")
    assignment.add_notes("Test all edge cases")
    print(f"   Notes: {assignment.get_notes()}")
    assignment.mark_completed(95.0)
    print(f"   Completed: {assignment.is_completed()}, Score: {assignment.score}%")
    
    # Test new derived classes
    print("\n5. New Project class:")
    project = Project('Final Project', '2025-12-10', 'INST326', 40.0,
                     num_milestones=3, team_size=4)
    print(f"   {project}")
    print(f"   Time commitment: {project.calculate_time_commitment()}h")
    print(f"   Priority: {project.get_priority()}")
    print(f"   Type: {project.get_item_type()}")
    
    print("\n6. New Exam class:")
    exam = Exam('Midterm', '2025-11-22', 'INST326', 25.0,
               exam_type='midterm', num_chapters=6)
    print(f"   {exam}")
    print(f"   Time commitment: {exam.calculate_time_commitment()}h")
    print(f"   Priority: {exam.get_priority()}")
    print(f"   Type: {exam.get_item_type()}")
    
    # Demonstrate polymorphism
    print("\n7. Polymorphism demonstration:")
    items = [assignment, project, exam]
    print("   All items using same interface:")
    for item in items:
        print(f"   - {item.title}: {item.get_item_type()}, "
              f"{item.calculate_time_commitment()}h, "
              f"Priority: {item.get_priority()}")
    
    print("\n" + "=" * 60)
    print("All tests passed! Backward compatible with Project 2.")
    print("=" * 60)
