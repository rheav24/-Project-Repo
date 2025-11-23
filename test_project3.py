"""
Comprehensive Test Suite for Project 3
INST326 - Project 3: Inheritance and Polymorphism

Team: Class Tracker
Members: Kayla Fuentes, Rhea Vyragaram, Jocelyn DeHenzel, Vinindi Withanage

This module contains comprehensive tests for:
- Abstract base classes
- Inheritance hierarchies
- Polymorphic behavior
- Composition relationships
"""

import unittest
from datetime import datetime, timedelta
from academic_item import AcademicItem
from assignment_types import Assignment, Project, Exam
from academic_planner import AcademicPlanner


class TestAcademicItemAbstract(unittest.TestCase):
    """Test abstract base class enforcement and common methods."""
    
    def test_cannot_instantiate_abstract_class(self):
        """Test that AcademicItem cannot be instantiated directly."""
        with self.assertRaises(TypeError):
            item = AcademicItem('Test', '2025-12-01', 'INST326', 10.0)
    
    def test_abstract_methods_must_be_implemented(self):
        """Test that abstract methods must be implemented in subclasses."""
        # Create incomplete subclass
        class IncompleteItem(AcademicItem):
            def get_item_type(self):
                return "INCOMPLETE"
        
        # Should raise TypeError because abstract methods not implemented
        with self.assertRaises(TypeError):
            item = IncompleteItem('Test', '2025-12-01', 'INST326', 10.0)
    
    def test_common_methods_inherited(self):
        """Test that common methods from base class work in subclasses."""
        assignment = Assignment('Test', '2025-12-01', 'INST326', 10.0)
        
        # Test inherited is_overdue method
        self.assertFalse(assignment.is_overdue())
        
        # Test inherited calculate_time_remaining
        time_left = assignment.calculate_time_remaining()
        self.assertIsInstance(time_left, tuple)
        self.assertEqual(len(time_left), 2)
        
        # Test inherited mark_completed
        assignment.mark_completed(90.0)
        self.assertTrue(assignment.is_completed())
        self.assertEqual(assignment.score, 90.0)


class TestInheritanceHierarchy(unittest.TestCase):
    """Test inheritance relationships and method overriding."""
    
    def test_assignment_is_academic_item(self):
        """Test that Assignment is an instance of AcademicItem."""
        assignment = Assignment('HW1', '2025-12-01', 'INST326', 10.0)
        self.assertIsInstance(assignment, AcademicItem)
        self.assertIsInstance(assignment, Assignment)
    
    def test_project_is_academic_item(self):
        """Test that Project is an instance of AcademicItem."""
        project = Project('Project 1', '2025-12-01', 'INST326', 30.0)
        self.assertIsInstance(project, AcademicItem)
        self.assertIsInstance(project, Project)
    
    def test_exam_is_academic_item(self):
        """Test that Exam is an instance of AcademicItem."""
        exam = Exam('Midterm', '2025-12-01', 'INST326', 25.0)
        self.assertIsInstance(exam, AcademicItem)
        self.assertIsInstance(exam, Exam)
    
    def test_subclass_properties_accessible(self):
        """Test that base class properties work in subclasses."""
        assignment = Assignment('Test', '2025-12-01', 'INST326', 10.0)
        
        self.assertEqual(assignment.title, 'Test')
        self.assertEqual(assignment.due_date, '2025-12-01')
        self.assertEqual(assignment.course_code, 'INST326')
        self.assertEqual(assignment.weight, 10.0)
    
    def test_method_overriding_with_super(self):
        """Test that subclasses properly use super() in constructors."""
        project = Project('Test Project', '2025-12-01', 'INST326', 40.0,
                         num_milestones=2, team_size=3)
        
        # Base class attributes should be set via super()
        self.assertEqual(project.title, 'Test Project')
        self.assertEqual(project.weight, 40.0)
        
        # Subclass-specific attributes
        self.assertEqual(project.num_milestones, 2)
        self.assertEqual(project.team_size, 3)


class TestPolymorphism(unittest.TestCase):
    """Test polymorphic behavior across different item types."""
    
    def test_calculate_time_commitment_polymorphism(self):
        """Test that different types calculate time commitment differently."""
        assignment = Assignment('HW1', '2025-12-01', 'INST326', 10.0, 
                              estimated_hours=3.0)
        project = Project('Project 1', '2025-12-01', 'INST326', 30.0,
                         num_milestones=3, team_size=1)
        exam = Exam('Midterm', '2025-12-01', 'INST326', 25.0,
                   num_chapters=5)
        
        # Each calculates differently
        self.assertEqual(assignment.calculate_time_commitment(), 3.0)
        self.assertGreater(project.calculate_time_commitment(), 10.0)
        self.assertGreater(exam.calculate_time_commitment(), 5.0)
        
        # But all return float
        self.assertIsInstance(assignment.calculate_time_commitment(), float)
        self.assertIsInstance(project.calculate_time_commitment(), float)
        self.assertIsInstance(exam.calculate_time_commitment(), float)
    
    def test_get_priority_polymorphism(self):
        """Test that different types calculate priority differently."""
        # Create items with same due date but different types
        due_date = (datetime.now() + timedelta(days=8)).strftime('%Y-%m-%d')
        
        assignment = Assignment('HW1', due_date, 'INST326', 15.0)
        project = Project('Project', due_date, 'INST326', 30.0)
        exam = Exam('Exam', due_date, 'INST326', 25.0)
        
        # Each should potentially calculate different priorities
        # (based on their specific logic)
        priorities = [
            assignment.get_priority(),
            project.get_priority(),
            exam.get_priority()
        ]
        
        # All should return valid priority strings
        valid_priorities = ['critical', 'high', 'medium', 'low']
        for priority in priorities:
            self.assertIn(priority, valid_priorities)
    
    def test_get_item_type_polymorphism(self):
        """Test that each type returns different item type string."""
        assignment = Assignment('HW1', '2025-12-01', 'INST326', 10.0)
        project = Project('Project', '2025-12-01', 'INST326', 30.0)
        exam = Exam('Exam', '2025-12-01', 'INST326', 25.0, exam_type='midterm')
        
        self.assertEqual(assignment.get_item_type(), 'ASSIGNMENT')
        self.assertEqual(project.get_item_type(), 'PROJECT')
        self.assertIn('EXAM', exam.get_item_type())
    
    def test_polymorphic_list_processing(self):
        """Test processing different types through common interface."""
        items = [
            Assignment('HW1', '2025-12-01', 'INST326', 10.0, estimated_hours=2.0),
            Project('Proj', '2025-12-01', 'INST326', 30.0, num_milestones=2),
            Exam('Exam', '2025-12-01', 'INST326', 25.0, num_chapters=4)
        ]
        
        # Can iterate and call same methods on all
        total_time = sum(item.calculate_time_commitment() for item in items)
        self.assertGreater(total_time, 0)
        
        # Can call any base class method
        for item in items:
            self.assertIsNotNone(item.get_priority())
            self.assertIsNotNone(item.is_overdue())
            self.assertIsInstance(item, AcademicItem)


class TestComposition(unittest.TestCase):
    """Test composition relationships in AcademicPlanner."""
    
    def test_planner_has_items(self):
        """Test that planner contains items (has-a relationship)."""
        planner = AcademicPlanner("Test Student")
        
        assignment = Assignment('HW1', '2025-12-01', 'INST326', 10.0)
        planner.add_item(assignment)
        
        items = planner.get_all_items()
        self.assertEqual(len(items), 1)
        self.assertIsInstance(items[0], AcademicItem)
    
    def test_planner_manages_multiple_item_types(self):
        """Test that planner can hold different item types."""
        planner = AcademicPlanner("Test Student")
        
        planner.add_item(Assignment('HW1', '2025-12-01', 'INST326', 10.0))
        planner.add_item(Project('Proj', '2025-12-01', 'INST326', 30.0))
        planner.add_item(Exam('Exam', '2025-12-01', 'INST326', 25.0))
        
        items = planner.get_all_items()
        self.assertEqual(len(items), 3)
        
        # Different types coexist
        types = [type(item).__name__ for item in items]
        self.assertIn('Assignment', types)
        self.assertIn('Project', types)
        self.assertIn('Exam', types)
    
    def test_composition_vs_inheritance_rationale(self):
        """
        Test that demonstrates why composition was chosen over inheritance.
        
        A planner is NOT a type of academic item - it manages them.
        This is a clear "has-a" relationship, not "is-a".
        """
        planner = AcademicPlanner("Student")
        
        # Planner is NOT an academic item
        self.assertNotIsInstance(planner, AcademicItem)
        
        # But it contains academic items
        assignment = Assignment('Test', '2025-12-01', 'INST326', 10.0)
        planner.add_item(assignment)
        
        # Planner provides different functionality than items
        # It aggregates and analyzes, doesn't have due dates or priorities itself
        self.assertTrue(hasattr(planner, 'calculate_weekly_workload'))
        self.assertTrue(hasattr(planner, 'get_priority_summary'))
        
        # Items have their own behavior
        self.assertTrue(hasattr(assignment, 'get_priority'))
        self.assertTrue(hasattr(assignment, 'is_overdue'))
    
    def test_planner_polymorphic_operations(self):
        """Test that planner operations work polymorphically with all item types."""
        planner = AcademicPlanner("Student")
        
        # Add different types
        items = [
            Assignment('HW1', '2025-11-25', 'INST326', 10.0, estimated_hours=2.0),
            Project('Proj', '2025-11-26', 'INST326', 30.0, num_milestones=2),
            Exam('Exam', '2025-11-27', 'INST326', 25.0, num_chapters=3)
        ]
        
        for item in items:
            planner.add_item(item)
        
        # Workload calculation works polymorphically
        workload = planner.calculate_weekly_workload(1)
        self.assertIsInstance(workload, dict)
        
        # Priority summary works polymorphically
        summary = planner.get_priority_summary()
        self.assertIsInstance(summary, dict)
        
        # Total workload sums polymorphically
        total = planner.get_total_workload()
        self.assertGreater(total, 0)


class TestDerivedClassSpecificBehavior(unittest.TestCase):
    """Test specific behaviors of derived classes."""
    
    def test_assignment_notes_and_instructions(self):
        """Test Assignment-specific features."""
        assignment = Assignment('HW1', '2025-12-01', 'INST326', 10.0)
        
        assignment.add_notes("Remember to test edge cases")
        assignment.set_instructions("Complete all 15 functions")
        
        self.assertEqual(assignment.get_notes(), "Remember to test edge cases")
        self.assertEqual(assignment.get_instructions(), "Complete all 15 functions")
    
    def test_project_milestones(self):
        """Test Project-specific milestone features."""
        project = Project('Final Project', '2025-12-10', 'INST326', 40.0,
                         num_milestones=3)
        
        project.add_milestone('Design', '2025-11-20')
        project.add_milestone('Implementation', '2025-12-01')
        
        milestones = project.get_milestones()
        self.assertEqual(len(milestones), 2)
        self.assertEqual(milestones[0]['title'], 'Design')
    
    def test_project_team_size_affects_workload(self):
        """Test that team size affects project workload calculation."""
        solo_project = Project('Solo', '2025-12-01', 'INST326', 30.0,
                              num_milestones=2, team_size=1)
        team_project = Project('Team', '2025-12-01', 'INST326', 30.0,
                              num_milestones=2, team_size=4)
        
        # Team project should have less individual workload
        self.assertLess(
            team_project.calculate_time_commitment(),
            solo_project.calculate_time_commitment()
        )
    
    def test_exam_study_guide(self):
        """Test Exam-specific study guide features."""
        exam = Exam('Midterm', '2025-12-01', 'INST326', 25.0)
        
        exam.set_study_guide("Review chapters 1-5, focus on OOP concepts")
        exam.set_location("ESJ 2204")
        
        self.assertEqual(exam.get_study_guide(), 
                        "Review chapters 1-5, focus on OOP concepts")
        self.assertEqual(exam.get_location(), "ESJ 2204")
    
    def test_exam_type_affects_workload(self):
        """Test that exam type affects time commitment calculation."""
        quiz = Exam('Quiz', '2025-12-01', 'INST326', 5.0, 
                   exam_type='quiz', num_chapters=2)
        final = Exam('Final', '2025-12-01', 'INST326', 30.0,
                    exam_type='final', num_chapters=2)
        
        # Finals require more study time per chapter
        self.assertLess(
            quiz.calculate_time_commitment(),
            final.calculate_time_commitment()
        )


class TestValidationAndErrorHandling(unittest.TestCase):
    """Test input validation and error handling."""
    
    def test_invalid_weight_raises_error(self):
        """Test that invalid weight values raise ValueError."""
        with self.assertRaises(ValueError):
            Assignment('Test', '2025-12-01', 'INST326', -10.0)
        
        with self.assertRaises(ValueError):
            Assignment('Test', '2025-12-01', 'INST326', 150.0)
    
    def test_invalid_date_format_raises_error(self):
        """Test that invalid date formats raise ValueError."""
        with self.assertRaises(ValueError):
            Assignment('Test', '12/01/2025', 'INST326', 10.0)
        
        with self.assertRaises(ValueError):
            Assignment('Test', '2025-13-01', 'INST326', 10.0)
    
    def test_planner_rejects_non_academic_items(self):
        """Test that planner only accepts AcademicItem instances."""
        planner = AcademicPlanner("Student")
        
        with self.assertRaises(TypeError):
            planner.add_item("Not an item")
        
        with self.assertRaises(TypeError):
            planner.add_item({'title': 'Test'})
    
    def test_project_validates_team_size(self):
        """Test that project validates team size."""
        with self.assertRaises(ValueError):
            Project('Test', '2025-12-01', 'INST326', 30.0, team_size=0)
        
        with self.assertRaises(ValueError):
            Project('Test', '2025-12-01', 'INST326', 30.0, team_size=-1)
    
    def test_exam_validates_type(self):
        """Test that exam validates exam type."""
        with self.assertRaises(ValueError):
            Exam('Test', '2025-12-01', 'INST326', 25.0, exam_type='invalid')


def run_all_tests():
    """Run all test suites and print results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAcademicItemAbstract))
    suite.addTests(loader.loadTestsFromTestCase(TestInheritanceHierarchy))
    suite.addTests(loader.loadTestsFromTestCase(TestPolymorphism))
    suite.addTests(loader.loadTestsFromTestCase(TestComposition))
    suite.addTests(loader.loadTestsFromTestCase(TestDerivedClassSpecificBehavior))
    suite.addTests(loader.loadTestsFromTestCase(TestValidationAndErrorHandling))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)
