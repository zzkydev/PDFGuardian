"""User prompt utilities for getting input from user."""
from __future__ import annotations


def prompt_bool(label: str, default: bool | None = None) -> bool:
    """
    Prompt user for a boolean (yes/no) answer.

    Args:
        label: The question to ask the user
        default: Default answer if user presses Enter (None means no default)

    Returns:
        bool: User's answer as True or False
    """
    while True:
        if default is True:
            suffix = " [Y/n]: "
        elif default is False:
            suffix = " [y/N]: "
        else:
            suffix = " [y/n]: "
        ans = input(f"{label}{suffix}").strip().lower()
        if ans == "" and default is not None:
            return default
        if ans in ("y", "yes", "ya"):
            return True
        if ans in ("n", "no", "tidak"):
            return False
        print("Masukan tidak dikenal. Jawab dengan y/yes atau n/no.")


def human_bool(b: bool) -> str:
    """
    Convert boolean to human-readable Indonesian string.

    Args:
        b: Boolean value to convert

    Returns:
        str: "diizinkan" if True, "dilarang" if False
    """
    return "diizinkan" if b else "dilarang"
