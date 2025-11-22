"""Schedule class (uses course.parse_meeting_schedule via composition)."""

from typing import Dict, List, Tuple


class Schedule:
    """Student schedule — generates weekly view from student's enrolled courses."""

    def __init__(self, student):
        # duck-typing: student must have get_courses() and name
        if not hasattr(student, "get_courses") or not hasattr(student, "name"):
            raise TypeError("Must provide a valid Student object")
        self._student = student
        self._day_mapping = {
            "M": "Monday", "Tu": "Tuesday", "W": "Wednesday",
            "Th": "Thursday", "F": "Friday", "Sa": "Saturday", "Su": "Sunday"
        }

    def generate_weekly_view(self) -> Dict[str, List[Dict]]:
        schedule = {day: [] for day in self._day_mapping.values()}
        courses = self._student.get_courses()
        if not isinstance(courses, list):
            raise TypeError("Student.get_courses() must return a list")
        for course in courses:
            if not hasattr(course, "parse_meeting_schedule"):
                continue
            try:
                parsed = course.parse_meeting_schedule()
                days_str = parsed["days"]
                i = 0
                while i < len(days_str):
                    # handle 2-letter codes first
                    if i < len(days_str) - 1 and days_str[i:i+2] in self._day_mapping:
                        day_code = days_str[i:i+2]
                        i += 2
                    elif days_str[i] in self._day_mapping:
                        day_code = days_str[i]
                        i += 1
                    else:
                        i += 1
                        continue
                    dn = self._day_mapping[day_code]
                    schedule[dn].append({
                        "course_code": course.course_code,
                        "start_time": parsed["start_time"],
                        "end_time": parsed["end_time"],
                        "location": getattr(course, "location", "TBA")
                    })
            except Exception:
                # ignore invalid meeting entries
                continue
        return schedule

    def get_classes_on_day(self, day: str) -> List[Dict]:
        weekly = self.generate_weekly_view()
        if day not in weekly:
            raise ValueError(f"Invalid day. Expected one of: {list(weekly.keys())}")
        return weekly[day]

    def has_time_conflict(self) -> Tuple[bool, List[str]]:
        conflicts = []
        weekly = self.generate_weekly_view()
        for day, cls_list in weekly.items():
            if len(cls_list) < 2:
                continue
            sorted_classes = sorted(cls_list, key=lambda x: x["start_time"])
            for i in range(len(sorted_classes) - 1):
                cur = sorted_classes[i]
                nxt = sorted_classes[i+1]
                # naive string compare works for HH:MM with same formatting
                if cur["end_time"] > nxt["start_time"]:
                    conflicts.append(f"{day}: {cur['course_code']} overlaps with {nxt['course_code']}")
        return (len(conflicts) > 0, conflicts)
