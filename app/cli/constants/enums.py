# app/cli/constants/enums.py

from enum import Enum


class LogLevelChoices(str, Enum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            value = value.upper()
            for member in cls:
                if member.value == value:
                    return member


class InitMode(str, Enum):
    ALL = "all"
    CONFIG = "config"


class ProfileChoices(str, Enum):
    DEFAULT = "default"
    MINIMAL = "minimal"
    DETAILED = "detailed"


class ProjectTypeChoices(str, Enum):
    AUTO = "auto"

    GENERIC = "generic"

    PYTHON = "python"
    DJANGO = "django"
    FLASK = "flask"
    FASTAPI = "fastapi"

    NODEJS = "nodejs"
    REACTJS = "reactjs"
    NEXTJS = "nextjs"
