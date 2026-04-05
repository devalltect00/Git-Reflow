---
# 🤝 Contributing Guide
---

Thank you for contributing to **Project Structure Generator**.

This project aims to provide a clean, professional CLI tool for generating repository documentation.

---

## 🧭 Principles

All contributions must follow:

- Simplicity
- Readability
- Maintainability
- Consistency

---

## 🧱 Project Architecture

```

app
├── cli.py
├── core/
├── services/
├── utils/

````

Each module has a **clear responsibility**. Avoid mixing concerns.

---

## 📝 Code Guidelines

### 1. Documentation (Required)

Every function must include:

```python
def example(arg: str) -> str:
    """
    Short description.

    Args:
        arg (str): Description

    Returns:
        str: Description

    Raises:
        ValueError: Description
    """
````

### 2. File-Level Docstring

Each file must start with:

```python
"""
Description of the module.
"""
```

---

### 3. Logging (NO print)

Always use:

```python
import logging
logger = logging.getLogger(__name__)
```

Examples:

```python
logger.info("Processing...")
logger.debug("Details: %s", data)
logger.error("Error occurred: %s", error)
```

---

### 4. CLI Behavior

* Must be consistent
* Must not break existing commands
* Must support config + CLI overrides

---

## 🧪 Testing

(Will be added in future phase)

* Add unit tests for new logic
* Ensure CLI commands work as expected

---

## 🔄 Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Implement changes
4. Add/update documentation
5. Submit Pull Request

---

## 📌 Notes

* Keep commits clean and meaningful
* Avoid unnecessary complexity
* Prefer explicit over implicit