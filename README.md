# Project 3: Class Tracker

This repository contains the implementation for Project 3, which demonstrates advanced object-oriented programming concepts including subclassing, method overriding, polymorphism, composition vs. inheritance decisions, and abstract base classes.

The project models a small class‑management system involving **Students**, **Courses**, and various **Task types** (Assignments, Exams, Projects). The system includes a reusable utilities module and a structured test suite using **pytest**.

---

## 📁 Repository Structure

```
project-repo/
├── README.md
├── docs/
│   └── architecture.txt
├── src/
│   ├── __init__.py
│   ├── abstract_base.py
│   ├── course.py
│   ├── student.py
│   ├── tasks.py
│   └── utils.py
└── tests/
    ├── test_inheritance.py
    ├── test_polymorphism.py
    └── test_composition.py
```

---

## ✨ Features Implemented

### 1. Inheritance & Subclassing

* Abstract base class `AbstractTask`
* Three subclasses: `Assignment`, `Exam`, `Project`
* Specialized implementations for each class

### 2. Polymorphism

* All task types override `calculate_weight()` and `summary()`
* Works interchangeably through shared interface

### 3. Composition vs. Inheritance

* Students *contain* Courses (composition)
* Courses *contain* Task lists (composition)
* Utilities such as email validation and course-code formatting are shared through composition (not inheritance)

### 4. Method Overriding & super()

* Subclasses extend base methods
* Shared logic kept in the abstract parent class

### 5. Reusable Helper Module

* `utils.py` contains:

  * `format_course_code()`
  * `validate_email()`

### 6. Test Suite Using pytest

* Tests inheritance behavior
* Tests polymorphism
* Tests composition relationships

---

## ▶️ Running the Project

### Install Dependencies

```
pip install -r requirements.txt
```

### Run Tests

```
pytest -v
```

---

## 📘 Documentation

More detailed technical explanations are available in:

➡️ `docs/architecture.txt`

---

## 👥 Authors

Class Tracker team — INST326
Jocelyn DeHenzel, Kayla Fuentes, Rhea Vyragaram, Vinindi Withanage

