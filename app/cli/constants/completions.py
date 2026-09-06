# app/cli/constants/completions.py


def completion_initialization_mode():
    return ["all", "config"]


def completion_target_directory():
    return ["."]


def completion_profile_choices():
    return ["default", "minimal", "detailed"]


def completion_output_choices():
    return ["docs/project_structure.md"]
