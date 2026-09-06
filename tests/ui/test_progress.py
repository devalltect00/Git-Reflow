# tests/ui/test_progress.py

"""Unit tests for reusable Rich progress helpers."""

from unittest.mock import MagicMock

import pytest
from rich.progress import Progress

from app.ui import progress


class DummyProgress:
    """Minimal Rich Progress replacement used for lifecycle assertions."""

    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
        self.add_task = MagicMock(return_value=123)
        self.update = MagicMock()
        self.advance = MagicMock()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback) -> bool:
        return False


def test_create_progress_returns_progress_instance() -> None:
    """Create a configured Rich progress instance."""

    assert isinstance(progress.create_progress(), Progress)


def test_create_progress_uses_shared_console_and_enabled_state(monkeypatch) -> None:
    """Use the shared console and map configuration to Rich's disable flag."""

    captured: dict[str, object] = {}

    def fake_progress(*args, **kwargs):
        captured["args"] = args
        captured["kwargs"] = kwargs
        return DummyProgress(*args, **kwargs)

    monkeypatch.setattr(progress, "Progress", fake_progress)

    progress.create_progress(enabled=False)

    assert captured["kwargs"]["console"] is progress.console
    assert captured["kwargs"]["disable"] is True
    assert captured["args"][0].__class__.__name__ == "SpinnerColumn"
    assert captured["args"][2].__class__.__name__ == "BarColumn"


def test_progress_spinner_tracks_lifecycle_and_enabled_state(monkeypatch) -> None:
    """Create a transient spinner and mark successful work complete."""

    captured: dict[str, object] = {}

    def fake_progress(*args, **kwargs):
        captured["kwargs"] = kwargs
        dummy = DummyProgress(*args, **kwargs)
        captured["progress"] = dummy
        return dummy

    monkeypatch.setattr(progress, "Progress", fake_progress)

    with progress.progress_spinner("Cloning", enabled=False):
        pass

    dummy = captured["progress"]
    dummy.add_task.assert_called_once_with(description="Cloning", total=None)
    dummy.update.assert_called_once_with(123, description="Cloning complete")
    assert captured["kwargs"]["transient"] is True
    assert captured["kwargs"]["disable"] is True


def test_progress_task_tracks_determinate_work(monkeypatch) -> None:
    """Expose description and advancement controls for determinate work."""

    dummy = DummyProgress()
    factory = MagicMock(return_value=dummy)
    monkeypatch.setattr(progress, "create_progress", factory)

    with progress.progress_task(
        "Preparing conversion",
        total=3,
        enabled=False,
    ) as task:
        task.update("Discovering tags")
        task.advance()

    factory.assert_called_once_with(enabled=False)
    dummy.add_task.assert_called_once_with(
        description="Preparing conversion",
        total=3,
    )
    dummy.advance.assert_called_once_with(123, 1)
    assert dummy.update.call_args_list[0].kwargs == {"description": "Discovering tags"}
    assert dummy.update.call_args_list[-1].kwargs == {
        "completed": 3,
        "description": "Preparing conversion complete",
    }


def test_progress_task_preserves_exceptions(monkeypatch) -> None:
    """Close the display without hiding or falsely completing failures."""

    dummy = DummyProgress()
    monkeypatch.setattr(
        progress,
        "create_progress",
        MagicMock(return_value=dummy),
    )

    with pytest.raises(RuntimeError, match="conversion failed"):
        with progress.progress_task("Preparing conversion", total=1):
            raise RuntimeError("conversion failed")

    dummy.update.assert_not_called()
