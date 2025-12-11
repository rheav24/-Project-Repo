"""
AcademicPlanner Module
INST326 - Project 4: System Integration, Persistence, and Testing

Team: Class Tracker
Members: Kayla Fuentes, Rhea Vyragaram, Jocelyn DeHenzel, Vinindi Withanage

This module demonstrates:
- Composition: AcademicPlanner HAS-A collection of AcademicItem objects
- Polymorphism: Works with Assignment, Project, and Exam uniformly
- Data persistence: save/load planner state to JSON
- Import/export: CSV import/export for academic items
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json
import csv

from academic_item import AcademicItem
from assignment import Assignment, Project, Exam


class AcademicPlanner:
    """
    Planner that manages a collection of academic items.

    Composition:
        A planner HAS-A list of AcademicItem instances (Assignment, Project, Exam).

    Project 4 Additions:
        - save_to_json / load_from_json
        - export_to_csv / import_from_csv
        - Robust error handling for file I/O
    """

    def __init__(self, student_name: str):
        if not isinstance(student_name, str) or not student_name.strip():
            raise ValueError("student_name must be a non-empty string")

        self._student_name = student_name.strip()
        self._items: List[AcademicItem] = []

    # ------------------------------------------------------------------
    # Basic composition / collection behavior
    # ------------------------------------------------------------------
    @property
    def student_name(self) -> str:
        return self._student_name

    def add_item(self, item: AcademicItem) -> None:
        """Add an AcademicItem (Assignment, Project, or Exam) to the planner."""
        if not isinstance(item, AcademicItem):
            raise TypeError("planner can only contain AcademicItem instances")
        self._items.append(item)

    def get_all_items(self) -> List[AcademicItem]:
        """Return a shallow copy of all items."""
        return list(self._items)

    # ------------------------------------------------------------------
    # Polymorphic aggregate operations (Project 3 behavior)
    # ------------------------------------------------------------------
    def get_total_workload(self) -> float:
        """
        Sum time commitment for all incomplete items, using polymorphic
        calculate_time_commitment() on each item.
        """
        total = 0.0
        for item in self._items:
            if getattr(item, "status", "not_started") != "completed":
                total += float(item.calculate_time_commitment())
        return round(total, 2)

    def get_items_by_priority(self, priority: str) -> List[AcademicItem]:
        """Return all items whose get_priority() matches the given level."""
        valid = {"critical", "high", "medium", "low"}
        if priority not in valid:
            raise ValueError(f"Priority must be one of {sorted(valid)}")

        result: List[AcademicItem] = []
        for item in self._items:
            if getattr(item, "status", "not_started") != "completed":
                if item.get_priority() == priority:
                    result.append(item)
        return result

    def get_priority_summary(self) -> Dict[str, int]:
        """
        Return counts of items in each priority level (critical/high/medium/low).
        Uses each item's polymorphic get_priority().
        """
        summary = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for item in self._items:
            prio = item.get_priority()
            if prio in summary:
                summary[prio] += 1
        return summary

    def get_items_by_type(self, type_name: str) -> List[AcademicItem]:
        """
        Filter items by class name: 'Assignment', 'Project', 'Exam'.
        (Used by your demo script.)
        """
        return [i for i in self._items if type(i).__name__ == type_name]

    def calculate_weekly_workload(self, weeks_ahead: int = 1) -> Dict[str, float]:
        """
        Approximate workload for the next N weeks.

        Returns:
            Dict like {"Week 1": hours, "Week 2": hours, ...}
        """
        if not isinstance(weeks_ahead, int) or weeks_ahead <= 0:
            raise ValueError("weeks_ahead must be a positive integer")

        today = datetime.now().date()
        result: Dict[str, float] = {f"Week {i+1}": 0.0 for i in range(weeks_ahead)}

        for item in self._items:
            try:
                due = datetime.strptime(item.due_date, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                # Skip items with bad dates
                continue

            days_delta = (due - today).days
            if days_delta < 0:
                continue  # already past

            week_index = days_delta // 7
            if 0 <= week_index < weeks_ahead:
                key = f"Week {week_index + 1}"
                result[key] += float(item.calculate_time_commitment())

        # Round for nicer output
        return {k: round(v, 2) for k, v in result.items()}

    def get_upcoming_deadlines(self, days_ahead: int = 7) -> List[Dict]:
        """
        Return a list of upcoming deadlines within days_ahead, including:
        title, due_date, type, hours_needed, priority.
        """
        if not isinstance(days_ahead, int) or days_ahead <= 0:
            raise ValueError("days_ahead must be a positive integer")

        today = datetime.now().date()
        cutoff = today + timedelta(days=days_ahead)
        results: List[Dict] = []

        for item in self._items:
            try:
                due = datetime.strptime(item.due_date, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                continue

            if today <= due <= cutoff:
                results.append({
                    "title": item.title,
                    "due_date": item.due_date,
                    "type": item.get_item_type(),
                    "hours_needed": float(item.calculate_time_commitment()),
                    "priority": item.get_priority(),
                })

        results.sort(key=lambda d: d["due_date"])
        return results

    def get_completion_stats(self) -> Dict[str, float]:
        """
        Return overall completion statistics for the planner.

        Returns dict with:
            - total_items
            - completed
            - in_progress
            - not_started
            - completion_rate
            - average_score (only counting completed items with score set)
        """
        total = len(self._items)
        completed = in_progress = not_started = 0
        scores = []

        for item in self._items:
            status = getattr(item, "status", "not_started")
            if status == "completed":
                completed += 1
                score = getattr(item, "score", None)
                if isinstance(score, (int, float)):
                    scores.append(float(score))
            elif status == "in_progress":
                in_progress += 1
            else:
                not_started += 1

        completion_rate = 0.0 if total == 0 else (completed / total) * 100.0
        average_score = sum(scores) / len(scores) if scores else 0.0

        return {
            "total_items": total,
            "completed": completed,
            "in_progress": in_progress,
            "not_started": not_started,
            "completion_rate": round(completion_rate, 2),
            "average_score": round(average_score, 2),
        }

    # ------------------------------------------------------------------
    # Persistence & I/O (Project 4)
    # ------------------------------------------------------------------
    def _item_to_dict(self, item: AcademicItem) -> Dict:
        """
        Convert an AcademicItem subclass to a serializable dict.

        We intentionally DO NOT rely on internal __dict__ layout.
        Instead, we use the public contract and known extra fields.
        """
        base = {
            "title": item.title,
            "due_date": item.due_date,
            "course_code": item.course_code,
            "weight": item.weight,
            "status": getattr(item, "status", "not_started"),
            "score": getattr(item, "score", None),
            "type": item.get_item_type(),  # 'ASSIGNMENT', 'PROJECT', 'EXAM...'
        }

        # Extra fields by type
        if isinstance(item, Assignment):
            base.update({
                "estimated_hours": getattr(item, "estimated_hours", 0.0),
                "notes": getattr(item, "_notes", ""),
                "instructions": getattr(item, "_instructions", ""),
            })
        elif isinstance(item, Project):
            base.update({
                "num_milestones": getattr(item, "num_milestones", 0),
                "team_size": getattr(item, "team_size", 1),
                "milestones": getattr(item, "_milestones", []),
                "repository_url": getattr(item, "_repository_url", ""),
            })
        elif isinstance(item, Exam):
            base.update({
                "exam_type": getattr(item, "exam_type", "exam"),
                "num_chapters": getattr(item, "num_chapters", 0),
                "study_guide": getattr(item, "_study_guide", ""),
                "location": getattr(item, "_location", ""),
            })

        return base

    def _item_from_dict(self, data: Dict) -> AcademicItem:
        """
        Recreate an AcademicItem subclass from a dict produced by _item_to_dict.
        Raises ValueError if data is missing required keys.
        """
        item_type = data.get("type", "").upper()
        title = data["title"]
        due_date = data["due_date"]
        course_code = data["course_code"]
        weight = float(data["weight"])

        if "ASSIGNMENT" in item_type:
            item = Assignment(
                title,
                due_date,
                course_code,
                weight,
                estimated_hours=float(data.get("estimated_hours", 0.0)),
            )
            notes = data.get("notes")
            instructions = data.get("instructions")
            if notes:
                item.add_notes(notes)
            if instructions:
                item.set_instructions(instructions)

        elif "PROJECT" in item_type:
            item = Project(
                title,
                due_date,
                course_code,
                weight,
                num_milestones=int(data.get("num_milestones", 0)),
                team_size=int(data.get("team_size", 1)),
            )
            for m in data.get("milestones", []):
                title_m = m.get("title")
                due_m = m.get("due_date")
                if title_m and due_m:
                    item.add_milestone(title_m, due_m)
            repo = data.get("repository_url")
            if repo:
                item.set_repository(repo)

        elif "EXAM" in item_type:
            item = Exam(
                title,
                due_date,
                course_code,
                weight,
                exam_type=data.get("exam_type", "exam"),
                num_chapters=int(data.get("num_chapters", 0)),
            )
            guide = data.get("study_guide")
            loc = data.get("location")
            if guide:
                item.set_study_guide(guide)
            if loc:
                item.set_location(loc)

        else:
            raise ValueError(f"Unknown academic item type: {item_type}")

        # Restore common status/score
        status = data.get("status")
        score = data.get("score", None)
        if status == "completed" and score is not None:
            try:
                item.mark_completed(float(score))
            except Exception:
                # If mark_completed is stricter than we expect, just set status
                item.status = "completed"  # type: ignore[attr-defined]
        elif status in {"completed", "in_progress", "not_started"}:
            item.status = status  # type: ignore[attr-defined]

        return item

    def save_to_json(self, path: Path | str) -> None:
        """
        Save planner state to a JSON file.

        Uses pathlib, context managers, and careful error handling.

        Raises:
            OSError: if the file cannot be written.
        """
        out_path = Path(path)
        payload = {
            "student_name": self._student_name,
            "generated_at": datetime.now().isoformat(),
            "items": [self._item_to_dict(i) for i in self._items],
        }

        try:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with out_path.open("w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
        except OSError as e:
            # Let caller decide how to surface this, but don't silently fail
            raise OSError(f"Failed to save planner JSON to {out_path}: {e}") from e

    def load_from_json(self, path: Path | str) -> None:
        """
        Load planner state from a JSON file, replacing current items.

        Raises:
            FileNotFoundError: if file is missing
            ValueError: if JSON is invalid or missing required keys
            OSError: if file cannot be read
        """
        in_path = Path(path)
        if not in_path.exists():
            raise FileNotFoundError(f"Planner JSON file not found: {in_path}")

        try:
            with in_path.open("r", encoding="utf-8") as f:
                raw = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {in_path}: {e}") from e
        except OSError as e:
            raise OSError(f"Failed to read planner JSON from {in_path}: {e}") from e

        try:
            self._student_name = raw.get("student_name", self._student_name)
            items_data = raw["items"]
        except KeyError as e:
            raise ValueError(f"Planner JSON missing required key: {e}") from e

        new_items: List[AcademicItem] = []
        for item_data in items_data:
            try:
                new_items.append(self._item_from_dict(item_data))
            except Exception:
                # Skip corrupted entries but do not crash the entire load
                continue

        self._items = new_items

    def export_to_csv(self, path: Path | str) -> None:
        """
        Export items to a CSV file.

        Columns:
            type, title, due_date, course_code, weight, priority, hours_needed
        """
        out_path = Path(path)
        try:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with out_path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "type",
                        "title",
                        "due_date",
                        "course_code",
                        "weight",
                        "priority",
                        "hours_needed",
                    ],
                )
                writer.writeheader()
                for item in self._items:
                    writer.writerow(
                        {
                            "type": item.get_item_type(),
                            "title": item.title,
                            "due_date": item.due_date,
                            "course_code": item.course_code,
                            "weight": item.weight,
                            "priority": item.get_priority(),
                            "hours_needed": float(item.calculate_time_commitment()),
                        }
                    )
        except OSError as e:
            raise OSError(f"Failed to export planner CSV to {out_path}: {e}") from e

    def import_from_csv(self, path: Path | str) -> int:
        """
        Import items from a CSV file.

        Expected minimum columns:
            type, title, due_date, course_code, weight

        Optional extra columns:
            estimated_hours, num_milestones, team_size, exam_type, num_chapters

        Returns:
            int: number of successfully imported items

        Raises:
            FileNotFoundError: if file does not exist
            OSError: if file cannot be read
        """
        in_path = Path(path)
        if not in_path.exists():
            raise FileNotFoundError(f"Planner CSV file not found: {in_path}")

        imported_count = 0

        try:
            with in_path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        item_type = (row.get("type") or "").upper()
                        title = row["title"]
                        due_date = row["due_date"]
                        course_code = row["course_code"]
                        weight = float(row["weight"])

                        if "ASSIGNMENT" in item_type:
                            est = float(row.get("estimated_hours", 0.0) or 0.0)
                            item = Assignment(
                                title, 
                                due_date, 
                                course_code, 
                                weight,
                                assignment_type='homework',
                                status='not_started',
                                estimated_hours=est
                            )
                        elif "PROJECT" in item_type:
                            milestones = int(row.get("num_milestones", 0) or 0)
                            team_size = int(row.get("team_size", 1) or 1)
                            item = Project(
                                title,
                                due_date,
                                course_code,
                                weight,
                                num_milestones=milestones,
                                team_size=team_size,
                            )
                        elif "EXAM" in item_type:
                            exam_type = row.get("exam_type", "exam")
                            chapters = int(row.get("num_chapters", 0) or 0)
                            item = Exam(
                                title,
                                due_date,
                                course_code,
                                weight,
                                exam_type=exam_type,
                                num_chapters=chapters,
                            )
                        else:
                            # Unknown type; skip row
                            continue

                        self.add_item(item)
                        imported_count += 1
                    except (KeyError, ValueError):
                        # Skip corrupted/invalid rows, continue reading
                        continue
        except OSError as e:
            raise OSError(f"Failed to import planner CSV from {in_path}: {e}") from e

        return imported_count

    # ------------------------------------------------------------------
    # Convenience / string representation
    # ------------------------------------------------------------------
    def __str__(self) -> str:
        return (
            f"AcademicPlanner for {self._student_name} "
            f"({len(self._items)} items, workload {self.get_total_workload()}h)"
        )

    def __repr__(self) -> str:
        return f"AcademicPlanner(student_name={self._student_name!r}, items={len(self._items)})"
