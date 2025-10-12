
"""
Class Tracker Function Library
INST326 - Project 01
Team: Class Tracker
Members: Kayla Fuentes, Rhea Vyragaram, Jocelyn DeHenzel, Vinindi Withanage

A comprehensive function library for managing college student schedules,
assignments, courses, and resources.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional, Union
import re


# ============================================================================
# SIMPLE FUNCTIONS (5-10 lines)
# ============================================================================

def validate_email(email: str) -> bool:
    """
    Validate if an email address is in correct format.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if email is valid, False otherwise
        
    Raises:
        TypeError: If email is not a string
    """
    if not isinstance(email, str):
        raise TypeError("Email must be a string")
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def format_course_code(course_code: str) -> str:
    """
    Format a course code to standard uppercase format (e.g., 'inst326' -> 'INST326').
    
    Args:
        course_code (str): Course code to format
        
    Returns:
        str: Formatted course code in uppercase
        
    Raises:
        TypeError: If course_code is not a string
        ValueError: If course_code is empty
    """
    if not isinstance(course_code, str):
        raise TypeError("Course code must be a string")
    if not course_code.strip():
        raise ValueError("Course code cannot be empty")
    return course_code.strip().upper()


def calculate_credits_total(credit_list: List[float]) -> float:
    """
    Calculate total credits from a list of course credits.
    
    Args:
        credit_list (List[float]): List of credit values for courses
        
    Returns:
        float: Total credits
        
    Raises:
        TypeError: If credit_list is not a list or contains non-numeric values
        ValueError: If any credit value is negative
    """
    if not isinstance(credit_list, list):
        raise TypeError("Credit list must be a list")
    for credit in credit_list:
        if not isinstance(credit, (int, float)):
            raise TypeError("All credits must be numeric")
        if credit < 0:
            raise ValueError("Credits cannot be negative")
    return sum(credit_list)


def is_assignment_overdue(due_date: str, current_date: str = None) -> bool:
    """
    Check if an assignment is overdue based on due date.
    
    Args:
        due_date (str): Due date in 'YYYY-MM-DD' format
        current_date (str, optional): Current date in 'YYYY-MM-DD' format. 
                                      Defaults to today.
        
    Returns:
        bool: True if assignment is overdue, False otherwise
        
    Raises:
        ValueError: If date format is invalid
    """
    try:
        due = datetime.strptime(due_date, '%Y-%m-%d')
        current = datetime.strptime(current_date, '%Y-%m-%d') if current_date else datetime.now()
        return current.date() > due.date()
    except ValueError as e:
        raise ValueError(f"Invalid date format. Use YYYY-MM-DD: {e}")


def generate_study_group_id(course_code: str, group_number: int) -> str:
    """
    Generate a unique study group identifier.
    
    Args:
        course_code (str): Course code for the study group
        group_number (int): Group number
        
    Returns:
        str: Unique study group ID
        
    Raises:
        TypeError: If arguments are not correct types
        ValueError: If group_number is not positive
    """
    if not isinstance(course_code, str) or not isinstance(group_number, int):
        raise TypeError("Course code must be string and group number must be integer")
    if group_number <= 0:
        raise ValueError("Group number must be positive")
    return f"{format_course_code(course_code)}_GROUP_{group_number}"


# ============================================================================
# MEDIUM COMPLEXITY FUNCTIONS (15-25 lines)
# ============================================================================

def calculate_assignment_priority(due_date: str, weight: float, 
                                   completion_status: str) -> str:
    """
    Calculate priority level for an assignment based on due date, weight, and status.
    
    Args:
        due_date (str): Due date in 'YYYY-MM-DD' format
        weight (float): Assignment weight/percentage (0-100)
        completion_status (str): Status ('not_started', 'in_progress', 'completed')
        
    Returns:
        str: Priority level ('critical', 'high', 'medium', 'low')
        
    Raises:
        ValueError: If inputs are invalid
    """
    if completion_status == 'completed':
        return 'low'
    
    try:
        due = datetime.strptime(due_date, '%Y-%m-%d')
        days_until_due = (due.date() - datetime.now().date()).days
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")
    
    if not 0 <= weight <= 100:
        raise ValueError("Weight must be between 0 and 100")
    
    if days_until_due < 0:
        return 'critical'
    elif days_until_due <= 2 and weight >= 20:
        return 'critical'
    elif days_until_due <= 5 or weight >= 30:
        return 'high'
    elif days_until_due <= 10 or weight >= 15:
        return 'medium'
    else:
        return 'low'


def parse_meeting_time(time_string: str) -> Dict[str, str]:
    """
    Parse a meeting time string into structured components.
    
    Args:
        time_string (str): Time string (e.g., 'MWF 10:00-10:50' or 'TuTh 2:00PM-3:15PM')
        
    Returns:
        Dict[str, str]: Dictionary with 'days', 'start_time', 'end_time'
        
    Raises:
        ValueError: If time_string format is invalid
    """
    if not isinstance(time_string, str):
        raise TypeError("Time string must be a string")
    
    parts = time_string.strip().split()
    if len(parts) < 2:
        raise ValueError("Time string must include days and time range")
    
    days = parts[0]
    time_range = parts[1]
    
    if '-' not in time_range:
        raise ValueError("Time range must include start and end times separated by '-'")
    
    times = time_range.split('-')
    if len(times) != 2:
        raise ValueError("Invalid time range format")
    
    return {
        'days': days,
        'start_time': times[0].strip(),
        'end_time': times[1].strip()
    }


def filter_assignments_by_status(assignments: List[Dict], 
                                  status: str) -> List[Dict]:
    """
    Filter assignments by completion status.
    
    Args:
        assignments (List[Dict]): List of assignment dictionaries
        status (str): Status to filter by ('completed', 'in_progress', 'not_started')
        
    Returns:
        List[Dict]: Filtered list of assignments
        
    Raises:
        TypeError: If assignments is not a list
        ValueError: If status is invalid
    """
    if not isinstance(assignments, list):
        raise TypeError("Assignments must be a list")
    
    valid_statuses = ['completed', 'in_progress', 'not_started']
    if status not in valid_statuses:
        raise ValueError(f"Status must be one of {valid_statuses}")
    
    filtered = []
    for assignment in assignments:
        if not isinstance(assignment, dict):
            raise TypeError("Each assignment must be a dictionary")
        if assignment.get('status') == status:
            filtered.append(assignment)
    
    return filtered


def calculate_time_until_due(due_date: str) -> Tuple[int, str]:
    """
    Calculate time remaining until an assignment is due.
    
    Args:
        due_date (str): Due date in 'YYYY-MM-DD' format
        
    Returns:
        Tuple[int, str]: (number, unit) where unit is 'days', 'hours', or 'overdue'
        
    Raises:
        ValueError: If date format is invalid
    """
    try:
        due = datetime.strptime(due_date, '%Y-%m-%d')
        now = datetime.now()
        delta = due - now
        
        if delta.total_seconds() < 0:
            days_overdue = abs(delta.days)
            return (days_overdue, 'overdue')
        elif delta.days > 0:
            return (delta.days, 'days')
        else:
            hours = int(delta.total_seconds() / 3600)
            return (hours, 'hours')
    except ValueError as e:
        raise ValueError(f"Invalid date format. Use YYYY-MM-DD: {e}")


def validate_course_data(course_data: Dict) -> Tuple[bool, List[str]]:
    """
    Validate course data dictionary for required fields and correct types.
    
    Args:
        course_data (Dict): Dictionary containing course information
        
    Returns:
        Tuple[bool, List[str]]: (is_valid, list_of_errors)
        
    Raises:
        TypeError: If course_data is not a dictionary
    """
    if not isinstance(course_data, dict):
        raise TypeError("Course data must be a dictionary")
    
    errors = []
    required_fields = ['course_code', 'instructor', 'credits']
    
    for field in required_fields:
        if field not in course_data:
            errors.append(f"Missing required field: {field}")
    
    if 'credits' in course_data:
        if not isinstance(course_data['credits'], (int, float)):
            errors.append("Credits must be numeric")
        elif course_data['credits'] <= 0:
            errors.append("Credits must be positive")
    
    if 'instructor' in course_data and not isinstance(course_data['instructor'], str):
        errors.append("Instructor must be a string")
    
    return (len(errors) == 0, errors)


# ============================================================================
# COMPLEX FUNCTIONS (30+ lines)
# ============================================================================

def generate_weekly_schedule(courses: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Generate a weekly schedule organized by day from course meeting times.
    
    Args:
        courses (List[Dict]): List of course dictionaries with 'course_code', 
                              'meeting_time', 'location' keys
        
    Returns:
        Dict[str, List[Dict]]: Schedule organized by day with course details
        
    Raises:
        TypeError: If courses is not a list or contains invalid data
        ValueError: If course data is missing required fields
    """
    if not isinstance(courses, list):
        raise TypeError("Courses must be a list")
    
    day_mapping = {
        'M': 'Monday', 'Tu': 'Tuesday', 'W': 'Wednesday',
        'Th': 'Thursday', 'F': 'Friday', 'Sa': 'Saturday', 'Su': 'Sunday'
    }
    
    schedule = {day: [] for day in day_mapping.values()}
    
    for course in courses:
        if not isinstance(course, dict):
            raise TypeError("Each course must be a dictionary")
        
        required_fields = ['course_code', 'meeting_time']
        for field in required_fields:
            if field not in course:
                raise ValueError(f"Course missing required field: {field}")
        
        try:
            parsed_time = parse_meeting_time(course['meeting_time'])
            days_str = parsed_time['days']
            
            # Parse day codes (handle M, Tu, W, Th, F, etc.)
            i = 0
            while i < len(days_str):
                if i < len(days_str) - 1 and days_str[i:i+2] in day_mapping:
                    day_code = days_str[i:i+2]
                    i += 2
                elif days_str[i] in day_mapping:
                    day_code = days_str[i]
                    i += 1
                else:
                    i += 1
                    continue
                
                day_name = day_mapping[day_code]
                schedule[day_name].append({
                    'course_code': course['course_code'],
                    'start_time': parsed_time['start_time'],
                    'end_time': parsed_time['end_time'],
                    'location': course.get('location', 'TBA')
                })
        except (ValueError, KeyError) as e:
            raise ValueError(f"Error processing course {course.get('course_code')}: {e}")
    
    return schedule


def calculate_workload_distribution(assignments: List[Dict], 
                                     days_ahead: int = 7) -> Dict[str, float]:
    """
    Calculate workload distribution over the next specified days.
    
    Args:
        assignments (List[Dict]): List of assignment dictionaries with 'due_date',
                                  'estimated_hours', 'status'
        days_ahead (int): Number of days to calculate workload for
        
    Returns:
        Dict[str, float]: Dictionary mapping dates to estimated hours of work
        
    Raises:
        TypeError: If assignments is not a list
        ValueError: If days_ahead is not positive or assignment data is invalid
    """
    if not isinstance(assignments, list):
        raise TypeError("Assignments must be a list")
    if not isinstance(days_ahead, int) or days_ahead <= 0:
        raise ValueError("Days ahead must be a positive integer")
    
    workload = {}
    today = datetime.now().date()
    
    # Initialize workload for each day
    for i in range(days_ahead):
        date = today + timedelta(days=i)
        workload[date.strftime('%Y-%m-%d')] = 0.0
    
    for assignment in assignments:
        if not isinstance(assignment, dict):
            raise TypeError("Each assignment must be a dictionary")
        
        # Skip completed assignments
        if assignment.get('status') == 'completed':
            continue
        
        if 'due_date' not in assignment:
            raise ValueError("Assignment missing required field: due_date")
        
        try:
            due_date = datetime.strptime(assignment['due_date'], '%Y-%m-%d').date()
        except ValueError:
            raise ValueError(f"Invalid due_date format: {assignment.get('due_date')}")
        
        # Only include assignments due within the time window
        if today <= due_date < today + timedelta(days=days_ahead):
            date_key = due_date.strftime('%Y-%m-%d')
            estimated_hours = assignment.get('estimated_hours', 2.0)
            
            if not isinstance(estimated_hours, (int, float)):
                raise ValueError("Estimated hours must be numeric")
            
            workload[date_key] += estimated_hours
    
    return workload


def generate_assignment_reminders(assignments: List[Dict], 
                                   reminder_days: List[int] = [7, 3, 1]) -> List[Dict]:
    """
    Generate reminders for upcoming assignments based on reminder thresholds.
    
    Args:
        assignments (List[Dict]): List of assignment dictionaries with 'title',
                                  'due_date', 'course_code', 'status'
        reminder_days (List[int]): Days before due date to generate reminders
        
    Returns:
        List[Dict]: List of reminder dictionaries with 'assignment', 'due_date',
                    'days_until', 'urgency'
        
    Raises:
        TypeError: If assignments is not a list
        ValueError: If assignment data is invalid
    """
    if not isinstance(assignments, list):
        raise TypeError("Assignments must be a list")
    if not isinstance(reminder_days, list):
        raise TypeError("Reminder days must be a list")
    
    reminders = []
    today = datetime.now().date()
    
    for assignment in assignments:
        if not isinstance(assignment, dict):
            raise TypeError("Each assignment must be a dictionary")
        
        # Skip completed assignments
        if assignment.get('status') == 'completed':
            continue
        
        required_fields = ['title', 'due_date']
        for field in required_fields:
            if field not in assignment:
                raise ValueError(f"Assignment missing required field: {field}")
        
        try:
            due_date = datetime.strptime(assignment['due_date'], '%Y-%m-%d').date()
        except ValueError:
            raise ValueError(f"Invalid due_date format: {assignment.get('due_date')}")
        
        days_until = (due_date - today).days
        
        # Check if assignment is overdue
        if days_until < 0:
            reminders.append({
                'assignment': assignment['title'],
                'course_code': assignment.get('course_code', 'Unknown'),
                'due_date': assignment['due_date'],
                'days_until': days_until,
                'urgency': 'overdue',
                'message': f"OVERDUE: {assignment['title']} was due {abs(days_until)} days ago"
            })
        # Check if assignment falls within any reminder threshold
        elif days_until in reminder_days or days_until == 0:
            urgency = 'critical' if days_until <= 1 else 'high' if days_until <= 3 else 'medium'
            message = f"{assignment['title']} is due "
            message += "today!" if days_until == 0 else f"in {days_until} day(s)"
            
            reminders.append({
                'assignment': assignment['title'],
                'course_code': assignment.get('course_code', 'Unknown'),
                'due_date': assignment['due_date'],
                'days_until': days_until,
                'urgency': urgency,
                'message': message
            })
    
    # Sort reminders by urgency and days until due
    urgency_order = {'overdue': 0, 'critical': 1, 'high': 2, 'medium': 3}
    reminders.sort(key=lambda x: (urgency_order[x['urgency']], x['days_until']))
    
    return reminders


def organize_resources_by_course(resources: List[Dict]) -> Dict[str, Dict[str, List[Dict]]]:
    """
    Organize course resources by course code and resource type.
    
    Args:
        resources (List[Dict]): List of resource dictionaries with 'course_code',
                                'resource_type', 'title', 'url'
        
    Returns:
        Dict[str, Dict[str, List[Dict]]]: Nested dictionary organized by course
                                          and resource type
        
    Raises:
        TypeError: If resources is not a list
        ValueError: If resource data is invalid or missing required fields
    """
    if not isinstance(resources, list):
        raise TypeError("Resources must be a list")
    
    organized = {}
    valid_resource_types = ['textbook', 'article', 'video', 'website', 'document', 'other']
    
    for resource in resources:
        if not isinstance(resource, dict):
            raise TypeError("Each resource must be a dictionary")
        
        required_fields = ['course_code', 'resource_type', 'title']
        for field in required_fields:
            if field not in resource:
                raise ValueError(f"Resource missing required field: {field}")
        
        course_code = format_course_code(resource['course_code'])
        resource_type = resource['resource_type'].lower()
        
        if resource_type not in valid_resource_types:
            raise ValueError(f"Invalid resource_type. Must be one of {valid_resource_types}")
        
        # Initialize nested structure if needed
        if course_code not in organized:
            organized[course_code] = {rtype: [] for rtype in valid_resource_types}
        
        # Add resource to appropriate category
        organized[course_code][resource_type].append({
            'title': resource['title'],
            'url': resource.get('url', ''),
            'notes': resource.get('notes', ''),
            'due_date': resource.get('due_date', '')
        })
    
    return organized


def calculate_grade_projection(assignments: List[Dict], 
                                current_grade: Optional[float] = None) -> Dict[str, Union[float, str]]:
    """
    Calculate projected course grade based on completed and pending assignments.
    
    Args:
        assignments (List[Dict]): List of assignment dictionaries with 'weight',
                                  'status', 'score'
        current_grade (Optional[float]): Current grade percentage if known
        
    Returns:
        Dict[str, Union[float, str]]: Dictionary with projected grade, letter grade,
                                      and analysis
        
    Raises:
        TypeError: If assignments is not a list
        ValueError: If assignment data is invalid
    """
    if not isinstance(assignments, list):
        raise TypeError("Assignments must be a list")
    if current_grade is not None and not isinstance(current_grade, (int, float)):
        raise TypeError("Current grade must be numeric")
    
    total_weight = 0.0
    earned_points = 0.0
    completed_weight = 0.0
    
    for assignment in assignments:
        if not isinstance(assignment, dict):
            raise TypeError("Each assignment must be a dictionary")
        
        if 'weight' not in assignment:
            raise ValueError("Assignment missing required field: weight")
        
        weight = assignment['weight']
        if not isinstance(weight, (int, float)) or weight < 0:
            raise ValueError("Assignment weight must be a non-negative number")
        
        total_weight += weight
        
        if assignment.get('status') == 'completed':
            score = assignment.get('score', 0)
            if not isinstance(score, (int, float)) or not 0 <= score <= 100:
                raise ValueError("Assignment score must be between 0 and 100")
            
            earned_points += (score / 100) * weight
            completed_weight += weight
    
    # Calculate current grade
    if completed_weight > 0:
        current_percentage = (earned_points / completed_weight) * 100
    elif current_grade is not None:
        current_percentage = current_grade
    else:
        current_percentage = 0.0
    
    # Project final grade assuming average performance on remaining work
    remaining_weight = total_weight - completed_weight
    if remaining_weight > 0:
        # Assume current performance continues
        projected_remaining = (current_percentage / 100) * remaining_weight
        projected_percentage = ((earned_points + projected_remaining) / total_weight) * 100
    else:
        projected_percentage = current_percentage
    
    # Determine letter grade
    if projected_percentage >= 90:
        letter_grade = 'A'
    elif projected_percentage >= 80:
        letter_grade = 'B'
    elif projected_percentage >= 70:
        letter_grade = 'C'
    elif projected_percentage >= 60:
        letter_grade = 'D'
    else:
        letter_grade = 'F'
    
    return {
        'current_percentage': round(current_percentage, 2),
        'projected_percentage': round(projected_percentage, 2),
        'letter_grade': letter_grade,
        'completed_weight': round(completed_weight, 2),
        'remaining_weight': round(remaining_weight, 2),
        'total_weight': round(total_weight, 2)
    }

# ============================================================================
# DEMONSTRATION FUNCTIONS
# ============================================================================

def demo_validation_functions():
    """Demonstrate email validation and formatting functions."""
    print(" VALIDATION & FORMATTING DEMO")
    print("=" * 50)
    
    print("\nEmail Validation:")
    print(f"  Valid email: {validate_email('student@umd.edu')}")
    print(f"  Invalid email: {validate_email('not-an-email')}")
    
    print("\nCourse Code Formatting:")
    print(f"  'inst326' formatted: {format_course_code('inst326')}")
    print(f"  'cmsc131' formatted: {format_course_code('cmsc131')}")
    
    print("\nCredit Calculation:")
    credits = [3.0, 4.0, 3.0, 1.0]
    total = calculate_credits_total(credits)
    print(f"  Credits {credits}: Total = {total}")


def demo_assignment_management():
    """Demonstrate assignment tracking and priority functions."""
    print("\n\n ASSIGNMENT MANAGEMENT DEMO")
    print("=" * 50)
    
    print("\nAssignment Priority Calculation:")
    priority1 = calculate_assignment_priority('2025-10-15', 25.0, 'not_started')
    priority2 = calculate_assignment_priority('2025-10-13', 40.0, 'in_progress')
    print(f"  Due 10/15, 25% weight, not started: {priority1}")
    print(f"  Due 10/13, 40% weight, in progress: {priority2}")
    
    print("\nTime Until Due:")
    time_info = calculate_time_until_due('2025-10-15')
    print(f"  Assignment due 10/15: {time_info[0]} {time_info[1]}")
    
    print("\nAssignment Reminders:")
    assignments = [
        {'title': 'Project 1', 'due_date': '2025-10-15', 'course_code': 'INST326', 'status': 'in_progress'},
        {'title': 'Quiz 2', 'due_date': '2025-10-19', 'course_code': 'INST314', 'status': 'not_started'},
        {'title': 'Essay', 'due_date': '2025-10-13', 'course_code': 'ENGL101', 'status': 'not_started'}
    ]
    reminders = generate_assignment_reminders(assignments)
    print(f"  Generated {len(reminders)} reminders")
    for reminder in reminders[:2]:  # Show first 2
        print(f"    - {reminder['message']}")


def demo_schedule_management():
    """Demonstrate schedule generation and time parsing."""
    print("\n\n SCHEDULE MANAGEMENT DEMO")
    print("=" * 50)
    
    print("\nMeeting Time Parsing:")
    parsed1 = parse_meeting_time('MWF 10:00-10:50')
    parsed2 = parse_meeting_time('TuTh 2:00-3:15')
    print(f"  'MWF 10:00-10:50': {parsed1}")
    print(f"  'TuTh 2:00-3:15': {parsed2}")
    
    print("\nWeekly Schedule Generation:")
    courses = [
        {'course_code': 'INST326', 'meeting_time': 'TuTh 2:00-3:15', 'location': 'HBK 0104'},
        {'course_code': 'INST314', 'meeting_time': 'MWF 11:00-11:50', 'location': 'HJP 1104'},
        {'course_code': 'CMSC131', 'meeting_time': 'MWF 9:00-9:50', 'location': 'CSI 2117'}
    ]
    schedule = generate_weekly_schedule(courses)
    print(f"  Total courses: {len(courses)}")
    print(f"  Monday classes: {len(schedule['Monday'])}")
    print(f"  Tuesday classes: {len(schedule['Tuesday'])}")
    print(f"  Wednesday classes: {len(schedule['Wednesday'])}")


def demo_workload_analysis():
    """Demonstrate workload distribution and grade projection."""
    print("\n\n WORKLOAD & GRADE ANALYSIS DEMO")
    print("=" * 50)
    
    print("\nWorkload Distribution (Next 7 Days):")
    assignments = [
        {'title': 'Project 1', 'due_date': '2025-10-15', 'estimated_hours': 5.0, 'status': 'in_progress'},
        {'title': 'Quiz 2', 'due_date': '2025-10-16', 'estimated_hours': 2.0, 'status': 'not_started'},
        {'title': 'Essay', 'due_date': '2025-10-18', 'estimated_hours': 4.0, 'status': 'not_started'}
    ]
    workload = calculate_workload_distribution(assignments, 7)
    print(f"  Assignments tracked: {len(assignments)}")
    total_hours = sum(workload.values())
    print(f"  Total hours upcoming: {total_hours}")
    
    print("\nGrade Projection:")
    grade_assignments = [
        {'weight': 20.0, 'status': 'completed', 'score': 85.0},
        {'weight': 20.0, 'status': 'completed', 'score': 90.0},
        {'weight': 30.0, 'status': 'in_progress', 'score': 0},
        {'weight': 30.0, 'status': 'not_started', 'score': 0}
    ]
    projection = calculate_grade_projection(grade_assignments)
    print(f"  Current grade: {projection['current_percentage']}%")
    print(f"  Projected final grade: {projection['projected_percentage']}% ({projection['letter_grade']})")
    print(f"  Completed: {projection['completed_weight']}% of total")


def demo_resource_organization():
    """Demonstrate resource organization by course and type."""
    print("\n\n RESOURCE ORGANIZATION DEMO")
    print("=" * 50)
    
    resources = [
        {'course_code': 'INST326', 'resource_type': 'textbook', 'title': 'Python Programming', 'url': 'http://example.com'},
        {'course_code': 'INST326', 'resource_type': 'video', 'title': 'OOP Tutorial', 'url': 'http://example.com'},
        {'course_code': 'CMSC131', 'resource_type': 'article', 'title': 'Java Basics', 'url': 'http://example.com'},
        {'course_code': 'INST326', 'resource_type': 'document', 'title': 'Project Guidelines', 'url': 'http://example.com'}
    ]
    
    organized = organize_resources_by_course(resources)
    print(f"\nTotal resources: {len(resources)}")
    print(f"Courses with resources: {len(organized)}")
    
    for course_code in organized:
        total = sum(len(resources) for resources in organized[course_code].values())
        print(f"  {course_code}: {total} resources")


def main():
    """Run all demonstration functions."""
    print("CLASS TRACKER FUNCTION LIBRARY - DEMONSTRATION")
    print("=" * 60)
    print("This demo shows how our function library manages student schedules,")
    print("assignments, workload, grades, and resources.")
    
    demo_validation_functions()
    demo_assignment_management()
    demo_schedule_management()
    demo_workload_analysis()
    demo_resource_organization()
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE!")
    print("This function library provides the foundation for managing")
    print("college student schedules, assignments, courses, and resources.")
    print("=" * 60)


if __name__ == "__main__":
    main()
