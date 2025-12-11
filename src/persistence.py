import json
import os


class PersistenceManager:
    """
    Handles saving and loading system data (students, courses, instructors, grades)
    using JSON files for simple persistence.
    """

    def __init__(self, file_path="data.json"):
        self.file_path = file_path

    def save(self, data):
        """
        Saves the provided dictionary to the JSON file.
        """
        try:
            with open(self.file_path, "w") as file:
                json.dump(data, file, indent=4)
            print(f"[Persistence] Data saved to {self.file_path}")
        except Exception as e:
            print(f"[Persistence] Error saving file: {e}")

    def load(self):
        """
        Loads and returns the data dictionary from the JSON file.
        If the file does not exist, return an empty dictionary.
        """
        if not os.path.exists(self.file_path):
            print("[Persistence] No data file found. Returning empty dataset.")
            return {}

        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
            print(f"[Persistence] Data loaded from {self.file_path}")
            return data
        except Exception as e:
            print(f"[Persistence] Error loading file: {e}")
            return {}


# Helper functions to convert objects into dicts

def student_to_dict(student):
    return {
        "name": student.name,
        "email": student.email,
        "major": student.major,
        "courses": student.courses  # You may adjust depending on your implementation
    }


def course_to_dict(course):
    return {
        "course_id": course.course_id,
        "title": course.title,
        "credits": course.credits
    }


def instructor_to_dict(instructor):
    return {
        "name": instructor.name,
        "email": instructor.email,
        "department": instructor.department
    }
