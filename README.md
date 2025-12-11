# Class Tracker - Project 3: Inheritance & Polymorphism

**INST326 - Object-Oriented Programming for Information Science**  
**Team**: Class Tracker  
**Members**: Kayla Fuentes, Rhea Vyragaram, Jocelyn DeHenzel, Vinindi Withanage

---

## 📋 Project Overview

Class Tracker is a comprehensive academic management system for college students. **Project 3** extends our existing system (Projects 1 & 2) with advanced OOP principles including inheritance hierarchies, polymorphic behavior, abstract base classes, and composition relationships.

## 🧩 Project 4: Data Persistence, I/O, and End-to-End Testing

Project 4 extends Class Tracker into a **complete, persistent system**:

### New Features

- 💾 **Data Persistence**
  - Save and load full `AcademicPlanner` state to/from JSON
  - Student now HAS-A planner and can call `save_planner_state()` and `load_planner_state()`

- 📥 **Import / 📤 Export**
  - `import_items_from_csv()` reads standard CSV files and creates `Assignment`, `Project`, and `Exam` objects
  - `export_deadlines_to_csv()` writes upcoming deadlines to a CSV report that users can open in Excel

- 🧪 **Comprehensive Testing (Project 4)**
  - `test_project4_persistence.py`:
    - Unit tests for persistence helpers
    - Integration tests for planner + items + I/O
    - System tests for full workflows (import → planner → save/load → export)
  - All tests use Python’s `unittest` framework

### Example: Saving and Loading Planner State

```python
from student import Student

student = Student("Alex Johnson", "alex@umd.edu", "UID123456")

# ... enroll courses, add assignments, etc. ...

# Save academic planner state
student.save_planner_state("data/alex_planner.json")

# Later: load it back
student.load_planner_state("data/alex_planner.json")
print(student.planner.get_total_workload())

### What's New in Project 3

✨ **Abstract Base Classes** - Interface enforcement with Python's `abc` module  
✨ **Inheritance Hierarchy** - `AcademicItem` family with specialized derived classes  
✨ **Polymorphism** - Same interface, type-specific behavior  
✨ **Composition** - `AcademicPlanner` manages collections of academic items  
✨ **Enhanced Testing** - Comprehensive test suite covering all new features

---

## 🏗️ System Architecture

### Class Hierarchy

```
AcademicItem (Abstract Base Class)
    ├── Assignment (homework with time estimates)
    ├── Project (multi-phase work with milestones)
    └── Exam (assessments with study requirements)

AcademicPlanner (Composition)
    └── contains multiple AcademicItems
```

### Design Principles Applied

| Principle | Implementation |
|-----------|----------------|
| **Abstraction** | `AcademicItem` ABC defines common interface |
| **Encapsulation** | Private attributes with property accessors |
| **Inheritance** | Three specialized classes extend `AcademicItem` |
| **Polymorphism** | Uniform interface, type-specific behavior |
| **Composition** | `AcademicPlanner` HAS-A collection of items |

---

## 📁 Project Structure

```
class-tracker/
├── README.md                    # This file
├── academic_item.py             # Abstract base class
├── assignment_types.py          # Assignment, Project, Exam classes
├── academic_planner.py          # Composition example
├── student.py                   # From Project 2 (enhanced)
├── course.py                    # From Project 2
├── schedule.py                  # From Project 2
├── study_group.py               # From Project 2
├── library_name.py              # Function library from Project 1
├── test_project3.py             # Comprehensive test suite
├── docs/
│   ├── ARCHITECTURE.md          # Detailed design documentation
│   └── UML_DIAGRAM.png          # Class relationships diagram
└── requirements.txt             # Dependencies (if any)
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/class-tracker.git
cd class-tracker

# No external dependencies required - uses Python standard library
```

### Basic Usage

```python
from assignment_types import Assignment, Project, Exam
from academic_planner import AcademicPlanner

# Create a planner
planner = AcademicPlanner("Jane Smith")

# Add different types of academic items
assignment = Assignment('Homework 5', '2025-11-25', 'INST326', 15.0, 
                       estimated_hours=4.0)
project = Project('Final Project', '2025-12-10', 'INST326', 40.0,
                 num_milestones=3, team_size=4)
exam = Exam('Midterm Exam', '2025-11-22', 'INST326', 25.0,
           exam_type='midterm', num_chapters=6)

planner.add_item(assignment)
planner.add_item(project)
planner.add_item(exam)

# Use polymorphic methods
print(f"Total workload: {planner.get_total_workload()} hours")
print(f"Priority summary: {planner.get_priority_summary()}")

# Each item calculates differently (polymorphism!)
for item in planner.get_all_items():
    print(f"{item.title}: {item.calculate_time_commitment()} hours")
```

### Running Tests

```bash
# Run comprehensive test suite
python test_project3.py

# Expected output: All tests should pass
# Tests run: 30+
# Covering: inheritance, polymorphism, composition, validation
```

---

## 🎯 Key Features

### 1. Abstract Base Class (ABC)

**AcademicItem** defines the contract all academic items must follow:

```python
from abc import ABC, abstractmethod

class AcademicItem(ABC):
    @abstractmethod
    def calculate_time_commitment(self) -> float:
        """Each type calculates differently"""
        pass
    
    @abstractmethod
    def get_priority(self) -> str:
        """Each type has unique priority logic"""
        pass
```

**Benefits**:
- ✓ Cannot instantiate incomplete subclasses
- ✓ Enforces consistent interface
- ✓ Catches missing implementations early
- ✓ Clear documentation of requirements

### 2. Inheritance Hierarchy

Three specialized classes extend `AcademicItem`:

#### Assignment
```python
assignment = Assignment('HW1', '2025-12-01', 'INST326', 10.0, 
                       estimated_hours=3.0)
# Time commitment: direct from estimated_hours
# Priority: based on due date and weight
```

#### Project
```python
project = Project('Final', '2025-12-10', 'INST326', 40.0,
                 num_milestones=3, team_size=4)
# Time commitment: calculated from milestones / team_size
# Priority: elevated due to complexity
# Features: add_milestone(), set_repository()
```

#### Exam
```python
exam = Exam('Midterm', '2025-11-22', 'INST326', 25.0,
           exam_type='midterm', num_chapters=6)
# Time commitment: based on chapters × study_hours_per_chapter
# Priority: always high when approaching
# Features: set_study_guide(), set_location()
```

### 3. Polymorphic Behavior

Same method calls, different implementations:

```python
items = [assignment, project, exam]

# Polymorphism in action!
for item in items:
    # Each type implements these differently
    hours = item.calculate_time_commitment()
    priority = item.get_priority()
    item_type = item.get_item_type()
    
    print(f"{item.title}: {hours}h, {priority} priority")
```

**Output demonstrates polymorphism:**
```
HW1: 3.0h, medium priority          (Assignment logic)
Final: 20.5h, high priority         (Project logic)
Midterm: 18.0h, critical priority   (Exam logic)
```

### 4. Composition Relationship

**AcademicPlanner** demonstrates composition - it HAS-A collection of items:

```python
planner = AcademicPlanner("Student Name")

# Planner CONTAINS items (composition, not inheritance)
planner.add_item(assignment)
planner.add_item(project)
planner.add_item(exam)

# Aggregate operations
workload = planner.calculate_weekly_workload(weeks_ahead=2)
summary = planner.get_priority_summary()
deadlines = planner.get_upcoming_deadlines(days_ahead=7)
```

**Why Composition?**
- ❌ A planner is NOT a type of academic item (not is-a)
- ✓ A planner HAS academic items (has-a relationship)
- ✓ Flexible: can hold any AcademicItem subclass
- ✓ Loose coupling: items and planner change independently

---

## 📊 Example Scenarios

### Scenario 1: Calculating Weekly Workload

```python
from assignment_types import Assignment, Project, Exam
from academic_planner import AcademicPlanner

planner = AcademicPlanner("Alex Chen")

# Add upcoming work
planner.add_item(Assignment('HW5', '2025-11-25', 'INST326', 10, 
                           estimated_hours=3))
planner.add_item(Project('Web App', '2025-11-28', 'INST326', 30,
                        num_milestones=2, team_size=3))
planner.add_item(Exam('Quiz 3', '2025-11-27', 'INST326', 5,
                     exam_type='quiz', num_chapters=2))

# Calculate workload (polymorphic calls!)
workload = planner.calculate_weekly_workload(1)
print(f"This week's workload: {list(workload.values())[0]} hours")

# Output: This week's workload: 21.5 hours
# Assignment: 3h + Project: 14.5h + Quiz: 4h = 21.5h
```

### Scenario 2: Priority Management

```python
# Get items by priority level
critical_items = planner.get_items_by_priority('critical')
high_items = planner.get_items_by_priority('high')

print(f"Critical items: {len(critical_items)}")
print(f"High priority items: {len(high_items)}")

# Each item type calculates priority differently!
# Exams become critical within 7 days
# Projects become critical within 5 days
# Assignments depend on weight + due date
```

### Scenario 3: Type-Specific Operations

```python
# Access type-specific features
for item in planner.get_items_by_type('Project'):
    item.add_milestone('Phase 1', '2025-11-20')
    item.set_repository('https://github.com/team/project')

for item in planner.get_items_by_type('Exam'):
    item.set_study_guide('Review chapters 1-5')
    item.set_location('ESJ 2204')

for item in planner.get_items_by_type('Assignment'):
    item.add_notes('Remember to test edge cases')
```

---

## 🧪 Testing

### Test Coverage

Our test suite (`test_project3.py`) includes:

| Test Category | Tests | Coverage |
|--------------|-------|----------|
| **Abstract Base Classes** | 3 | Cannot instantiate, must implement methods |
| **Inheritance** | 5 | Relationships, super() calls, properties |
| **Polymorphism** | 5 | Different behaviors, uniform interface |
| **Composition** | 4 | Has-a relationships, management |
| **Specialized Behavior** | 6 | Type-specific features |
| **Validation** | 5 | Input checking, error handling |
| **Total** | **28+** | Comprehensive coverage |

### Running Tests

```bash
# Run all tests with verbose output
python test_project3.py

# Expected output:
# test_assignment_is_academic_item ... ok
# test_calculate_time_commitment_polymorphism ... ok
# test_planner_has_items ... ok
# ... (all tests)
# 
# ======================================================================
# TEST SUMMARY
# ======================================================================
# Tests run: 28
# Successes: 28
# Failures: 0
# Errors: 0
```

### Key Test Examples

**Testing Abstract Class Enforcement:**
```python
def test_cannot_instantiate_abstract_class(self):
    """AcademicItem cannot be instantiated directly."""
    with self.assertRaises(TypeError):
        item = AcademicItem('Test', '2025-12-01', 'INST326', 10.0)
```

**Testing Polymorphism:**
```python
def test_polymorphic_list_processing(self):
    """Same interface works with all types."""
    items = [assignment, project, exam]
    total = sum(item.calculate_time_commitment() for item in items)
    # Each calculates differently, but interface is uniform
```

**Testing Composition:**
```python
def test_planner_manages_multiple_types(self):
    """Planner can hold different item types."""
    planner.add_item(Assignment(...))
    planner.add_item(Project(...))
    planner.add_item(Exam(...))
    # Planner HAS items, doesn't inherit from them
```

---

## 📖 Documentation

### Main Documentation Files

1. **README.md** (this file) - Quick start and overview
2. **docs/ARCHITECTURE.md** - Detailed design decisions and rationale
   - Inheritance hierarchies explained
   - Polymorphism examples
   - Composition vs. inheritance decisions
   - UML diagrams

### Code Documentation

All modules include:
- Comprehensive docstrings (Google style)
- Type hints for all methods
- Usage examples in docstrings
- Inline comments for complex logic

Example:
```python
def calculate_time_commitment(self) -> float:
    """
    Calculate time commitment for projects.
    
    Projects require more time based on complexity (milestones)
    but divided by team size for collaborative work.
    
    Returns:
        float: Estimated hours
        
    Example:
        >>> project = Project('Final', '2025-12-10', 'INST326', 40, 
        ...                   num_milestones=3, team_size=4)
        >>> project.calculate_time_commitment()
        20.5
    """
```

---

## 🎓 Learning Outcomes Demonstrated

### Advanced OOP Concepts

✅ **Abstract Base Classes**
- Defined clear interfaces with `abc` module
- Enforced method implementation in subclasses
- Cannot instantiate incomplete classes

✅ **Inheritance Hierarchies**
- Created logical "is-a" relationships
- Maximized code reuse through inheritance
- Kept hierarchy shallow (2 levels) for maintainability

✅ **Polymorphism**
- Same method name, different implementations
- Dynamic dispatch at runtime
- Type-agnostic code in `AcademicPlanner`

✅ **Composition**
- Demonstrated "has-a" relationships
- Chose composition over inheritance appropriately
- Loose coupling between components

✅ **Method Overriding**
- All subclasses properly override abstract methods
- Use of `super()` for parent class initialization
- Maintained consistent interfaces

### Software Engineering Practices

✅ **Design Patterns**
- Template Method (in `AcademicItem`)
- Composite Pattern (in `AcademicPlanner`)

✅ **SOLID Principles**
- Single Responsibility: Each class has one purpose
- Open/Closed: Open for extension, closed for modification
- Liskov Substitution: Subclasses can replace base class
- Interface Segregation: Clean, focused interfaces
- Dependency Inversion: Depend on abstractions

✅ **Testing**
- Unit tests for all components
- Integration tests for interactions
- Edge case handling
- 100% of abstract methods tested

---

## 🔄 Integration with Projects 1 & 2

### Project 1 Integration
- Function library still used for utilities
- Validation functions integrated into new classes
- All 15 original functions preserved

### Project 2 Integration
- `Student` class works with new item types
- `Course` class unchanged but compatible
- Existing composition relationships preserved
- Backward compatibility maintained

### Migration Path
```python
# Project 2 style (still works!)
from assignment import Assignment as OldAssignment
assignment = OldAssignment('HW1', '2025-12-01', 'INST326', 10.0)

# Project 3 style (new capabilities!)
from assignment_types import Assignment
assignment = Assignment('HW1', '2025-12-01', 'INST326', 10.0, 
                       estimated_hours=3.0)

# Both work! New classes extend, don't replace
```

---

## 🚧 Future Enhancements

Potential extensions while maintaining current architecture:

### 1. Additional Item Types
```python
class Quiz(Exam):
    """Quiz as specialized exam type"""
    pass

class Lab(Assignment):
    """Lab with equipment and partner tracking"""
    pass
```

### 2. Notification System
```python
class NotificationManager:
    """Observer pattern for due date alerts"""
    def register_observer(self, item: AcademicItem):
        # Send alerts as due dates approach
```

### 3. Persistence Layer
```python
class ItemRepository:
    """Save/load items to database"""
    def save(self, item: AcademicItem):
        # Serialize polymorphically
```

### 4. Grade Calculator
```python
class GradeCalculator:
    """Calculate weighted averages"""
    def calculate_final_grade(self, items: List[AcademicItem]):
        # Use polymorphic weight and score
```

All extensions leverage existing polymorphic infrastructure!

---

## 👥 Team Contributions

| Team Member | Contributions |
|------------|---------------|
| **Kayla Fuentes** | Abstract base class design, inheritance hierarchy |
| **Rhea Vyragaram** | Polymorphic methods, derived class implementation |
| **Jocelyn DeHenzel** | Composition relationships, AcademicPlanner |
| **Vinindi Withanage** | Testing suite, documentation |

All members contributed to design discussions, code review, and documentation.

---

## 📝 Assignment Requirements Checklist

### Technical Requirements ✓

- [x] **Inheritance Hierarchy**: `AcademicItem` → `Assignment`, `Project`, `Exam`
- [x] **Base Class**: `AcademicItem` with common interface
- [x] **2-3 Derived Classes**: Three classes with specialization
- [x] **Method Overriding**: All abstract methods overridden with `super()` calls
- [x] **Logical Relationships**: True "is-a" relationships throughout

### Abstract Base Classes ✓

- [x] **ABC Module**: Used `from abc import ABC, abstractmethod`
- [x] **Abstract Methods**: Three abstract methods defined
- [x] **Enforcement**: Cannot instantiate base class
- [x] **Documentation**: Clear docstrings explaining contract

### Polymorphism ✓

- [x] **Same Method, Different Behavior**: `calculate_time_commitment()`, `get_priority()`
- [x] **Base Class References**: `AcademicPlanner` works with base class type
- [x] **Uniform Handling**: Multiple object types processed uniformly
- [x] **Dynamic Dispatch**: Runtime method resolution

### Composition ✓

- [x] **Composition Relationship**: `AcademicPlanner` contains `AcademicItems`
- [x] **Has-A Demonstrated**: Clear container/contained relationship
- [x] **Rationale Explained**: Why composition chosen over inheritance

### Deliverables ✓

- [x] **Enhanced Codebase**: All Project 2 classes refactored
- [x] **Tests**: Comprehensive test suite (28+ tests)
- [x] **Architecture Document**: `docs/ARCHITECTURE.md` with full explanations
- [x] **Updated README**: This document with diagrams and examples
- [x] **GitHub Structure**: Proper repository organization

---

**README Version**: 3.0  
**Last Updated**: November 2025  
**Project**: 3 - Inheritance and Polymorphism
