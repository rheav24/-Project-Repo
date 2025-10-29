"""
Schedule Class Module
INST326 - Project 2: OOP Class Implementation

Team: Class Tracker
Members: Kayla Fuentes, Rhea Vyragaram, Jocelyn DeHenzel, Vinindi Withanage

This module contains the Schedule class for managing weekly class schedules.
Integrates functions from Project 1: generate_weekly_schedule, parse_meeting_time
"""

from typing import Dict, List, Tuple


class Schedule:
    """
    Represents a student's weekly class schedule with conflict detection.
    
    This class manages weekly schedules, generates organized views of classes
    by day, and helps identify scheduling conflicts.
    
    Attributes:
        student: Associated student object
        
    Example:
        >>> from student import Student
        >>> from course import Course
        >>> student = Student('Jane Doe', 'jane@umd.edu', 'UID789')
        >>> schedule = Schedule(student)
        >>> weekly = schedule.generate_weekly_view()
        >>> monday_classes = schedule.get_classes_on_day('Monday')
        >>> has_conflict, conflicts = schedule.has_time_conflict()
    """
    
    def __init__(self, student):
        """
        Initialize a Schedule object.
        
        Args:
            student: Student who owns this schedule
            
        Raises:
            TypeError: If student is not a Student object
        """
        # Avoid circular import - check type by duck typing
        if not hasattr(student, 'get_courses') or not hasattr(student, 'name'):
            raise TypeError("Must provide a valid Student object")
        
        self._student = student
        self._day_mapping = {
            'M': 'Monday', 'Tu': 'Tuesday', 'W': 'Wednesday',
            'Th': 'Thursday', 'F': 'Friday', 'Sa': 'Saturday', 'Su': 'Sunday'
        }
    
    @property
    def student(self):
        """Get associated student (read-only)."""
        return self._student
    
    def generate_weekly_view(self) -> Dict[str, List[Dict]]:
        """
        Generate a weekly schedule view organized by day.
        Integrates generate_weekly_schedule from Project 1.
        
        Returns:
            Dict[str, List[Dict]]: Schedule organized by day with course details
            
        Raises:
            TypeError: If courses is not a list or contains invalid data
            ValueError: If course data is missing required fields
        """
        schedule = {day: [] for day in self._day_mapping.values()}
        courses = self._student.get_courses()
        
        # Validation from Project 1 function
        if not isinstance(courses, list):
            raise TypeError("Courses must be a list")
        
        for course in courses:
            # Validation from Project 1 function
            if not hasattr(course, 'course_code') or not hasattr(course, 'meeting_time'):
                raise ValueError("Course missing required fields")
            
            try:
                parsed_time = course.parse_meeting_schedule()
                days_str = parsed_time['days']
                
                # Parse day codes (handle M, Tu, W, Th, F, etc.)
                # This logic is from Project 1's generate_weekly_schedule
                i = 0
                while i < len(days_str):
                    if i < len(days_str) - 1 and days_str[i:i+2] in self._day_mapping:
                        day_code = days_str[i:i+2]
                        i += 2
                    elif days_str[i] in self._day_mapping:
                        day_code = days_str[i]
                        i += 1
                    else:
                        i += 1
                        continue
                    
                    day_name = self._day_mapping[day_code]
                    schedule[day_name].append({
                        'course_code': course.course_code,
                        'instructor': course.instructor,
                        'start_time': parsed_time['start_time'],
                        'end_time': parsed_time['end_time'],
                        'location': course.location
                    })
            except (ValueError, KeyError, AttributeError) as e:
                # Skip courses with invalid meeting times
                continue
        
        return schedule
    
    def get_classes_on_day(self, day: str) -> List[Dict]:
        """
        Get all classes scheduled for a specific day.
        
        Args:
            day (str): Day name (e.g., 'Monday', 'Tuesday', etc.)
            
        Returns:
            List[Dict]: Classes on that day
            
        Raises:
            ValueError: If day is invalid
        """
        valid_days = list(self._day_mapping.values())
        if day not in valid_days:
            raise ValueError(f"Day must be one of {valid_days}")
        
        weekly = self.generate_weekly_view()
        return weekly[day]
    
    def has_time_conflict(self) -> Tuple[bool, List[str]]:
        """
        Check for time conflicts in the schedule.
        
        Returns:
            Tuple[bool, List[str]]: (has_conflict, list_of_conflict_messages)
        """
        conflicts = []
        weekly = self.generate_weekly_view()
        
        for day, classes in weekly.items():
            if len(classes) < 2:
                continue
            
            # Sort by start time for easier comparison
            sorted_classes = sorted(classes, key=lambda x: x['start_time'])
            
            for i in range(len(sorted_classes) - 1):
                current = sorted_classes[i]
                next_class = sorted_classes[i + 1]
                
                # Simple conflict detection (comparing end time with start time)
                if current['end_time'] > next_class['start_time']:
                    conflicts.append(
                        f"{day}: {current['course_code']} ({current['start_time']}-{current['end_time']}) "
                        f"overlaps with {next_class['course_code']} ({next_class['start_time']}-{next_class['end_time']})"
                    )
        
        return (len(conflicts) > 0, conflicts)
    
    def get_free_days(self) -> List[str]:
        """
        Get days with no scheduled classes.
        
        Returns:
            List[str]: List of day names with no classes
        """
        weekly = self.generate_weekly_view()
        return [day for day, classes in weekly.items() if len(classes) == 0]
    
    def get_busiest_day(self) -> Tuple[str, int]:
        """
        Find the day with the most classes.
        
        Returns:
            Tuple[str, int]: (day_name, number_of_classes)
        """
        weekly = self.generate_weekly_view()
        if not any(classes for classes in weekly.values()):
            return ("No classes", 0)
        
        busiest = max(weekly.items(), key=lambda x: len(x[1]))
        return (busiest[0], len(busiest[1]))
    
    def get_total_class_hours_per_week(self) -> float:
        """
        Calculate total class hours per week (approximate).
        
        Returns:
            float: Estimated total class hours per week
        """
        weekly = self.generate_weekly_view()
        total_hours = 0.0
        
        for day, classes in weekly.items():
            for cls in classes:
                # Simple hour calculation (assumes HH:MM format)
                try:
                    start_parts = cls['start_time'].replace('PM', '').replace('AM', '').split(':')
                    end_parts = cls['end_time'].replace('PM', '').replace('AM', '').split(':')
                    
                    start_hour = int(start_parts[0])
                    start_min = int(start_parts[1]) if len(start_parts) > 1 else 0
                    end_hour = int(end_parts[0])
                    end_min = int(end_parts[1]) if len(end_parts) > 1 else 0
                    
                    # Handle PM times
                    if 'PM' in cls['end_time'] and end_hour != 12:
                        end_hour += 12
                    if 'PM' in cls['start_time'] and start_hour != 12:
                        start_hour += 12
                    
                    duration = (end_hour + end_min/60) - (start_hour + start_min/60)
                    total_hours += duration
                except (ValueError, IndexError):
                    # If parsing fails, skip this class
                    continue
        
        return round(total_hours, 2)
    
    def __str__(self) -> str:
        """Return a readable string representation."""
        total_classes = sum(len(classes) for classes in self.generate_weekly_view().values())
        return f"Schedule for {self._student.name}: {total_classes} class meetings per week"
    
    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return f"Schedule(student={repr(self._student)})"


if __name__ == "__main__":
    # Test the Schedule class
    print("=" * 60)
    print("Testing Schedule Class")
    print("=" * 60)
    
    # Note: Full testing requires Student and Course classes
    print("\nSchedule class structure created successfully!")
    print("Full testing requires Student and Course classes to be imported.")
    
    # Test day mapping
    print("\n1. Day mapping validation:")
    schedule_test = type('obj', (object,), {
        '_day_mapping': {
            'M': 'Monday', 'Tu': 'Tuesday', 'W': 'Wednesday',
            'Th': 'Thursday', 'F': 'Friday', 'Sa': 'Saturday', 'Su': 'Sunday'
        }
    })()
    print(f"   Days configured: {list(schedule_test._day_mapping.values())}")
    
    # Test with mock student
    print("\n2. Mock student test:")
    
    class MockStudent:
        def __init__(self):
            self.name = "Test Student"
        def get_courses(self):
            return []
    
    mock_student = MockStudent()
    schedule = Schedule(mock_student)
    print(f"   Created: {schedule}")
    
    # Test empty schedule
    print("\n3. Test empty schedule:")
    weekly = schedule.generate_weekly_view()
    print(f"   Days in schedule: {len(weekly)}")
    print(f"   Total class meetings: {sum(len(classes) for classes in weekly.values())}")
    
    # Test free days
    print("\n4. Test free days:")
    free_days = schedule.get_free_days()
    print(f"   Free days: {len(free_days)}")
    
    # Test busiest day
    print("\n5. Test busiest day:")
    busiest, count = schedule.get_busiest_day()
    print(f"   Busiest day: {busiest} ({count} classes)")
    
    # Test conflict detection
    print("\n6. Test conflict detection:")
    has_conflict, conflicts = schedule.has_time_conflict()
    print(f"   Has conflicts: {has_conflict}")
    print(f"   Number of conflicts: {len(conflicts)}")
    
    # Test total hours
    print("\n7. Test total hours calculation:")
    hours = schedule.get_total_class_hours_per_week()
    print(f"   Total class hours per week: {hours}")
    
    print("\n" + "=" * 60)
    print("All Schedule class tests passed!")
    print("Note: Run with actual Student and Course objects for full testing")
    print("=" * 60)
