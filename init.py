"""
Class Tracker Function Library

A comprehensive Python library for college student schedule and assignment
management, providing utilities for assignment tracking, course management,
resource organization, and academic planning.

This library serves as the foundation for the Class Tracker project in INST326,
demonstrating professional function library development with proper
documentation, error handling, and team collaboration practices.

Author: Team Class Tracker
Course: Object-Oriented Programming for Information Science
Institution: University of Maryland, College Park
Team Members: Kayla Fuentes, Rhea Vyragaram, Jocelyn DeHenzel, Vinindi Withanage
"""

# Package metadata
__version__ = "1.0.0"
__author__ = "Team Class Tracker (Kayla Fuentes, Rhea Vyragaram, Jocelyn DeHenzel, Vinindi Withanage)"
__email__ = "classracker@umd.edu"
__description__ = "Class Tracker Function Library for INST326"
__license__ = "MIT"

# Import main functions for easy access
from library_name import (
    # Simple Utility Functions
    validate_email,
    format_course_code,
    calculate_credits_total,
    is_assignment_overdue,
    generate_study_group_id,
    
    # Medium Complexity Functions
    calculate_assignment_priority,
    parse_meeting_time,
    filter_assignments_by_status,
    calculate_time_until_due,
    validate_course_data,
    
    # Complex Analysis Functions
    generate_weekly_schedule,
    calculate_workload_distribution,
    generate_assignment_reminders,
    organize_resources_by_course,
    calculate_grade_projection
)

# Define what gets imported with "from class_tracker import *"
__all__ = [
    # Simple Utilities
    'validate_email',
    'format_course_code',
    'calculate_credits_total',
    'is_assignment_overdue',
    'generate_study_group_id',
    
    # Medium Complexity
    'calculate_assignment_priority',
    'parse_meeting_time',
    'filter_assignments_by_status',
    'calculate_time_until_due',
    'validate_course_data',
    
    # Complex Functions
    'generate_weekly_schedule',
    'calculate_workload_distribution',
    'generate_assignment_reminders',
    'organize_resources_by_course',
    'calculate_grade_projection'
]

# Convenience function groupings for easier access
VALIDATION_FUNCTIONS = [
    'validate_email',
    'format_course_code',
    'validate_course_data'
]

ASSIGNMENT_FUNCTIONS = [
    'calculate_assignment_priority',
    'filter_assignments_by_status',
    'calculate_time_until_due',
    'is_assignment_overdue',
    'generate_assignment_reminders'
]

SCHEDULE_FUNCTIONS = [
    'generate_weekly_schedule',
    'parse_meeting_time',
    'calculate_workload_distribution'
]

COURSE_FUNCTIONS = [
    'format_course_code',
    'calculate_credits_total',
    'validate_course_data'
]

RESOURCE_FUNCTIONS = [
    'organize_resources_by_course'
]

GRADE_FUNCTIONS = [
    'calculate_grade_projection'
]

COLLABORATION_FUNCTIONS = [
    'generate_study_group_id'
]


