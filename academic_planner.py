"""
Academic Planner Class - Composition Example
INST326 - Project 3: Inheritance and Polymorphism

Team: Class Tracker
Members: Kayla Fuentes, Rhea Vyragaram, Jocelyn DeHenzel, Vinindi Withanage

This module demonstrates composition relationships where AcademicPlanner
"has-a" collection of AcademicItems and manages them collectively.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from academic_item import AcademicItem


class AcademicPlanner:
    """
    Manages a collection of academic items using composition.
    
    This class demonstrates the "has-a" relationship - an AcademicPlanner
    HAS many AcademicItems. It provides high-level management and analysis
    of all academic work.
    
    Composition was chosen over inheritance because:
    - A planner is not a "type of" academic item
    - It manages and coordinates multiple items
    - It provides aggregate analysis across items
    - It needs to exist independently of any specific item
    
    Example:
        >>> from assignment_types import Assignment, Project, Exam
        >>> planner = AcademicPlanner("John Doe")
        >>> assignment = Assignment('HW1', '2025-11-25', 'INST326', 10.0)
        >>> planner.add_item(assignment)
        >>> workload = planner.calculate_weekly_workload()
        >>> critical_items = planner.get_items_by_priority('critical')
    """
    
    def __init__(self, student_name: str):
        """
        Initialize an Academic Planner.
        
        Args:
            student_name (str): Name of student this planner belongs to
        """
        if not isinstance(student_name, str) or not student_name.strip():
            raise ValueError("Student name must be a non-empty string")
        
        self._student_name = student_name.strip()
        self._items = []  # Composition: planner HAS items
        self._created_date = datetime.now().strftime('%Y-%m-%d')
    
    @property
    def student_name(self) -> str:
        """str: Get student name."""
        return self._student_name
    
    @property
    def created_date(self) -> str:
        """str: Get creation date."""
        return self._created_date
    
    def add_item(self, item: AcademicItem):
        """
        Add an academic item to the planner.
        
        Demonstrates composition - the planner contains items.
        
        Args:
            item (AcademicItem): Item to add (Assignment, Project, or Exam)
            
        Raises:
            TypeError: If item is not an AcademicItem
        """
        if not isinstance(item, AcademicItem):
            raise TypeError("Item must be an AcademicItem instance")
        
        self._items.append(item)
    
    def remove_item(self, title: str, course_code: str) -> bool:
        """
        Remove an item by title and course code.
        
        Args:
            title (str): Item title
            course_code (str): Course code
            
        Returns:
            bool: True if removed, False if not found
        """
        for i, item in enumerate(self._items):
            if item.title == title and item.course_code == course_code.upper():
                self._items.pop(i)
                return True
        return False
    
    def get_all_items(self) -> List[AcademicItem]:
        """
        Get all items in planner.
        
        Returns:
            List[AcademicItem]: Copy of all items
        """
        return self._items.copy()
    
    def get_items_by_course(self, course_code: str) -> List[AcademicItem]:
        """
        Get all items for a specific course.
        
        Demonstrates polymorphism - works with any AcademicItem subclass.
        
        Args:
            course_code (str): Course code to filter by
            
        Returns:
            List[AcademicItem]: Items for that course
        """
        course_code = course_code.upper()
        return [item for item in self._items if item.course_code == course_code]
    
    def get_items_by_priority(self, priority: str) -> List[AcademicItem]:
        """
        Get all items with specified priority.
        
        Demonstrates polymorphism - each item type calculates priority differently.
        
        Args:
            priority (str): Priority level to filter by
            
        Returns:
            List[AcademicItem]: Items with that priority
        """
        return [item for item in self._items if item.get_priority() == priority]
    
    def get_items_by_type(self, item_type: str) -> List[AcademicItem]:
        """
        Get all items of a specific type.
        
        Args:
            item_type (str): Type name (e.g., 'Assignment', 'Project', 'Exam')
            
        Returns:
            List[AcademicItem]: Items of that type
        """
        return [item for item in self._items 
                if item.__class__.__name__ == item_type]
    
    def calculate_weekly_workload(self, weeks_ahead: int = 1) -> Dict[str, float]:
        """
        Calculate workload distribution over coming weeks.
        
        Demonstrates polymorphism - each item type calculates time differently.
        
        Args:
            weeks_ahead (int): Number of weeks to calculate for
            
        Returns:
            Dict[str, float]: Date to hours mapping
        """
        workload = {}
        today = datetime.now().date()
        
        for week in range(weeks_ahead):
            week_start = today + timedelta(weeks=week)
            week_end = week_start + timedelta(days=6)
            week_key = f"Week {week + 1} ({week_start.strftime('%m/%d')})"
            
            week_hours = 0.0
            for item in self._items:
                if item.status == 'completed':
                    continue
                
                due_date = datetime.strptime(item.due_date, '%Y-%m-%d').date()
                if week_start <= due_date <= week_end:
                    # Polymorphic call - each type calculates differently
                    week_hours += item.calculate_time_commitment()
            
            workload[week_key] = round(week_hours, 2)
        
        return workload
    
    def get_upcoming_deadlines(self, days_ahead: int = 7) -> List[Dict]:
        """
        Get all deadlines in the next specified days.
        
        Args:
            days_ahead (int): Number of days to look ahead
            
        Returns:
            List[Dict]: Upcoming deadlines with details
        """
        deadlines = []
        today = datetime.now().date()
        cutoff = today + timedelta(days=days_ahead)
        
        for item in self._items:
            if item.status == 'completed':
                continue
            
            due_date = datetime.strptime(item.due_date, '%Y-%m-%d').date()
            if today <= due_date <= cutoff:
                days_until = (due_date - today).days
                deadlines.append({
                    'title': item.title,
                    'course': item.course_code,
                    'type': item.get_item_type(),
                    'due_date': item.due_date,
                    'days_until': days_until,
                    'priority': item.get_priority(),
                    'hours_needed': item.calculate_time_commitment()
                })
        
        # Sort by due date
        deadlines.sort(key=lambda x: x['due_date'])
        return deadlines
    
    def get_priority_summary(self) -> Dict[str, int]:
        """
        Get count of items at each priority level.
        
        Demonstrates polymorphism - each item calculates its own priority.
        
        Returns:
            Dict[str, int]: Priority level to count mapping
        """
        summary = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        
        for item in self._items:
            if item.status != 'completed':
                priority = item.get_priority()
                summary[priority] += 1
        
        return summary
    
    def get_completion_stats(self) -> Dict[str, any]:
        """
        Calculate completion statistics across all items.
        
        Returns:
            Dict: Statistics including completion rate, average score, etc.
        """
        total = len(self._items)
        if total == 0:
            return {
                'total_items': 0,
                'completed': 0,
                'in_progress': 0,
                'not_started': 0,
                'completion_rate': 0.0,
                'average_score': 0.0
            }
        
        completed = sum(1 for item in self._items if item.status == 'completed')
        in_progress = sum(1 for item in self._items if item.status == 'in_progress')
        not_started = sum(1 for item in self._items if item.status == 'not_started')
        
        # Calculate average score for completed items
        scores = [item.score for item in self._items if item.score is not None]
        avg_score = sum(scores) / len(scores) if scores else 0.0
        
        return {
            'total_items': total,
            'completed': completed,
            'in_progress': in_progress,
            'not_started': not_started,
            'completion_rate': round((completed / total) * 100, 2),
            'average_score': round(avg_score, 2)
        }
    
    def get_total_workload(self) -> float:
        """
        Calculate total hours needed for all incomplete items.
        
        Demonstrates polymorphism - each item type calculates differently.
        
        Returns:
            float: Total estimated hours
        """
        total_hours = 0.0
        for item in self._items:
            if item.status != 'completed':
                total_hours += item.calculate_time_commitment()
        
        return round(total_hours, 2)
    
    def get_items_by_status(self, status: str) -> List[AcademicItem]:
        """
        Get items filtered by completion status.
        
        Args:
            status (str): Status to filter by
            
        Returns:
            List[AcademicItem]: Filtered items
        """
        valid_statuses = ['completed', 'in_progress', 'not_started']
        if status not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")
        
        return [item for item in self._items if item.status == status]
    
    def __str__(self) -> str:
        """Return readable string representation."""
        stats = self.get_completion_stats()
        return (f"Academic Planner for {self._student_name}: "
                f"{stats['total_items']} items "
                f"({stats['completed']} completed, "
                f"{stats['in_progress']} in progress)")
    
    def __repr__(self) -> str:
        """Return detailed representation."""
        return (f"AcademicPlanner(student_name='{self._student_name}', "
                f"items={len(self._items)})")


if __name__ == "__main__":
    print("=" * 60)
    print("Testing Academic Planner (Composition)")
    print("=" * 60)
    
    # Import derived classes for testing
    from assignment_types import Assignment, Project, Exam
    
    # Create planner
    planner = AcademicPlanner("Jane Smith")
    print(f"\n1. Created planner: {planner}")
    print(f"   Repr: {repr(planner)}")
    
    # Add various item types (demonstrating composition)
    print("\n2. Adding items (composition):")
    assignment = Assignment('Homework 3', '2025-11-25', 'INST326', 10.0, 
                           estimated_hours=3.0)
    project = Project('Final Project', '2025-12-10', 'INST326', 40.0,
                     num_milestones=3, team_size=4)
    exam = Exam('Midterm', '2025-11-22', 'INST326', 25.0,
               exam_type='midterm', num_chapters=6)
    
    planner.add_item(assignment)
    planner.add_item(project)
    planner.add_item(exam)
    print(f"   Items added: {len(planner.get_all_items())}")
    
    # Demonstrate polymorphism through planner
    print("\n3. Polymorphism - calculate workload:")
    workload = planner.calculate_weekly_workload(2)
    for week, hours in workload.items():
        print(f"   {week}: {hours} hours")
    
    # Priority analysis
    print("\n4. Priority summary:")
    priority_summary = planner.get_priority_summary()
    for priority, count in priority_summary.items():
        print(f"   {priority.capitalize()}: {count} items")
    
    # Upcoming deadlines
    print("\n5. Upcoming deadlines (next 30 days):")
    deadlines = planner.get_upcoming_deadlines(30)
    for deadline in deadlines:
        print(f"   {deadline['due_date']}: {deadline['title']} "
              f"({deadline['type']}) - {deadline['hours_needed']}h")
    
    # Get items by type
    print("\n6. Items by type:")
    for item_type in ['Assignment', 'Project', 'Exam']:
        items = planner.get_items_by_type(item_type)
        print(f"   {item_type}s: {len(items)}")
    
    # Total workload
    print("\n7. Total workload:")
    total = planner.get_total_workload()
    print(f"   Total hours needed: {total}")
    
    # Completion stats
    print("\n8. Completion statistics:")
    stats = planner.get_completion_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Mark an item complete
    print("\n9. Complete an item:")
    assignment.mark_completed(95.0)
    updated_stats = planner.get_completion_stats()
    print(f"   Completed: {updated_stats['completed']}")
    print(f"   Completion rate: {updated_stats['completion_rate']}%")
    print(f"   Average score: {updated_stats['average_score']}%")
    
    print("\n" + "=" * 60)
    print("All composition tests passed!")
    print("Composition allows planner to manage multiple items")
    print("while maintaining loose coupling and flexibility.")
    print("=" * 60)
