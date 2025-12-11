"""
Comprehensive Test Suite for Projects 3 & 4
INST326 - Project 3/4: Inheritance, Polymorphism, Composition, Persistence

Team: Class Tracker
Members: Kayla Fuentes, Rhea Vyragaram, Jocelyn DeHenzel, Vinindi Withanage
"""

import unittest
from datetime import datetime, timedelta
from pathlib import Path
import tempfile
import json
import csv

from academic_item import AcademicItem
from assignment_types import Assignment, Project, Exam
from academic_planner import AcademicPlanner


# ----------------------- ORIGINAL PROJECT 3 TESTS ----------------------- #


class TestAcademicItemAbstract(unittest.TestCase):
    """Test abstract base class enforcement and common methods."""

    def test_cannot_instantiate_abstract_class(self):
        """Test that AcademicItem cannot be instantiated directly."""
        with self.assertRaises(TypeError):
            _ = AcademicItem('Test', '2025-12-01', 'INST326', 10.0)

    def test_abstract_methods_must_be_implemented(self):
        """Test that abstract methods must be implemented in subclasses."""

        class IncompleteItem(AcademicItem):
            def get_item_type(self):
                return "INCOMPLETE"

        with self.assertRaises(TypeError):
            _ = IncompleteItem('Test', '2025-12-01', 'INST326', 10.0)

    def test_common_methods_inherited(self):
        """Test that common methods from base class work in subclasses."""
        assignment = Assignment('Test', '2025-12-01', 'INST326', 10.0)

        self.assertFalse(assignment.is_overdue())
        time_left = assignment.calculate_time_remaining()
        self.assertIsInstance(time_left, tuple)
        self.assertEqual(len(time_left), 2)

        assignment.mark_completed(90.0)
        self.assertTrue(assignment.is_completed())
        self.assertEqual(assignment.score, 90.0)


class TestInheritanceHierarchy(unittest.TestCase):
    """Test inheritance relationships and method overriding."""

    def test_assignment_is_academic_item(self):
        assignment = Assignment('HW1', '2025-12-01', 'INST326', 10.0)
        self.assertIsInstance(assignment, AcademicItem)
        self.assertIsInstance(assignment, Assignment)

    def test_project_is_academic_item(self):
        project = Project('Project 1', '2025-12-01', 'INST326', 30.0)
        self.assertIsInstance(project, AcademicItem)
        self.assertIsInstance(project, Project)

    def test_exam_is_academic_item(self):
        exam = Exam('Midterm', '2025-12-01', 'INST326', 25.0)
        self.assertIsInstance(exam, AcademicItem)
        self.assertIsInstance(exam, Exam)

    def test_subclass_properties_accessible(self):
        assignment = Assignment('Test', '2025-12-01', 'INST326', 10.0)
        self.assertEqual(assignment.title, 'Test')
        self.assertEqual(assignment.due_date, '2025-12-01')
        self.assertEqual(assignment.course_code, 'INST326')
        self.assertEqual(assignment.weight, 10.0)

    def test_method_overriding_with_super(self):
        project = Project('Test Project', '2025-12-01', 'INST326', 40.0,
                          num_milestones=2, team_size=3)
        self.assertEqual(project.title, 'Test Project')
        self.assertEqual(project.weight, 40.0)
        self.assertEqual(project.num_milestones, 2)
        self.assertEqual(project.team_size, 3)


class TestPolymorphism(unittest.TestCase):
    """Test polymorphic behavior across different item types."""

    def test_calculate_time_commitment_polymorphism(self):
        assignment = Assignment('HW1', '2025-12-01', 'INST326', 10.0,
                                estimated_hours=3.0)
        project = Project('Project 1', '2025-12-01', 'INST326', 30.0,
                          num_milestones=3, team_size=1)
        exam = Exam('Midterm', '2025-12-01', 'INST326', 25.0,
                    num_chapters=5)

        self.assertEqual(assignment.calculate_time_commitment(), 3.0)
        self.assertGreater(project.calculate_time_commitment(), 10.0)
        self.assertGreater(exam.calculate_time_commitment(), 5.0)

        self.assertIsInstance(assignment.calculate_time_commitment(), float)
        self.assertIsInstance(project.calculate_time_commitment(), float)
        self.assertIsInstance(exam.calculate_time_commitment(), float)

    def test_get_priority_polymorphism(self):
        due_date = (datetime.now() + timedelta(days=8)).strftime('%Y-%m-%d')
        assignment = Assignment('HW1', due_date, 'INST326', 15.0)
        project = Project('Project', due_date, 'INST326', 30.0)
        exam = Exam('Exam', due_date, 'INST326', 25.0)

        priorities = [assignment.get_priority(),
                      project.get_priority(),
                      exam.get_priority()]

        valid_priorities = ['critical', 'high', 'medium', 'low']
        for priority in priorities:
            self.assertIn(priority, valid_priorities)

    def test_get_item_type_polymorphism(self):
        assignment = Assignment('HW1', '2025-12-01', 'INST326', 10.0)
        project = Project('Project', '2025-12-01', 'INST326', 30.0)
        exam = Exam('Exam', '2025-12-01', 'INST326', 25.0,
                    exam_type='midterm')

        self.assertEqual(assignment.get_item_type(), 'ASSIGNMENT')
        self.assertEqual(project.get_item_type(), 'PROJECT')
        self.assertIn('EXAM', exam.get_item_type())

    def test_polymorphic_list_processing(self):
        items = [
            Assignment('HW1', '2025-12-01', 'INST326', 10.0,
                       estimated_hours=2.0),
            Project('Proj', '2025-12-01', 'INST326', 30.0,
                    num_milestones=2),
            Exam('Exam', '2025-12-01', 'INST326', 25.0,
                 num_chapters=4)
        ]

        total_time = sum(item.calculate_time_commitment() for item in items)
        self.assertGreater(total_time, 0)

        for item in items:
            self.assertIsNotNone(item.get_priority())
            self.assertIsNotNone(item.is_overdue())
            self.assertIsInstance(item, AcademicItem)


class TestComposition(unittest.TestCase):
    """Test composition relationships in AcademicPlanner."""

    def test_planner_has_items(self):
        planner = AcademicPlanner("Test Student")
        assignment = Assignment('HW1', '2025-12-01', 'INST326', 10.0)
        planner.add_item(assignment)

        items = planner.get_all_items()
        self.assertEqual(len(items), 1)
        self.assertIsInstance(items[0], AcademicItem)

    def test_planner_manages_multiple_item_types(self):
        planner = AcademicPlanner("Test Student")
        planner.add_item(Assignment('HW1', '2025-12-01', 'INST326', 10.0))
        planner.add_item(Project('Proj', '2025-12-01', 'INST326', 30.0))
        planner.add_item(Exam('Exam', '2025-12-01', 'INST326', 25.0))

        items = planner.get_all_items()
        self.assertEqual(len(items), 3)
        types = [type(item).__name__ for item in items]
        self.assertIn('Assignment', types)
        self.assertIn('Project', types)
        self.assertIn('Exam', types)

    def test_composition_vs_inheritance_rationale(self):
        planner = AcademicPlanner("Student")
        self.assertNotIsInstance(planner, AcademicItem)

        assignment = Assignment('Test', '2025-12-01', 'INST326', 10.0)
        planner.add_item(assignment)

        self.assertTrue(hasattr(planner, 'calculate_weekly_workload'))
        self.assertTrue(hasattr(planner, 'get_priority_summary'))

        self.assertTrue(hasattr(assignment, 'get_priority'))
        self.assertTrue(hasattr(assignment, 'is_overdue'))

    def test_planner_polymorphic_operations(self):
        planner = AcademicPlanner("Student")
        items = [
            Assignment('HW1', '2025-11-25', 'INST326', 10.0,
                       estimated_hours=2.0),
            Project('Proj', '2025-11-26', 'INST326', 30.0,
                    num_milestones=2),
            Exam('Exam', '2025-11-27', 'INST326', 25.0,
                 num_chapters=3)
        ]
        for item in items:
            planner.add_item(item)

        workload = planner.calculate_weekly_workload(1)
        self.assertIsInstance(workload, dict)

        summary = planner.get_priority_summary()
        self.assertIsInstance(summary, dict)

        total = planner.get_total_workload()
        self.assertGreater(total, 0)


class TestDerivedClassSpecificBehavior(unittest.TestCase):
    """Test specific behaviors of derived classes."""

    def test_assignment_notes_and_instructions(self):
        assignment = Assignment('HW1', '2025-12-01', 'INST326', 10.0)
        assignment.add_notes("Remember to test edge cases")
        assignment.set_instructions("Complete all 15 functions")

        self.assertEqual(assignment.get_notes(),
                         "Remember to test edge cases")
        self.assertEqual(assignment.get_instructions(),
                         "Complete all 15 functions")

    def test_project_milestones(self):
        project = Project('Final Project', '2025-12-10', 'INST326', 40.0,
                          num_milestones=3)
        project.add_milestone('Design', '2025-11-20')
        project.add_milestone('Implementation', '2025-12-01')

        milestones = project.get_milestones()
        self.assertEqual(len(milestones), 2)
        self.assertEqual(milestones[0]['title'], 'Design')

    def test_project_team_size_affects_workload(self):
        solo_project = Project('Solo', '2025-12-01', 'INST326', 30.0,
                               num_milestones=2, team_size=1)
        team_project = Project('Team', '2025-12-01', 'INST326', 30.0,
                               num_milestones=2, team_size=4)

        self.assertLess(
            team_project.calculate_time_commitment(),
            solo_project.calculate_time_commitment()
        )

    def test_exam_study_guide(self):
        exam = Exam('Midterm', '2025-12-01', 'INST326', 25.0)
        exam.set_study_guide("Review chapters 1-5, focus on OOP concepts")
        exam.set_location("ESJ 2204")

        self.assertEqual(
            exam.get_study_guide(),
            "Review chapters 1-5, focus on OOP concepts"
        )
        self.assertEqual(exam.get_location(), "ESJ 2204")

    def test_exam_type_affects_workload(self):
        quiz = Exam('Quiz', '2025-12-01', 'INST326', 5.0,
                    exam_type='quiz', num_chapters=2)
        final = Exam('Final', '2025-12-01', 'INST326', 30.0,
                     exam_type='final', num_chapters=2)

        self.assertLess(
            quiz.calculate_time_commitment(),
            final.calculate_time_commitment()
        )


class TestValidationAndErrorHandling(unittest.TestCase):
    """Test input validation and error handling."""

    def test_invalid_weight_raises_error(self):
        with self.assertRaises(ValueError):
            _ = Assignment('Test', '2025-12-01', 'INST326', -10.0)

        with self.assertRaises(ValueError):
            _ = Assignment('Test', '2025-12-01', 'INST326', 150.0)

    def test_invalid_date_format_raises_error(self):
        with self.assertRaises(ValueError):
            _ = Assignment('Test', '12/01/2025', 'INST326', 10.0)

        with self.assertRaises(ValueError):
            _ = Assignment('Test', '2025-13-01', 'INST326', 10.0)

    def test_planner_rejects_non_academic_items(self):
        planner = AcademicPlanner("Student")

        with self.assertRaises(TypeError):
            planner.add_item("Not an item")

        with self.assertRaises(TypeError):
            planner.add_item({'title': 'Test'})

    def test_project_validates_team_size(self):
        with self.assertRaises(ValueError):
            _ = Project('Test', '2025-12-01', 'INST326', 30.0, team_size=0)

        with self.assertRaises(ValueError):
            _ = Project('Test', '2025-12-01', 'INST326', 30.0, team_size=-1)

    def test_exam_validates_type(self):
        with self.assertRaises(ValueError):
            _ = Exam('Test', '2025-12-01', 'INST326', 25.0,
                     exam_type='invalid')


# -------------------------- PROJECT 4 ADDITIONS ------------------------- #


class TestPlannerPersistenceJSON(unittest.TestCase):
    """Integration tests for save/load JSON (data persistence)."""

    def test_save_and_load_round_trip(self):
        planner = AcademicPlanner("JSON Tester")
        planner.add_item(Assignment("HW JSON", "2025-12-01", "INST326", 10.0,
                                    estimated_hours=3.0))
        planner.add_item(Project("Proj JSON", "2025-12-05", "INST326", 30.0,
                                 num_milestones=2, team_size=2))
        planner.add_item(Exam("Exam JSON", "2025-12-10", "INST326", 25.0,
                              exam_type="final", num_chapters=5))

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "planner.json"
            planner.save_to_json(path)

            # Load into a new planner instance
            loaded = AcademicPlanner("Placeholder")
            loaded.load_from_json(path)

            self.assertEqual(len(loaded.get_all_items()), 3)
            # Roughly same workload (allow floating-point wiggle)
            self.assertAlmostEqual(
                planner.get_total_workload(),
                loaded.get_total_workload(),
                places=2
            )

    def test_load_missing_file_raises(self):
        planner = AcademicPlanner("MissingFile")
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "does_not_exist.json"
            with self.assertRaises(FileNotFoundError):
                planner.load_from_json(path)


class TestPlannerPersistenceCSV(unittest.TestCase):
    """Integration tests for CSV import/export."""

    def test_export_and_import_csv_round_trip(self):
        planner = AcademicPlanner("CSV Tester")
        planner.add_item(
            Assignment("HW CSV", "2025-12-01", "INST326", 10.0,
                       estimated_hours=2.0)
        )
        planner.add_item(
            Exam("Quiz CSV", "2025-12-03", "INST314", 5.0,
                 exam_type="quiz", num_chapters=2)
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "items.csv"
            planner.export_to_csv(path)

            # Basic sanity check on raw CSV
            self.assertTrue(path.exists())
            with path.open("r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            self.assertEqual(len(rows), 2)

            # Import into new planner
            new_planner = AcademicPlanner("CSV Importer")
            imported = new_planner.import_from_csv(path)
            self.assertEqual(imported, 2)
            self.assertEqual(len(new_planner.get_all_items()), 2)


class TestSystemWorkflows(unittest.TestCase):
    """
    System tests: end-to-end workflows combining
    items, planner, and persistence.
    """

    def test_end_to_end_workflow(self):
        """
        Create items → add to planner → compute workload →
        save to JSON → load into new planner → recompute.
        """
        planner = AcademicPlanner("EndToEnd Student")
        planner.add_item(
            Assignment("HW5", "2025-11-25", "INST326", 10.0,
                       estimated_hours=3.0)
        )
        planner.add_item(
            Project("Final Project", "2025-12-10", "INST326", 40.0,
                    num_milestones=3, team_size=4)
        )
        planner.add_item(
            Exam("Midterm", "2025-11-22", "INST326", 25.0,
                 exam_type="midterm", num_chapters=6)
        )

        initial_workload = planner.get_total_workload()
        self.assertGreater(initial_workload, 0)

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "workflow.json"
            planner.save_to_json(path)

            loaded = AcademicPlanner("Loaded")
            loaded.load_from_json(path)

            self.assertEqual(len(loaded.get_all_items()), 3)
            self.assertAlmostEqual(
                initial_workload,
                loaded.get_total_workload(),
                places=2
            )

            # Also check upcoming deadlines + summary run without error
            deadlines = loaded.get_upcoming_deadlines(14)
            self.assertIsInstance(deadlines, list)
            summary = loaded.get_priority_summary()
            self.assertIsInstance(summary, dict)


def run_all_tests():
    """Run all test suites and print results."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    for test_case in [
        TestAcademicItemAbstract,
        TestInheritanceHierarchy,
        TestPolymorphism,
        TestComposition,
        TestDerivedClassSpecificBehavior,
        TestValidationAndErrorHandling,
        TestPlannerPersistenceJSON,
        TestPlannerPersistenceCSV,
        TestSystemWorkflows,
    ]:
        suite.addTests(loader.loadTestsFromTestCase(test_case))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

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
