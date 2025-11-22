"""Tests for composition relationships: Student<->Course, Course->tasks, Course->StudyGroup."""

from src.student import Student
from src.course import Course
from src.tasks import Assignment
from src.studygroup import StudyGroup


def test_student_course_enrollment_and_task_assignment():
    s = Student("Sam", "sam@umd.edu", "UID1")
    c = Course("INST326", "Intro to InfoSci")
    s.enroll_course(c)
    assert c in s._courses or c in s.get_courses()
    a = Assignment("HW1", "2025-12-01", "INST326", 10)
    c.add_task(a)
    # composition: course tasks are accessible and can be assigned to students
    s.add_assignment(a)
    assert a in s.get_assignments()
    # study group composition
    g = StudyGroup("INST326", 1, max_members=3)
    c.add_study_group(g)
    assert g in c.get_study_groups()
    # enroll student into study group
    g.add_member(s, contact_email="sam@umd.edu")
    assert any(m["student"].student_id == s.student_id for m in g.get_members())
