"""PDF permissions configuration."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Set, Any

from utils.prompts import prompt_bool, human_bool
from pdf.compatibility import (
    PERM_FLAGS_AVAILABLE,
    Permissions,
    PERM_PRINT,
    PERM_MODIFY_CONTENTS,
    PERM_COPY,
    PERM_MODIFY_ANNOTATIONS,
    PERM_FILL_FORM,
    PERM_ACCESSIBILITY,
    PERM_PRINT_HIGH,
)


@dataclass
class PermissionConfig:
    """Configuration for PDF permissions."""
    allow_comments: bool
    allow_copy: bool
    allow_accessibility: bool
    allow_edit: bool
    allow_fill: bool
    allow_print: bool
    allow_sign: bool

    def display_summary(self) -> None:
        """Display a summary of permission settings."""
        print("\n=== Ringkasan Pengaturan Permissions ===")
        print(f"- Komentar/Annotasi: {human_bool(self.allow_comments)}")
        print(f"- Content Copying: {human_bool(self.allow_copy)}")
        print(f"- Copy for Accessibility: {human_bool(self.allow_accessibility)}")
        print(f"- Editing Konten: {human_bool(self.allow_edit)}")
        print(f"- Filling Form Fields: {human_bool(self.allow_fill)}")
        print(f"- Print: {human_bool(self.allow_print)}")
        print(f"- Signing (aproksimasi): {human_bool(self.allow_sign)}")

    def to_permission_set(self) -> Set[Any] | None:
        """
        Convert config to permission set for modern PDF libraries.

        Returns:
            Set of permission flags or None if not available
        """
        if not PERM_FLAGS_AVAILABLE:
            return None

        allowed = set()
        if self.allow_comments:
            if hasattr(Permissions, "MODIFY_ANNOTATIONS"):
                allowed.add(Permissions.MODIFY_ANNOTATIONS)
        if self.allow_sign:
            for perm_name in ("MODIFY_ANNOTATIONS", "FILL_FORM"):
                if hasattr(Permissions, perm_name):
                    allowed.add(getattr(Permissions, perm_name))
        if self.allow_copy and hasattr(Permissions, "COPY"):
            allowed.add(Permissions.COPY)
        if self.allow_accessibility and hasattr(Permissions, "ACCESSIBILITY"):
            allowed.add(Permissions.ACCESSIBILITY)
        if self.allow_edit and hasattr(Permissions, "MODIFY_CONTENTS"):
            allowed.add(Permissions.MODIFY_CONTENTS)
        if self.allow_fill and hasattr(Permissions, "FILL_FORM"):
            allowed.add(Permissions.FILL_FORM)
        if self.allow_print:
            if hasattr(Permissions, "PRINT"):
                allowed.add(Permissions.PRINT)
            if hasattr(Permissions, "PRINT_HIGH"):
                allowed.add(Permissions.PRINT_HIGH)

        return allowed if allowed else None

    def to_permission_flag(self) -> int:
        """
        Convert config to permission bitmask for older PDF libraries.

        Returns:
            Integer bitmask representing permissions
        """
        permissions_flag = 0
        if self.allow_comments:
            permissions_flag |= PERM_MODIFY_ANNOTATIONS
        if self.allow_sign:
            permissions_flag |= (PERM_MODIFY_ANNOTATIONS | PERM_FILL_FORM)
        if self.allow_copy:
            permissions_flag |= PERM_COPY
        if self.allow_accessibility:
            permissions_flag |= PERM_ACCESSIBILITY
        if self.allow_edit:
            permissions_flag |= PERM_MODIFY_CONTENTS
        if self.allow_fill:
            permissions_flag |= PERM_FILL_FORM
        if self.allow_print:
            permissions_flag |= (PERM_PRINT | PERM_PRINT_HIGH)

        return permissions_flag


def ask_permissions() -> PermissionConfig:
    """
    Interactively ask user for permission settings.

    Returns:
        PermissionConfig: Configuration based on user responses
    """
    print("\n=== Menu Izin (permissions) ===")
    allow_comments = prompt_bool("Izinkan komentar/annotasi?", False)
    allow_copy = prompt_bool("Content copying diizinkan?", False)
    allow_accessibility = prompt_bool("Content copy for accessibility diizinkan?", True)
    allow_edit = prompt_bool("Editing konten diizinkan?", False)
    allow_fill = prompt_bool("Filling form fields diizinkan?", True)
    allow_print = prompt_bool("Print diizinkan?", True)
    allow_sign = prompt_bool("Signing diizinkan? (aproksimasi via annotasi & form)", False)

    return PermissionConfig(
        allow_comments=allow_comments,
        allow_copy=allow_copy,
        allow_accessibility=allow_accessibility,
        allow_edit=allow_edit,
        allow_fill=allow_fill,
        allow_print=allow_print,
        allow_sign=allow_sign,
    )
