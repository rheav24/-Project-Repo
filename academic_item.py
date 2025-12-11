from abc import ABC, abstractmethod
from datetime import datetime

class AcademicItem(ABC):
    def __init__(self, title, due_date, weight):
        self.title = title

        # Convert date string → datetime.date
        try:
            self.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format, expected YYYY-MM-DD")

        if not (0 < weight <= 100):
            raise ValueError("Weight must be between 1 and 100")
        self.weight = weight

    @abstractmethod
    def calculate_time_commitment(self):
        pass

    @abstractmethod
    def get_details(self):
        pass

    def get_item_type(self):
        """Return uppercase class identifier (ASSIGNMENT, PROJECT, EXAM)."""
        return self.__class__.__name__.upper()

    def is_overdue(self):
        """Return True if due date is earlier than today's date."""
        today = datetime.today().date()
        return self.due_date < today
