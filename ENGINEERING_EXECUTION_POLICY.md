---
# ENGINEERING_EXECUTION_POLICY.md
---

# ⚙️ Engineering Execution Policy

Defines engineering standards for this project.

---

## 🎯 Goal

Deliver a **clean, maintainable, production-ready CLI tool**.

---

## 🧱 Architecture Rules

### 1. Separation of Concerns

| Layer | Responsibility |
|------|--------|
| CLI | user interaction |
| Config | configuration |
| Scanner | file system logic |
| Generator | output |
| Utils | shared tools |

---

### 2. No Cross-Layer Leakage

Example:

❌ Scanner should NOT handle CLI
❌ CLI should NOT handle filesystem logic

---

## 🧠 Code Quality Rules

### Required:

- Type hints
- Docstrings
- Logging

---

### Forbidden:

- `print()` for debugging
- hardcoded paths
- duplicated logic

---

## 🪵 Logging Policy

Use logging levels:

| Level | Usage |
|------|------|
| DEBUG | internal state |
| INFO | normal operations |
| WARNING | recoverable issues |
| ERROR | failures |

---

## 📦 Feature Development Flow

Each feature must include:

1. Implementation
2. CLI integration
3. Documentation update

---

## 🚀 Release Readiness

Before release:

- CLI works correctly
- documentation updated
- no debug code
- clean output

---

## 📌 Principle

> "Simple, predictable, and maintainable over clever."
