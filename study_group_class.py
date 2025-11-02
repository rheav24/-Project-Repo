"""
StudyGroup Class Module
INST326 - Project 2: OOP Class Implementation

Team: Class Tracker
Members: Kayla Fuentes, Rhea Vyragaram, Jocelyn DeHenzel, Vinindi Withanage

This module contains the StudyGroup class for managing study group collaboration.
Integrates functions from Project 1: generate_study_group_id
"""

from datetime import datetime
from typing import List, Dict


class StudyGroup:
    """
    Represents a study group for course collaboration.
    
    This class manages study group information, member tracking, and
    meeting coordination for collaborative learning.
    
    Attributes:
        course_code (str): Associated course code
        group_number (int): Group identifier number
        max_members (int): Maximum group capacity
        
    Example:
        >>> from student import Student
        >>> group = StudyGroup('INST326', 1, 5)
        >>> student = Student('Alice', 'alice@umd.edu', 'UID111')
        >>> group.add_member(student, 'alice@umd.edu', '555-1234')
        >>> group.schedule_meeting('2025-11-10', '3:00 PM', 'McKeldin Library')
        >>> print(group.get_member_count())
        1
    """
    
    def __init__(self, course_code: str, group_number: int, max_members: int = 6):
        """
        Initialize a StudyGroup object.
        
        Args:
            course_code (str): Course this group is for
            group_number (int): Group identifier (must be positive)
            max_members (int, optional): Maximum group size (default 6)
            
        Raises:
            ValueError: If parameters are invalid
            TypeError: If arguments are not correct types
        """
        # Input validation
        if not isinstance(course_code, str) or not course_code.strip():
            raise ValueError("Course code must be a non-empty string")
        if not isinstance(group_number, int) or group_number <= 0:
            raise ValueError("Group number must be a positive integer")
        if not isinstance(max_members, int) or max_members <= 0:
            raise ValueError("Max members must be a positive integer")
        
        # Private attributes with encapsulation
        self._course_code = self._format_course_code(course_code)
        self._group_number = group_number
        self._max_members = max_members
        self._members = []
        self._meetings = []
        self._group_id = self._generate_study_group_id()
        self._description = ""
    
    @property
    def course_code(self) -> str:
        """str: Get course code (read-only)."""
        return self._course_code
    
    @property
    def group_number(self) -> int:
        """int: Get group number (read-only)."""
        return self._group_number
    
    @property
    def group_id(self) -> str:
        """str: Get unique group ID (read-only)."""
        return self._group_id
    
    @property
    def max_members(self) -> int:
        """int: Get maximum member capacity."""
        return self._max_members
    
    @property
    def description(self) -> str:
        """str: Get group description."""
        return self._description
    
    @description.setter
    def description(self, value: str):
        """Set group description."""
        self._description = value.strip()
    
    def _format_course_code(self, course_code: str) -> str:
        """
        Format course code to uppercase.
        Uses logic from Project 1's format_course_code function.
        
        Args:
            course_code (str): Raw course code
            
        Returns:
            str: Formatted course code
        """
        if not isinstance(course_code, str):
            raise TypeError("Course code must be a string")
        if not course_code.strip():
            raise ValueError("Course code cannot be empty")
        return course_code.strip().upper()
    
    def _generate_study_group_id(self) -> str:
        """
        Generate unique study group identifier.
        Integrates generate_study_group_id from Project 1.
        
        Returns:
            str: Unique group ID in format 'COURSECODE_GROUP_NUMBER'
            
        Raises:
            TypeError: If arguments are not correct types
            ValueError: If group_number is not positive
        """
        # Validation from Project 1 function
        if not isinstance(self._course_code, str) or not isinstance(self._group_number, int):
            raise TypeError("Course code must be string and group number must be integer")
        if self._group_number <= 0:
            raise ValueError("Group number must be positive")
        
        return f"{self._course_code}_GROUP_{self._group_number}"
    
    def add_member(self, student, email: str, phone: str = ''):
        """
        Add a student to the study group.
        
        Args:
            student: Student object to add
            email (str): Contact email for the student
            phone (str, optional): Contact phone number
            
        Raises:
            TypeError: If student is not a Student object
            ValueError: If group is full or student already in group
        """
        # Avoid circular import - check type by duck typing
        if not hasattr(student, 'student_id') or not hasattr(student, 'name'):
            raise TypeError("Must provide a valid Student object")
        
        if len(self._members) >= self._max_members:
            raise ValueError(f"Study group is full (max {self._max_members} members)")
        
        # Check if student already in group
        for member in self._members:
            if member['student'].student_id == student.student_id:
                raise ValueError(f"{student.name} is already in this group")
        
        self._members.append({
            'student': student,
            'email': email.strip(),
            'phone': phone.strip(),
            'join_date': datetime.now().strftime('%Y-%m-%d')
        })
    
    def remove_member(self, student_id: str):
        """
        Remove a member from the study group.
        
        Args:
            student_id (str): Student ID to remove
            
        Raises:
            ValueError: If student not found in group
        """
        for i, member in enumerate(self._members):
            if member['student'].student_id == student_id:
                self._members.pop(i)
                return
        
        raise ValueError(f"Student {student_id} not found in group")
    
    def schedule_meeting(self, date: str, time: str, location: str, agenda: str = ''):
        """
        Schedule a study group meeting.
        
        Args:
            date (str): Meeting date in 'YYYY-MM-DD' format
            time (str): Meeting time (e.g., '3:00 PM')
            location (str): Meeting location
            agenda (str, optional): Meeting agenda/topics
            
        Raises:
            ValueError: If date format is invalid or fields are empty
        """
        # Validate date format
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
        
        if not time.strip():
            raise ValueError("Time cannot be empty")
        if not location.strip():
            raise ValueError("Location cannot be empty")
        
        self._meetings.append({
            'date': date,
            'time': time.strip(),
            'location': location.strip(),
            'agenda': agenda.strip(),
            'scheduled_on': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    def get_members(self) -> List[Dict]:
        """
        Get all group members.
        
        Returns:
            List[Dict]: Copy of member information list
        """
        return self._members.copy()
    
    def get_member_count(self) -> int:
        """
        Get current number of members.
        
        Returns:
            int: Number of members in the group
        """
        return len(self._members)
    
    def is_full(self) -> bool:
        """
        Check if group is at maximum capacity.
        
        Returns:
            bool: True if full, False otherwise
        """
        return len(self._members) >= self._max_members
    
    def get_upcoming_meetings(self) -> List[Dict]:
        """
        Get all upcoming meetings (future dates only).
        
        Returns:
            List[Dict]: Upcoming meetings sorted by date
        """
        today = datetime.now().date()
        upcoming = []
        
        for meeting in self._meetings:
            meeting_date = datetime.strptime(meeting['date'], '%Y-%m-%d').date()
            if meeting_date >= today:
                upcoming.append(meeting)
        
        # Sort by date
        upcoming.sort(key=lambda m: m['date'])
        return upcoming
    
    def get_all_meetings(self) -> List[Dict]:
        """
        Get all meetings (past and future).
        
        Returns:
            List[Dict]: Copy of all meetings
        """
        return self._meetings.copy()
    
    def get_member_by_id(self, student_id: str) -> Dict:
        """
        Get member information by student ID.
        
        Args:
            student_id (str): Student ID to find
            
        Returns:
            Dict: Member information or None if not found
        """
        for member in self._members:
            if member['student'].student_id == student_id:
                return member.copy()
        return None
    
    def __str__(self) -> str:
        """Return a readable string representation."""
        return f"Study Group {self._group_number} for {self._course_code} ({self.get_member_count()}/{self._max_members} members)"
    
    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return (f"StudyGroup(course_code='{self._course_code}', "
                f"group_number={self._group_number}, max_members={self._max_members})")


if __name__ == "__main__":
    # Test the StudyGroup class
    print("=" * 60)
    print("Testing StudyGroup Class")
    print("=" * 60)
    
    # Create study group
    group = StudyGroup('INST326', 1, 5)
    print(f"\n1. Created study group: {group}")
    print(f"   Repr: {repr(group)}")
    print(f"   Group ID: {group.group_id}")
    
    # Test properties
    print("\n2. Test properties:")
    print(f"   Course code: {group.course_code}")
    print(f"   Group number: {group.group_number}")
    print(f"   Max members: {group.max_members}")
    print(f"   Current members: {group.get_member_count()}")
    print(f"   Is full: {group.is_full()}")
    
    # Test description
    print("\n3. Set description:")
    group.description = "Study group for Project 2 collaboration"
    print(f"   Description: {group.description}")
    
    # Test with mock student
    print("\n4. Mock student test:")
    
    class MockStudent:
        def __init__(self, name, student_id):
            self.name = name
            self.student_id = student_id
    
    student1 = MockStudent("Alice Johnson", "UID123")
    student2 = MockStudent("Bob Smith", "UID456")
    
    # Add members
    print("\n5. Add members:")
    group.add_member(student1, "alice@umd.edu", "555-1234")
    group.add_member(student2, "bob@umd.edu", "555-5678")
    print(f"   Members added: {group.get_member_count()}")
    print(f"   Is full: {group.is_full()}")
    
    # Get members
    print("\n6. Get member list:")
    members = group.get_members()
    for member in members:
        print(f"   - {member['student'].name} ({member['email']})")
    
    # Schedule meetings
    print("\n7. Schedule meetings:")
    group.schedule_meeting('2025-11-10', '3:00 PM', 'McKeldin Library', 'Discuss Project 2')
    group.schedule_meeting('2025-11-15', '4:00 PM', 'ESJ 2204', 'Code review session')
    all_meetings = group.get_all_meetings()
    print(f"   Meetings scheduled: {len(all_meetings)}")
    
    # Get upcoming meetings
    print("\n8. Upcoming meetings:")
    upcoming = group.get_upcoming_meetings()
    for meeting in upcoming:
        print(f"   - {meeting['date']} at {meeting['time']}: {meeting['location']}")
        if meeting['agenda']:
            print(f"     Agenda: {meeting['agenda']}")
    
    # Test member lookup
    print("\n9. Find member by ID:")
    found = group.get_member_by_id("UID123")
    if found:
        print(f"   Found: {found['student'].name}")
    
    # Test remove member
    print("\n10. Remove member:")
    group.remove_member("UID456")
    print(f"    Members after removal: {group.get_member_count()}")
    
    # Test error handling
    print("\n11. Test error handling:")
    try:
        invalid_group = StudyGroup("", 1, 5)
    except ValueError as e:
        print(f"    Caught expected error: {e}")
    
    try:
        group.remove_member("NONEXISTENT")
    except ValueError as e:
        print(f"    Caught expected error: {e}")
    
    try:
        group.schedule_meeting('invalid-date', '3PM', 'Library')
    except ValueError as e:
        print(f"    Caught expected error: {e}")
    
    # Test group ID generation with different courses
    print("\n12. Test group ID generation:")
    group2 = StudyGroup('CMSC131', 2, 4)
    print(f"    Group 1 ID: {group.group_id}")
    print(f"    Group 2 ID: {group2.group_id}")
    
    print("\n" + "=" * 60)
    print("All StudyGroup class tests passed!")
    print("=" * 60)
