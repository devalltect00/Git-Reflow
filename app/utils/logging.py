import logging

from rich.logging import RichHandler


def setup_logging(level=logging.INFO):
    """
    Setup rich logging.
    """
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[
            RichHandler(
                markup=True,
                rich_tracebacks=True,
                show_time=False,
                show_level=False,
            )
        ],
    )