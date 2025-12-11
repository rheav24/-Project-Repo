# test_project4_persistence.py
"""
Project 4 Test Suite: Persistence, Import/Export, and End-to-End Workflows.

Covers:
- Unit tests for academic_io helpers
- Integration tests across AcademicPlanner + AcademicItem types + I/O
- System tests for full workflows (import -> planner -> export)
"""

import os
import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timedelta

from assignment import Assignment, Project, Exam
from academic_planner import AcademicPlanner
from academic_io import (
    save_planner_to_json,
    load_planner_from_json,
    import_items_from_csv,
    export_deadlines_to_csv,
)


class TestPersistenceUnit(unittest.TestCase):
    """Unit tests focused on academic_io behavior itself."""

    def test_save_and_load_empty_planner(self):
        planner = AcademicPlanner("Empty Student")

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "planner.json"
            save_planner_to_json(planner, path)
            self.assertTrue(path.exists())

            loaded = load_planner_from_json(path)
            self.assertEqual(len(loaded.get_all_items()), 0)

    def test_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            load_planner_from_json("nonexistent_planner.json")

    def test_corrupted_json_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "bad.json"
            path.write_text("{ this is not valid json", encoding="utf-8")

            with self.assertRaises(ValueError):
                load_planner_from_json(path)


class TestIntegrationPlannerIO(unittest.TestCase):
    """Integration tests: Planner + items + I/O working together."""

    def _build_sample_planner(self) -> AcademicPlanner:
        planner = AcademicPlanner("Integration Student")

        today = datetime.now().date()
        planner.add_item(Assignment(
            "HW1",
            (today + timedelta(days=3)).strftime("%Y-%m-%d"),
            "INST326",
            10.0,
            estimated_hours=3.0,
        ))
        planner.add_item(Project(
            "Project 1",
            (today + timedelta(days=10)).strftime("%Y-%m-%d"),
            "INST326",
            30.0,
            num_milestones=2,
            team_size=3,
        ))
        planner.add_item(Exam(
            "Midterm",
            (today + timedelta(days=7)).strftime("%Y-%m-%d"),
            "INST326",
            25.0,
            exam_type="midterm",
            num_chapters=5,
        ))
        return planner

    def test_save_and_load_preserves_item_count_and_types(self):
        planner = self._build_sample_planner()

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "planner.json"
            save_planner_to_json(planner, path)

            loaded = load_planner_from_json(path, default_student_name="Loaded")
            items = loaded.get_all_items()

            self.assertEqual(len(items), 3)
            type_names = sorted(type(i).__name__ for i in items)
            self.assertEqual(type_names, ["Assignment", "Exam", "Project"])

    def test_import_items_from_csv_and_add_to_planner(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "items.csv"
            csv_path.write_text(
                "type,title,due_date,course_code,weight,estimated_hours,num_milestones,team_size,exam_type,num_chapters\n"
                "Assignment,HW CSV,2025-11-25,INST326,10,3,,,,\n"
                "Project,Proj CSV,2025-12-01,INST326,30,,2,3,,\n"
                "Exam,Exam CSV,2025-11-30,INST326,20,,,,final,4\n",
                encoding="utf-8"
            )

            items = import_items_from_csv(csv_path)
            self.assertEqual(len(items), 3)

            planner = AcademicPlanner("CSV Student")
            for item in items:
                planner.add_item(item)

            self.assertEqual(len(planner.get_all_items()), 3)

    def test_export_deadlines_to_csv(self):
        planner = self._build_sample_planner()

        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "deadlines.csv"
            export_deadlines_to_csv(planner, csv_path, days_ahead=30)

            self.assertTrue(csv_path.exists())
            content = csv_path.read_text(encoding="utf-8").strip().splitlines()
            # At least header + one data line
            self.assertGreaterEqual(len(content), 2)


class TestSystemWorkflows(unittest.TestCase):
    """System tests: end-to-end workflows from import to export."""

    def test_end_to_end_import_save_load_export(self):
        """
        Full workflow:
        CSV -> AcademicItems -> Planner -> JSON save -> JSON load -> CSV deadlines.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # 1. Create CSV file with items
            csv_path = tmpdir / "items.csv"
            csv_path.write_text(
                "type,title,due_date,course_code,weight,estimated_hours,num_milestones,team_size,exam_type,num_chapters\n"
                "Assignment,HW1,2025-11-25,INST326,10,3,,,,\n"
                "Project,Proj1,2025-12-05,INST326,30,,2,3,,\n"
                "Exam,Final,2025-12-15,INST326,30,,,,final,6\n",
                encoding="utf-8"
            )

            # 2. Import items
            items = import_items_from_csv(csv_path)
            self.assertEqual(len(items), 3)

            # 3. Add to planner and compute workload
            planner = AcademicPlanner("System Student")
            for item in items:
                planner.add_item(item)

            total_workload_before = planner.get_total_workload()
            self.assertGreater(total_workload_before, 0.0)

            # 4. Save planner to JSON
            json_path = tmpdir / "planner.json"
            save_planner_to_json(planner, json_path)
            self.assertTrue(json_path.exists())

            # 5. Load planner from JSON
            loaded_planner = load_planner_from_json(json_path, default_student_name="System Student")
            self.assertEqual(len(loaded_planner.get_all_items()), 3)

            # 6. Ensure workload is still reasonable
            total_workload_after = loaded_planner.get_total_workload()
            self.assertAlmostEqual(total_workload_after, total_workload_before, places=2)

            # 7. Export deadlines
            deadlines_csv = tmpdir / "deadlines.csv"
            export_deadlines_to_csv(loaded_planner, deadlines_csv, days_ahead=365)
            self.assertTrue(deadlines_csv.exists())

    def test_end_to_end_completion_and_stats_after_load(self):
        """
        Workflow:
        Build planner -> complete some items -> save -> load -> stats preserved.
        """
        planner = AcademicPlanner("Stats Student")
        today = datetime.now().date()

        hw = Assignment("HW Stats", (today + timedelta(days=3)).strftime("%Y-%m-%d"),
                        "INST326", 10.0, estimated_hours=2.0)
        proj = Project("Proj Stats", (today + timedelta(days=10)).strftime("%Y-%m-%d"),
                       "INST326", 30.0, num_milestones=2, team_size=2)
        exam = Exam("Exam Stats", (today + timedelta(days=7)).strftime("%Y-%m-%d"),
                    "INST326", 25.0, exam_type="midterm", num_chapters=4)

        planner.add_item(hw)
        planner.add_item(proj)
        planner.add_item(exam)

        hw.mark_completed(95.0)

        with tempfile.TemporaryDirectory() as tmpdir:
            json_path = Path(tmpdir) / "planner.json"
            save_planner_to_json(planner, json_path)

            loaded = load_planner_from_json(json_path, default_student_name="Stats Student")
            stats = loaded.get_completion_stats()

            self.assertEqual(stats["total_items"], 3)
            self.assertEqual(stats["completed"], 1)
            self.assertGreaterEqual(stats["completion_rate"], 33.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
