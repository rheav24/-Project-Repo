# academic_io.py
"""
Academic I/O utilities for Project 4.

Handles:
- Saving/loading AcademicPlanner state to/from JSON
- Importing AcademicItem objects from CSV
- Exporting upcoming deadlines to CSV

This module fulfills Project 4 requirements for:
- Data persistence between sessions
- Import/export from standard formats
- Robust error handling around file I/O
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, List

from academic_item import AcademicItem
from assignment import Assignment, Project, Exam
from academic_planner import AcademicPlanner


# Map type strings to concrete classes for deserialization
ITEM_CLASS_MAP = {
    "Assignment": Assignment,
    "Project": Project,
    "Exam": Exam,
}


def _serialize_item(item: AcademicItem) -> Dict[str, Any]:
    """
    Convert an AcademicItem (or subclass) into a JSON-serializable dict.

    We do NOT depend on internal implementation details more than necessary.
    We rely on public attributes/methods exposed in Project 3.
    """
    base = {
        "type": item.__class__.__name__,
        "title": item.title,
        "due_date": item.due_date,
        "course_code": item.course_code,
        "weight": item.weight,
        "status": getattr(item, "status", "not_started"),
        "score": getattr(item, "score", None),
    }

    # Type-specific fields (polymorphic)
    if isinstance(item, Assignment):
        base.update({
            "estimated_hours": getattr(item, "estimated_hours", 0.0),
            "notes": getattr(item, "get_notes", lambda: "")(),
            "instructions": getattr(item, "get_instructions", lambda: "")(),
        })
    elif isinstance(item, Project):
        base.update({
            "num_milestones": getattr(item, "num_milestones", 0),
            "team_size": getattr(item, "team_size", 1),
            "milestones": getattr(item, "get_milestones", lambda: [])(),
            "repository": getattr(item, "get_repository", lambda: "")(),
        })
    elif isinstance(item, Exam):
        base.update({
            "exam_type": getattr(item, "exam_type", ""),
            "num_chapters": getattr(item, "num_chapters", 0),
            "study_guide": getattr(item, "get_study_guide", lambda: "")(),
            "location": getattr(item, "get_location", lambda: "")(),
        })

    return base


def _deserialize_item(data: Dict[str, Any]) -> AcademicItem:
    """
    Recreate an AcademicItem subclass from a serialized dict.

    Raises:
        ValueError: If the type is unknown or data is invalid.
    """
    item_type = data.get("type")
    cls = ITEM_CLASS_MAP.get(item_type)
    if cls is None:
        raise ValueError(f"Unknown academic item type: {item_type!r}")

    title = data["title"]
    due_date = data["due_date"]
    course_code = data["course_code"]
    weight = float(data["weight"])

    if item_type == "Assignment":
        item = Assignment(
            title,
            due_date,
            course_code,
            weight,
            estimated_hours=float(data.get("estimated_hours", 0.0)),
        )
        notes = data.get("notes")
        if notes:
            item.add_notes(notes)
        instructions = data.get("instructions")
        if instructions:
            item.set_instructions(instructions)

    elif item_type == "Project":
        item = Project(
            title,
            due_date,
            course_code,
            weight,
            num_milestones=int(data.get("num_milestones", 0)),
            team_size=int(data.get("team_size", 1)),
        )
        for m in data.get("milestones", []):
            m_title = m.get("title")
            m_due = m.get("due_date")
            if m_title and m_due:
                item.add_milestone(m_title, m_due)
        repo = data.get("repository")
        if repo:
            item.set_repository(repo)

    elif item_type == "Exam":
        item = Exam(
            title,
            due_date,
            course_code,
            weight,
            exam_type=data.get("exam_type", "exam"),
            num_chapters=int(data.get("num_chapters", 0)),
        )
        sg = data.get("study_guide")
        if sg:
            item.set_study_guide(sg)
        loc = data.get("location")
        if loc:
            item.set_location(loc)
    else:
        # Should not reach here because of ITEM_CLASS_MAP check above
        raise ValueError(f"Unsupported academic item type: {item_type!r}")

    # Restore status/score if present
    status = data.get("status")
    if status in {"completed", "in_progress", "not_started"}:
        item.status = status
    score = data.get("score")
    if score is not None:
        try:
            item.score = float(score)
        except (TypeError, ValueError):
            pass

    return item


def save_planner_to_json(planner: AcademicPlanner, filepath: str | Path) -> None:
    """
    Save an AcademicPlanner and all items to a JSON file.

    Uses:
        - pathlib for paths
        - with-statement for safe file I/O
        - explicit error handling

    Raises:
        OSError: If writing the file fails.
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "student_name": getattr(planner, "student_name", None),
        "generated_at": datetime.now().isoformat(),
        "items": [_serialize_item(item) for item in planner.get_all_items()],
    }

    try:
        with path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
    except OSError as e:
        raise OSError(f"Failed to save planner to {path}: {e}") from e


def load_planner_from_json(filepath: str | Path,
                           default_student_name: str = "Loaded Student"
                           ) -> AcademicPlanner:
    """
    Load an AcademicPlanner and its items from a JSON file.

    Handles:
        - Missing file (FileNotFoundError)
        - Corrupted JSON (ValueError)

    Returns:
        AcademicPlanner: New planner instance populated with items.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Planner file not found: {path}")

    try:
        with path.open("r", encoding="utf-8") as f:
            payload = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Planner file {path} is corrupted or invalid JSON") from e

    student_name = payload.get("student_name") or default_student_name
    planner = AcademicPlanner(student_name)

    for item_data in payload.get("items", []):
        try:
            item = _deserialize_item(item_data)
            planner.add_item(item)
        except (ValueError, KeyError):
            # Skip invalid item records instead of crashing
            continue

    return planner


def import_items_from_csv(csv_path: str | Path,
                          default_course_code: str | None = None
                          ) -> List[AcademicItem]:
    """
    Import AcademicItems from a CSV file.

    Expected columns (header row):
        type,title,due_date,course_code,weight,
        estimated_hours,num_milestones,team_size,
        exam_type,num_chapters

    Missing/extra columns are tolerated; invalid rows are skipped.

    Returns:
        List[AcademicItem]: List of successfully imported items.

    Raises:
        FileNotFoundError: If CSV file is missing.
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    items: List[AcademicItem] = []

    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                item_type = (row.get("type") or "").strip()
                title = (row.get("title") or "").strip()
                due_date = (row.get("due_date") or "").strip()
                course_code = (row.get("course_code") or "").strip() or (default_course_code or "")
                weight_str = (row.get("weight") or "").strip()
                if not all([item_type, title, due_date, course_code, weight_str]):
                    continue
                weight = float(weight_str)

                if item_type == "Assignment":
                    est = float((row.get("estimated_hours") or "0").strip() or 0)
                    item = Assignment(title, due_date, course_code, weight,
                                      estimated_hours=est)
                elif item_type == "Project":
                    num_milestones = int((row.get("num_milestones") or "0").strip() or 0)
                    team_size = int((row.get("team_size") or "1").strip() or 1)
                    item = Project(title, due_date, course_code, weight,
                                   num_milestones=num_milestones, team_size=team_size)
                elif item_type == "Exam":
                    exam_type = (row.get("exam_type") or "exam").strip()
                    num_chapters = int((row.get("num_chapters") or "0").strip() or 0)
                    item = Exam(title, due_date, course_code, weight,
                                exam_type=exam_type, num_chapters=num_chapters)
                else:
                    # Unknown type -> skip
                    continue

                items.append(item)
            except (ValueError, TypeError):
                # Skip malformed rows
                continue

    return items


def export_deadlines_to_csv(planner: AcademicPlanner,
                            csv_path: str | Path,
                            days_ahead: int = 30) -> None:
    """
    Export upcoming deadlines from a planner to a CSV file.

    Uses AcademicPlanner.get_upcoming_deadlines(days_ahead) which is expected
    to return a list of dicts with at least:
        'due_date', 'title', 'type', 'hours_needed', 'priority'

    Raises:
        OSError: If writing the file fails.
    """
    path = Path(csv_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    deadlines = planner.get_upcoming_deadlines(days_ahead)
    fieldnames = ["due_date", "title", "type", "course_code",
                  "hours_needed", "priority"]

    try:
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for d in deadlines:
                writer.writerow({
                    "due_date": d.get("due_date", ""),
                    "title": d.get("title", ""),
                    "type": d.get("type", ""),
                    "course_code": d.get("course_code", ""),
                    "hours_needed": d.get("hours_needed", ""),
                    "priority": d.get("priority", ""),
                })
    except OSError as e:
        raise OSError(f"Failed to export deadlines to {path}: {e}") from e
