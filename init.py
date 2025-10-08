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

def get_function_categories():
    """Get a dictionary of function categories and their functions.
    
    Returns:
        Dict[str, List[str]]: Dictionary mapping category names to function lists
        
    Example:
        >>> categories = get_function_categories()
        >>> print(categories['assignment'])
        ['calculate_assignment_priority', 'filter_assignments_by_status', ...]
    """
    return {
        'validation': VALIDATION_FUNCTIONS,
        'assignment': ASSIGNMENT_FUNCTIONS,
        'schedule': SCHEDULE_FUNCTIONS,
        'course': COURSE_FUNCTIONS,
        'resource': RESOURCE_FUNCTIONS,
        'grade': GRADE_FUNCTIONS,
        'collaboration': COLLABORATION_FUNCTIONS
    }

def list_all_functions():
    """List all available functions in the library.
    
    Returns:
        List[str]: Alphabetically sorted list of all function names
        
    Example:
        >>> functions = list_all_functions()
        >>> print(f"Total functions: {len(functions)}")
        Total functions: 15
    """
    return sorted(__all__)

def get_library_info():
    """Get library metadata and information.
    
    Returns:
        Dict[str, str]: Dictionary with library information
        
    Example:
        >>> info = get_library_info()
        >>> print(f"Version: {info['version']}")
        Version: 1.0.0
    """
    return {
        'name': 'Class Tracker Function Library',
        'version': __version__,
        'author': __author__,
        'description': __description__,
        'total_functions': len(__all__),
        'categories': list(get_function_categories().keys()),
        'license': __license__
    }

# Quick usage example for interactive help
def quick_start():
    """Display quick start information for new users.
    
    Example:
        >>> import class_tracker
        >>> class_tracker.quick_start()
    """
    print("📚 Class Tracker Function Library - Quick Start")
    print("=" * 60)
    print()
    print("This library provides 15 functions for student academic management:")
    print()
    
    categories = get_function_categories()
    for category, functions in categories.items():
        print(f"📋 {category.title()} Functions ({len(functions)}):")
        for func in functions:
            print(f"   • {func}")
        print()
    
    print("💡 Quick Examples:")
    print()
    print("   # Validate student email")
    print("   >>> valid = validate_email('student@umd.edu')")
    print("   >>> print(f'Valid email: {valid}')")
    print()
    print("   # Calculate assignment priority")
    print("   >>> priority = calculate_assignment_priority('2025-10-15', 25.0, 'not_started')")
    print("   >>> print(f'Priority level: {priority}')")
    print()
    print("   # Generate weekly schedule")
    print("   >>> courses = [")
    print("   ...     {'course_code': 'INST326', 'meeting_time': 'TuTh 2:00-3:15', 'location': 'HBK 0104'}")
    print("   ... ]")
    print("   >>> schedule = generate_weekly_schedule(courses)")
    print("   >>> print(f'Tuesday classes: {len(schedule[\"Tuesday\"])}')")
    print()
    print("   # Get assignment reminders")
    print("   >>> assignments = [")
    print("   ...     {'title': 'Project 1', 'due_date': '2025-10-10', 'course_code': 'INST326', 'status': 'in_progress'}")
    print("   ... ]")
    print("   >>> reminders = generate_assignment_reminders(assignments)")
    print("   >>> for reminder in reminders:")
    print("   ...     print(reminder['message'])")
    print()
    print("   # Calculate grade projection")
    print("   >>> assignments = [")
    print("   ...     {'weight': 20, 'status': 'completed', 'score': 95},")
    print("   ...     {'weight': 30, 'status': 'completed', 'score': 88}")
    print("   ... ]")
    print("   >>> projection = calculate_grade_projection(assignments)")
    print("   >>> print(f'Projected Grade: {projection[\"letter_grade\"]}')")
    print()
    print("📚 For detailed documentation, see function docstrings")
    print("🎯 Run example usage with: python -m class_tracker_library")
    print()
    print("👥 Team Members:")
    print("   • Kayla Fuentes - Documentation Manager")
    print("   • Rhea Vyragaram - Project Analyst")
    print("   • Jocelyn DeHenzel - Project Coordinator")
    print("   • Vinindi Withanage - Quality Testing")


if __name__ == "__main__":
    # If someone runs "python -m class_tracker", show quick start
    quick_start()
