"""
Project 3 Feature Demonstration Script
INST326 - Inheritance and Polymorphism

Team: Class Tracker
Members: Kayla Fuentes, Rhea Vyragaram, Jocelyn DeHenzel, Vinindi Withanage

This script demonstrates all key features of Project 3:
- Abstract base classes
- Inheritance hierarchies
- Polymorphic behavior
- Composition relationships
"""

from datetime import datetime, timedelta
from academic_item import AcademicItem
from assignment_types import Assignment, Project, Exam
from academic_planner import AcademicPlanner


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_abstract_base_class():
    """Demonstrate abstract base class enforcement."""
    print_section("1. ABSTRACT BASE CLASS (ABC) DEMONSTRATION")
    
    print("\n📌 Attempting to instantiate abstract class...")
    try:
        # This should fail - cannot instantiate abstract class
        item = AcademicItem('Test', '2025-12-01', 'INST326', 10.0)
        print("   ❌ ERROR: Should not be able to instantiate!")
    except TypeError as e:
        print("   ✓ SUCCESS: Cannot instantiate abstract class")
        print(f"   Error message: {str(e)[:60]}...")
    
    print("\n📌 Abstract methods enforce implementation...")
    print("   - calculate_time_commitment() must be implemented")
    print("   - get_priority() must be implemented")
    print("   - get_item_type() must be implemented")
    
    print("\n📌 All derived classes implement these methods:")
    assignment = Assignment('HW1', '2025-12-01', 'INST326', 10.0, estimated_hours=3.0)
    print(f"   Assignment.calculate_time_commitment() = {assignment.calculate_time_commitment()}h")
    print(f"   Assignment.get_priority() = {assignment.get_priority()}")
    print(f"   Assignment.get_item_type() = {assignment.get_item_type()}")


def demo_inheritance_hierarchy():
    """Demonstrate inheritance relationships."""
    print_section("2. INHERITANCE HIERARCHY DEMONSTRATION")
    
    print("\n📌 Creating instances of derived classes...")
    
    assignment = Assignment('Homework 5', '2025-11-25', 'INST326', 15.0, 
                           estimated_hours=4.0)
    project = Project('Final Project', '2025-12-10', 'INST326', 40.0,
                     num_milestones=3, team_size=4)
    exam = Exam('Midterm Exam', '2025-11-22', 'INST326', 25.0,
               exam_type='midterm', num_chapters=6)
    
    print("   ✓ Assignment created")
    print("   ✓ Project created")
    print("   ✓ Exam created")
    
    print("\n📌 Verifying inheritance relationships...")
    print(f"   Assignment isinstance of AcademicItem: {isinstance(assignment, AcademicItem)}")
    print(f"   Project isinstance of AcademicItem: {isinstance(project, AcademicItem)}")
    print(f"   Exam isinstance of AcademicItem: {isinstance(exam, AcademicItem)}")
    
    print("\n📌 All share common base class properties:")
    for item in [assignment, project, exam]:
        print(f"   - {item.__class__.__name__}: title='{item.title}', "
              f"weight={item.weight}%, status='{item.status}'")
    
    print("\n📌 Each has specialized attributes:")
    print(f"   Assignment: estimated_hours = {assignment.estimated_hours}")
    print(f"   Project: num_milestones = {project.num_milestones}, team_size = {project.team_size}")
    print(f"   Exam: exam_type = '{exam.exam_type}', num_chapters = {exam.num_chapters}")


def demo_polymorphism():
    """Demonstrate polymorphic behavior."""
    print_section("3. POLYMORPHISM DEMONSTRATION")
    
    print("\n📌 Creating a mixed collection of academic items...")
    items = [
        Assignment('Homework 3', '2025-11-25', 'INST326', 10.0, estimated_hours=3.0),
        Project('Web Application', '2025-12-01', 'INST326', 35.0, num_milestones=3, team_size=3),
        Exam('Final Exam', '2025-12-15', 'INST326', 30.0, exam_type='final', num_chapters=10),
        Assignment('Lab Report', '2025-11-28', 'INST314', 15.0, estimated_hours=5.0),
    ]
    
    print(f"   Collection has {len(items)} items of different types")
    
    print("\n📌 POLYMORPHIC METHOD #1: calculate_time_commitment()")
    print("   Same method name, different implementations:\n")
    for item in items:
        hours = item.calculate_time_commitment()
        print(f"   {item.__class__.__name__:12} '{item.title[:20]:20}' → {hours:6.1f} hours")
    
    print("\n   💡 Each type calculates differently:")
    print("      • Assignment: uses estimated_hours directly")
    print("      • Project: (milestones × 15h) ÷ team_size^0.7")
    print("      • Exam: chapters × hours_per_chapter (varies by type)")
    
    print("\n📌 POLYMORPHIC METHOD #2: get_priority()")
    print("   Same method name, type-specific priority logic:\n")
    for item in items:
        priority = item.get_priority()
        print(f"   {item.__class__.__name__:12} '{item.title[:20]:20}' → {priority:8} priority")
    
    print("\n   💡 Different priority algorithms:")
    print("      • Assignment: based on weight + days until due")
    print("      • Project: elevated priority due to complexity")
    print("      • Exam: always high priority when approaching")
    
    print("\n📌 POLYMORPHIC METHOD #3: get_item_type()")
    print("   Type identification:\n")
    for item in items:
        item_type = item.get_item_type()
        print(f"   {item.title[:30]:30} → {item_type}")
    
    print("\n📌 Processing collection polymorphically:")
    total_hours = sum(item.calculate_time_commitment() for item in items)
    print(f"   Total workload across all items: {total_hours:.1f} hours")
    print("   ✓ Same interface works uniformly across all types!")


def demo_composition():
    """Demonstrate composition relationships."""
    print_section("4. COMPOSITION DEMONSTRATION")
    
    print("\n📌 Composition: AcademicPlanner HAS-A collection of items")
    print("   (Not inheritance - planner is NOT a type of academic item)")
    
    planner = AcademicPlanner("Jane Smith")
    print(f"\n   Created: {planner}")
    
    print("\n📌 Adding items to planner (composition in action)...")
    
    items_to_add = [
        Assignment('Homework 5', '2025-11-25', 'INST326', 10.0, estimated_hours=3.0),
        Assignment('Reading Response', '2025-11-27', 'INST314', 5.0, estimated_hours=2.0),
        Project('Final Project', '2025-12-10', 'INST326', 40.0, num_milestones=3, team_size=4),
        Project('Case Study', '2025-12-05', 'INST314', 25.0, num_milestones=2, team_size=2),
        Exam('Midterm', '2025-11-22', 'INST326', 25.0, exam_type='midterm', num_chapters=6),
        Exam('Quiz 3', '2025-11-29', 'INST314', 10.0, exam_type='quiz', num_chapters=2),
    ]
    
    for item in items_to_add:
        planner.add_item(item)
    
    print(f"   ✓ Added {len(items_to_add)} items to planner")
    print(f"   Planner now manages: {len(planner.get_all_items())} academic items")
    
    print("\n📌 Planner uses polymorphism to manage items:")
    
    # Weekly workload (polymorphic calculation)
    print("\n   1. Calculate Weekly Workload (next 2 weeks):")
    workload = planner.calculate_weekly_workload(2)
    for week, hours in workload.items():
        print(f"      {week}: {hours} hours")
    
    # Priority summary (polymorphic priority calculation)
    print("\n   2. Priority Summary:")
    summary = planner.get_priority_summary()
    for priority, count in summary.items():
        if count > 0:
            print(f"      {priority.capitalize():10} priority: {count} items")
    
    # Get items by type
    print("\n   3. Items by Type:")
    for item_type in ['Assignment', 'Project', 'Exam']:
        items = planner.get_items_by_type(item_type)
        print(f"      {item_type}s: {len(items)}")
    
    # Total workload (polymorphic time calculation)
    total = planner.get_total_workload()
    print(f"\n   4. Total Workload: {total} hours")
    
    # Upcoming deadlines
    print("\n   5. Upcoming Deadlines (next 7 days):")
    deadlines = planner.get_upcoming_deadlines(7)
    for deadline in deadlines[:3]:  # Show first 3
        print(f"      {deadline['due_date']}: {deadline['title']} "
              f"({deadline['type']}) - {deadline['hours_needed']}h, "
              f"{deadline['priority']} priority")
    
    print("\n   💡 Why Composition vs Inheritance?")
    print("      ✓ Planner is NOT a type of academic item (no is-a relationship)")
    print("      ✓ Planner HAS items (has-a relationship is appropriate)")
    print("      ✓ Loose coupling - items and planner change independently")
    print("      ✓ Flexible - can hold any AcademicItem subclass")


def demo_specialized_features():
    """Demonstrate type-specific features."""
    print_section("5. SPECIALIZED CLASS FEATURES")
    
    print("\n📌 Assignment-specific features:")
    assignment = Assignment('Project Report', '2025-12-01', 'INST326', 20.0, 
                           estimated_hours=8.0)
    assignment.add_notes("Remember to include UML diagrams")
    assignment.set_instructions("Write 10-page analysis of OOP principles")
    print(f"   Notes: {assignment.get_notes()}")
    print(f"   Instructions: {assignment.get_instructions()[:50]}...")
    
    print("\n📌 Project-specific features:")
    project = Project('Mobile App', '2025-12-15', 'INST326', 45.0,
                     num_milestones=4, team_size=3)
    project.add_milestone('UI Design', '2025-11-20')
    project.add_milestone('Backend API', '2025-11-28')
    project.add_milestone('Integration', '2025-12-05')
    project.add_milestone('Testing', '2025-12-12')
    project.set_repository('https://github.com/team/mobile-app')
    
    print(f"   Milestones: {len(project.get_milestones())}")
    for milestone in project.get_milestones():
        print(f"      - {milestone['title']}: {milestone['due_date']}")
    print(f"   Repository: {project.get_repository()}")
    
    print("\n📌 Exam-specific features:")
    exam = Exam('Comprehensive Final', '2025-12-18', 'INST326', 35.0,
               exam_type='final', num_chapters=12)
    exam.set_study_guide("Review all projects, homeworks, and lecture notes. "
                        "Focus on inheritance, polymorphism, and design patterns.")
    exam.set_location("ESJ 2204")
    
    print(f"   Study Guide: {exam.get_study_guide()[:60]}...")
    print(f"   Location: {exam.get_location()}")
    print(f"   Study Time Needed: {exam.calculate_time_commitment()} hours")


def demo_method_overriding():
    """Demonstrate proper method overriding with super()."""
    print_section("6. METHOD OVERRIDING WITH super()")
    
    print("\n📌 All derived classes use super() to initialize base class:")
    
    print("\n   Example: Creating a Project")
    print("   Code: project = Project('Test', '2025-12-01', 'INST326', 30, ...)")
    print("\n   What happens:")
    print("   1. Project.__init__() called")
    print("   2. super().__init__() calls AcademicItem.__init__()")
    print("   3. Base class attributes initialized (title, due_date, etc.)")
    print("   4. Project-specific attributes initialized (milestones, team_size)")
    
    project = Project('Test Project', '2025-12-01', 'INST326', 30.0,
                     num_milestones=2, team_size=3)
    
    print("\n   Result:")
    print(f"   Base class attribute (title): '{project.title}'")
    print(f"   Base class attribute (weight): {project.weight}%")
    print(f"   Derived class attribute (num_milestones): {project.num_milestones}")
    print(f"   Derived class attribute (team_size): {project.team_size}")
    
    print("\n   ✓ Proper inheritance chain maintained through super()")


def demo_completion_workflow():
    """Demonstrate completing items and tracking progress."""
    print_section("7. COMPLETION WORKFLOW")
    
    print("\n📌 Creating items and tracking completion...")
    
    planner = AcademicPlanner("Alex Johnson")
    
    # Add items
    hw = Assignment('Homework 4', '2025-11-20', 'INST326', 10.0, estimated_hours=3.0)
    proj = Project('Database Project', '2025-11-25', 'INST326', 30.0, 
                   num_milestones=2, team_size=2)
    exam = Exam('Quiz 2', '2025-11-23', 'INST326', 5.0, exam_type='quiz', num_chapters=2)
    
    planner.add_item(hw)
    planner.add_item(proj)
    planner.add_item(exam)
    
    print(f"   Initial stats: {planner}")
    stats = planner.get_completion_stats()
    print(f"   Completion rate: {stats['completion_rate']}%")
    
    print("\n📌 Marking items as completed...")
    
    hw.mark_completed(95.0)
    print(f"   ✓ Completed: {hw.title} - Score: {hw.score}%")
    
    proj.status = 'in_progress'
    print(f"   ⏳ In Progress: {proj.title}")
    
    print("\n📌 Updated statistics:")
    updated_stats = planner.get_completion_stats()
    print(f"   Total items: {updated_stats['total_items']}")
    print(f"   Completed: {updated_stats['completed']}")
    print(f"   In Progress: {updated_stats['in_progress']}")
    print(f"   Not Started: {updated_stats['not_started']}")
    print(f"   Completion rate: {updated_stats['completion_rate']}%")
    print(f"   Average score: {updated_stats['average_score']}%")
    
    print("\n   💡 Completion affects priority:")
    print(f"   Homework priority after completion: {hw.get_priority()} (was high)")


from pathlib import Path
from academic_io import (
    save_planner_to_json,
    load_planner_from_json,
    import_items_from_csv,
    export_deadlines_to_csv,
)


def demo_persistence_and_io():
    """Demonstrate Project 4 persistence, import, and export features."""
    print_section("8. PROJECT 4: DATA PERSISTENCE & I/O DEMONSTRATION")

    planner = AcademicPlanner("Demo Student")

    # Add a couple of items
    planner.add_item(Assignment('HW Persistence', '2025-11-25', 'INST326', 10.0,
                                estimated_hours=3.0))
    planner.add_item(Exam('Final Persistence', '2025-12-15', 'INST326', 30.0,
                          exam_type='final', num_chapters=8))

    # 1. Save planner to JSON
    json_path = Path("demo_data") / "planner_state.json"
    print(f"\n📁 Saving planner to JSON: {json_path}")
    save_planner_to_json(planner, json_path)
    print("   ✓ Planner saved")

    # 2. Load planner from JSON
    print(f"\n📁 Loading planner from JSON: {json_path}")
    loaded_planner = load_planner_from_json(json_path, default_student_name="Loaded Demo")
    print(f"   ✓ Loaded planner with {len(loaded_planner.get_all_items())} items")

    # 3. Import items from CSV (if file exists)
    csv_import_path = Path("demo_data") / "sample_items.csv"
    print(f"\n📥 Importing items from CSV (if present): {csv_import_path}")
    if csv_import_path.exists():
        imported_items = import_items_from_csv(csv_import_path)
        for item in imported_items:
            loaded_planner.add_item(item)
        print(f"   ✓ Imported and added {len(imported_items)} items to loaded planner")
    else:
        print("   ⚠ No CSV found; skipping import demonstration")

    # 4. Export upcoming deadlines to CSV
    csv_export_path = Path("demo_data") / "upcoming_deadlines.csv"
    print(f"\n📤 Exporting upcoming deadlines to CSV: {csv_export_path}")
    export_deadlines_to_csv(loaded_planner, csv_export_path, days_ahead=60)
    print("   ✓ Deadlines exported")

    print("\n   💡 This demonstrates:")
    print("      • JSON save/load of full planner state")
    print("      • CSV import of new items")
    print("      • CSV export of upcoming deadlines")
    print("      • Error-safe I/O using pathlib + with-statements")


def main():
    """Run all demonstrations."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 10 + "PROJECT 3: INHERITANCE & POLYMORPHISM" + " " * 20 + "║")
    print("║" + " " * 20 + "Feature Demonstration" + " " * 27 + "║")
    print("╚" + "=" * 68 + "╝")
    
    print("\nThis demonstration showcases:")
    print("  • Abstract Base Classes (ABC)")
    print("  • Inheritance Hierarchies")
    print("  • Polymorphic Behavior")
    print("  • Composition Relationships")
    print("  • Method Overriding with super()")
    print("  • Specialized Class Features")
    
    # Run all demonstrations
    demo_abstract_base_class()
    demo_inheritance_hierarchy()
    demo_polymorphism()
    demo_composition()
    demo_specialized_features()
    demo_method_overriding()
    demo_completion_workflow()
    demo_persistence_and_io()

    
    # Final summary
    print("\n" + "=" * 70)
    print("  DEMONSTRATION COMPLETE!")
    print("=" * 70)
    
    print("\n✅ Key Accomplishments:")
    print("   • Abstract base class enforces interface")
    print("   • Three derived classes with specialized behavior")
    print("   • Polymorphism enables uniform item processing")
    print("   • Composition provides flexible item management")
    print("   • All classes properly use super() for initialization")
    print("   • Type-specific features enhance functionality")
    
    print("\n📚 For more details, see:")
    print("   • README.md - Quick start and overview")
    print("   • docs/ARCHITECTURE.md - Design decisions and rationale")
    print("   • test_project3.py - Comprehensive test suite")
    
    print("\n" + "=" * 70)
    print("Team: Class Tracker")
    print("Members: Kayla Fuentes, Rhea Vyragaram, Jocelyn DeHenzel, Vinindi Withanage")
    print("Course: INST326 - Object-Oriented Programming")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

