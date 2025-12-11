"""
Entry point for the Project 4 application.
Runs the course management system using the classes
defined in the src/ directory.
"""

from src.course import Course
from src.student import Student
from src.instructor import Instructor
from src.gradebook import Gradebook


def main():
    print("=== Project 4: Course Management System ===\n")

    # Create example objects
    course = Course("CMSC131", "Introduction to Programming", 4)
    instructor = Instructor("Dr. Smith", "smith@umd.edu", "Computer Science")
    student = Student("Alice Johnson", "alice@umd.edu", "Computer Science")

    # Show information
    print("Created Course:")
    print(course)

    print("\nCreated Instructor:")
    print(instructor)

    print("\nCreated Student:")
    print(student)

    # Gradebook example
    gradebook = Gradebook(course)
    gradebook.add_student(student)
    gradebook.record_grade(student, 92)

    print("\nGradebook Report:")
    print(gradebook.generate_report())

    print("\nProgram finished successfully.")


if __name__ == "__main__":
    main()
