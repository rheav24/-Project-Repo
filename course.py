"""
Course Class Module
INST326 - Project 2: OOP Class Implementation

Team: Class Tracker
Members: Kayla Fuentes, Rhea Vyragaram, Jocelyn DeHenzel, Vinindi Withanage

This module contains the Course class for managing college course information.
Integrates functions from Project 1: format_course_code, parse_meeting_time
"""

from typing import List, Dict


class Course:
    """
    Represents a college course with schedule, instructor, and enrollment details.
    
    This class manages course information including meeting times, credits,
    and related resources. It integrates functions from Project 1 for course
    management and validation.
    
    Attributes:
        course_code (str): Unique course identifier (e.g., 'INST326')
        instructor (str): Instructor name
        credits (float): Course credit hours
        meeting_time (str): Meeting schedule (e.g., 'MWF 10:00-10:50')
        location (str): Classroom location
        
    Example:
        >>> course = Course('INST326', 'Dr. Smith', 3.0, 'TuTh 2:00-3:15', 'HBK 0104')
        >>> print(course)
        INST326: Dr. Smith (3.0 credits) - TuTh 2:00-3:15
        >>> course.add_resource('textbook', 'Python Crash Course', 'https://example.com')
        >>> resources = course.get_resources_by_type('textbook')
    """
    
    def __init__(self, course_code: str, instructor: str, credits: float,
                 meeting_time: str, location: str = 'TBA',
                 office_hours: str = 'By appointment'):
        """
        Initialize a Course object.
        
        Args:
            course_code (str): Course code (will be formatted to uppercase)
            instructor (str): Instructor name
            credits (float): Credit hours (must be positive)
            meeting_time (str): Meeting schedule string
            location (str, optional): Classroom location
            office_hours (str, optional): Instructor office hours
            
        Raises:
            TypeError: If arguments are not correct types
            ValueError: If course_code is empty or credits are not positive
        """
        # Input validation
        if not isinstance(course_code, str) or not course_code.strip():
            raise ValueError("Course code must be a non-empty string")
        if not isinstance(instructor, str) or not instructor.strip():
            raise ValueError("Instructor must be a non-empty string")
        if not isinstance(credits, (int, float)) or credits <= 0:
            raise ValueError("Credits must be a positive number")
        if not isinstance(meeting_time, str):
            raise TypeError("Meeting time must be a string")
        
        # Private attributes with encapsulation
        self._course_code = self._format_course_code(course_code)
        self._instructor = instructor.strip()
        self._credits = float(credits)
        self._meeting_time = meeting_time.strip()
        self._location = location.strip()
        self._office_hours = office_hours
        self._resources = []
        self._syllabus_info = {}
    
    @property
    def course_code(self) -> str:
        """str: Get the course code (read-only)."""
        return self._course_code
    
    @property
    def instructor(self) -> str:
        """str: Get the instructor name."""
        return self._instructor
    
    @instructor.setter
    def instructor(self, value: str):
        """Set the instructor name with validation."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Instructor must be a non-empty string")
        self._instructor = value.strip()
    
    @property
    def credits(self) -> float:
        """float: Get course credits (read-only)."""
        return self._credits
    
    @property
    def meeting_time(self) -> str:
        """str: Get meeting time."""
        return self._meeting_time
    
    @property
    def location(self) -> str:
        """str: Get course location."""
        return self._location
    
    @location.setter
    def location(self, value: str):
        """Set course location."""
        self._location = value.strip() if value else 'TBA'
    
    @property
    def office_hours(self) -> str:
        """str: Get instructor office hours."""
        return self._office_hours
    
    def _format_course_code(self, course_code: str) -> str:
        """
        Format course code to standard uppercase format.
        Integrates format_course_code from Project 1.
        
        Args:
            course_code (str): Raw course code
            
        Returns:
            str: Formatted course code in uppercase
            
        Raises:
            TypeError: If course_code is not a string
            ValueError: If course_code is empty
        """
        if not isinstance(course_code, str):
            raise TypeError("Course code must be a string")
        if not course_code.strip():
            raise ValueError("Course code cannot be empty")
        return course_code.strip().upper()
    
    def parse_meeting_schedule(self) -> Dict[str, str]:
        """
        Parse meeting time into structured components.
        Integrates parse_meeting_time from Project 1.
        
        Returns:
            Dict[str, str]: Dictionary with 'days', 'start_time', 'end_time'
            
        Raises:
            ValueError: If meeting time format is invalid
        """
        parts = self._meeting_time.strip().split()
        if len(parts) < 2:
            raise ValueError("Meeting time must include days and time range")
        
        days = parts[0]
        time_range = parts[1]
        
        if '-' not in time_range:
            raise ValueError("Time range must include start and end times separated by '-'")
        
        times = time_range.split('-')
        if len(times) != 2:
            raise ValueError("Invalid time range format")
        
        return {
            'days': days,
            'start_time': times[0].strip(),
            'end_time': times[1].strip()
        }
    
    def add_resource(self, resource_type: str, title: str, 
                    url: str = '', notes: str = ''):
        """
        Add a course resource (textbook, article, video, etc.).
        
        Args:
            resource_type (str): Type of resource (textbook, article, video, 
                               website, document, other)
            title (str): Resource title
            url (str, optional): Resource URL
            notes (str, optional): Additional notes
            
        Raises:
            ValueError: If required fields are empty or type is invalid
        """
        if not title.strip():
            raise ValueError("Resource title cannot be empty")
        
        valid_types = ['textbook', 'article', 'video', 'website', 'document', 'other']
        resource_type = resource_type.lower()
        if resource_type not in valid_types:
            raise ValueError(f"Resource type must be one of {valid_types}")
        
        self._resources.append({
            'type': resource_type,
            'title': title.strip(),
            'url': url.strip(),
            'notes': notes.strip()
        })
    
    def get_resources_by_type(self, resource_type: str) -> List[Dict]:
        """
        Get all resources of a specific type.
        
        Args:
            resource_type (str): Type to filter by
            
        Returns:
            List[Dict]: Filtered list of resources
        """
        return [r for r in self._resources if r['type'] == resource_type.lower()]
    
    def get_all_resources(self) -> List[Dict]:
        """
        Get all course resources.
        
        Returns:
            List[Dict]: Copy of all resources
        """
        return self._resources.copy()
    
    def set_syllabus_info(self, key: str, value: str):
        """
        Store syllabus information for the course.
        
        Args:
            key (str): Information key (e.g., 'grading_policy', 'prerequisites')
            value (str): Information value
        """
        if not isinstance(key, str) or not key.strip():
            raise ValueError("Key must be a non-empty string")
        self._syllabus_info[key.strip()] = str(value)
    
    def get_syllabus_info(self, key: str) -> str:
        """
        Retrieve syllabus information.
        
        Args:
            key (str): Information key
            
        Returns:
            str: Information value or empty string if not found
        """
        return self._syllabus_info.get(key.strip(), '')
    
    def __str__(self) -> str:
        """Return a readable string representation."""
        return f"{self._course_code}: {self._instructor} ({self._credits} credits) - {self._meeting_time}"
    
    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return (f"Course(course_code='{self._course_code}', "
                f"instructor='{self._instructor}', credits={self._credits}, "
                f"meeting_time='{self._meeting_time}', location='{self._location}')")


if __name__ == "__main__":
    # Test the Course class
    print("=" * 60)
    print("Testing Course Class")
    print("=" * 60)
    
    # Create course
    course = Course('inst326', 'Dr. Smith', 3.0, 'TuTh 2:00-3:15', 'HBK 0104', 'M 2-4PM')
    print(f"\n1. Created course: {course}")
    print(f"   Repr: {repr(course)}")
    
    # Test parsing meeting time
    print("\n2. Parse meeting schedule:")
    schedule = course.parse_meeting_schedule()
    print(f"   Days: {schedule['days']}")
    print(f"   Start: {schedule['start_time']}")
    print(f"   End: {schedule['end_time']}")
    
    # Test adding resources
    print("\n3. Add resources:")
    course.add_resource('textbook', 'Python Crash Course', 'https://example.com/book')
    course.add_resource('video', 'OOP Tutorial Series', 'https://youtube.com/playlist')
    course.add_resource('textbook', 'Learning Python', 'https://example.com/book2')
    print(f"   Total resources: {len(course.get_all_resources())}")
    
    # Test filtering resources
    print("\n4. Filter resources by type:")
    textbooks = course.get_resources_by_type('textbook')
    videos = course.get_resources_by_type('video')
    print(f"   Textbooks: {len(textbooks)}")
    for book in textbooks:
        print(f"      - {book['title']}")
    print(f"   Videos: {len(videos)}")
    
    # Test syllabus info
    print("\n5. Set syllabus information:")
    course.set_syllabus_info('grading_policy', '40% Projects, 30% Exams, 30% Homework')
    course.set_syllabus_info('prerequisites', 'INST126')
    print(f"   Grading: {course.get_syllabus_info('grading_policy')}")
    print(f"   Prerequisites: {course.get_syllabus_info('prerequisites')}")
    
    # Test property access
    print("\n6. Test properties:")
    print(f"   Course code: {course.course_code}")
    print(f"   Instructor: {course.instructor}")
    print(f"   Credits: {course.credits}")
    print(f"   Location: {course.location}")
    print(f"   Office hours: {course.office_hours}")
    
    # Test changing location
    print("\n7. Update location:")
    course.location = "ESJ 2204"
    print(f"   New location: {course.location}")
    
    print("\n" + "=" * 60)
    print("All Course class tests passed!")
    print("=" * 60)
