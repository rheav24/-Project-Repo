"""Small integration examples showing polymorphism and composition usage."""

from src.tasks import Assignment, Exam
from src.student import Student
from src.course import Course


def test_example_workflow():
    student = Student("Alex", "alex@umd.edu", "UID10")
    course = Course("INST326", "Programming Foundations")
    student.enroll_course(course)
    hw = Assignment("Lab", "2025-12-05", "INST326", 5)
    exam = Exam("Final", "2025-12-10", "INST326", 40)
    course.add_task(hw)
    course.add_task(exam)
    student.add_assignment(hw)
    student.add_assignment(exam)
    # polymorphism: same method works on both
    priorities = [t.get_priority() for t in student.get_assignments()]
    assert len(priorities) == 2
