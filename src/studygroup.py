"""StudyGroup class (few small updates for composition)."""

from datetime import datetime
from typing import List, Dict


class StudyGroup:
    """Manages members and meetings for a study group (composition with Student)."""

    def __init__(self, course_code: str, group_number: int, max_members: int = 6):
        if not isinstance(course_code, str) or not course_code.strip():
            raise ValueError("Course code required")
        if not isinstance(group_number, int) or group_number <= 0:
            raise ValueError("Group number must be positive")
        self._course_code = course_code.strip().upper()
        self._group_number = group_number
        self._max_members = int(max_members)
        self._members: List[Dict] = []
        self._meetings: List[Dict] = []
        self._group_id = f"{self._course_code}_GROUP_{self._group_number}"

    @property
    def group_id(self) -> str:
        return self._group_id

    def add_member(self, student, contact_email: str = "", phone: str = ""):
        if not hasattr(student, "student_id"):
            raise TypeError("Invalid student")
        if self.is_full():
            raise ValueError("Study group is full")
        for m in self._members:
            if m["student"].student_id == student.student_id:
                raise ValueError("Student already in group")
        self._members.append({
            "student": student,
            "email": contact_email,
            "phone": phone,
            "joined_on": datetime.now().strftime("%Y-%m-%d")
        })

    def is_full(self) -> bool:
        return len(self._members) >= self._max_members

    def get_members(self) -> List[Dict]:
        return [m.copy() for m in self._members]

    def schedule_meeting(self, date: str, time: str, location: str, agenda: str = ""):
        # validate date
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
        if not time or not location:
            raise ValueError("Time and location required")
        self._meetings.append({
            "date": date,
            "time": time,
            "location": location,
            "agenda": agenda
        })

    def get_upcoming_meetings(self) -> List[Dict]:
        today = datetime.now().date()
        return [m for m in self._meetings if datetime.strptime(m["date"], "%Y-%m-%d").date() >= today]
