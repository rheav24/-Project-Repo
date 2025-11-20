"""Utility helper functions for Class Tracker (Project 3)."""

import re
from datetime import datetime
from typing import Tuple


def format_course_code(code: str) -> str:
    """Standardize course code formatting (e.g., 'inst326' -> 'INST326')."""
    if not isinstance(code, str):
        raise TypeError("Course code must be a string")
    if not code.strip():
        raise ValueError("Course code cannot be empty")
    return code.strip().upper()


def validate_email(email: str) -> bool:
    """Return True if email looks valid (basic check)."""
    if not isinstance(email, str):
        raise TypeError("Email must be a string")
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def parse_date_iso(date_str: str) -> datetime:
    """Parse ISO date 'YYYY-MM-DD' into datetime (raises ValueError on bad format)."""
    return datetime.strptime(date_str, "%Y-%m-%d")


def hours_between(start_time: str, end_time: str) -> float:
    """Simple HH:MM (or H:MM) difference in hours; supports optional AM/PM tokens."""
    def norm(t: str):
        t = t.strip()
        # remove AM/PM for numeric parse (naive)
        has_pm = 'PM' in t.upper()
        has_am = 'AM' in t.upper()
        t = t.upper().replace('AM', '').replace('PM', '').strip()
        parts = t.split(':')
        hour = int(parts[0])
        minute = int(parts[1]) if len(parts) > 1 else 0
        if has_pm and hour != 12:
            hour += 12
        if has_am and hour == 12:
            hour = 0
        return hour + minute / 60.0

    return max(0.0, norm(end_time) - norm(start_time))

