Project Title: Class Tracker
The Class Tracker is a system that helps college students manage their classes and assignments throughout 
the semester. Some of the features are that it validates email addresses and generates weekly schedules.

Team Members: Jocelyn DeHenzel, Rhea Vyragaram, Vinindi Withanage, Kayla Fuentes
Roles:
Jocelyn DeHenzel- I helped to use AI to create initial functions, created and wrote the README file, and update GitHub commits reguarly. 
Vinindi Withanage - I edited some of the errors in the code.  
Rhea Vyragaram- I helped organize which functions needed to go into the init file. 
Problem Statement: College students often struggle with keeping track of their assignments 
due to outside commitments such as jobs and clubs. 

Installation and setup instructions: This library requires Python 3.6 or higher.

Usage examples for key functions:

# Validate an email address
is_valid = validate_email('student@umd.edu')  # Returns: True

# Format a course code
formatted = format_course_code('inst326')  # Returns: 'INST326'

# Calculate total credits
total = calculate_credits_total([3.0, 4.0, 3.0, 1.0])  # Returns: 11.0

Function library overview and organization: 

Simple Functions
Email Validation - Verify email address formats
Course Code Formatting - Standardize course codes to uppercase
Credit Calculation - Sum total credits from course lists
Assignment Status Checking - Determine if assignments are overdue
Study Group ID Generation - Create unique identifiers for study groups

Medium Complexity Functions
Assignment Priority Calculation - Determine priority levels based on due dates and weights
Meeting Time Parsing - Convert time strings into structured data
Assignment Filtering - Filter assignments by completion status
Time Until Due Calculation - Calculate remaining time for assignments
Course Data Validation - Verify course information integrity

Complex Functions
Weekly Schedule Generation - Create organized schedules from course data
Workload Distribution Analysis - Calculate work hours across upcoming days
Assignment Reminder System - Generate timely reminders for due assignments
Resource Organization - Organize course materials by type and course
Grade Projection Calculator - Project final grades based on completed work

Contribution guidelines for team members:
Everyone should have contributed to the README individually. 
Jocelyn, Rhea, and Vinindi worked together in person to collaborate on creating AI prompts to help write the functions and to upload the functions together. 
