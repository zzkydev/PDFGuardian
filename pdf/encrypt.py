"""PDF encryption functionality."""
from __future__ import annotations

from pathlib import Path

from pdf.compatibility import PDFReader, PDFWriter, PERM_FLAGS_AVAILABLE
from pdf.permissions import PermissionConfig


def encrypt_pdf(
    input_path: Path,
    output_path: Path,
    user_password: str,
    owner_password: str,
    permissions: PermissionConfig,
) -> None:
    """
    Encrypt a PDF file with specified passwords and permissions.

    Args:
        input_path: Path to input PDF file
        output_path: Path to output encrypted PDF file
        user_password: User password (can be empty for no open password)
        owner_password: Owner password (required, cannot be empty)
        permissions: Permission configuration

    Raises:
        Exception: If PDF cannot be read or written
    """
    # Read the input PDF
    reader = PDFReader(str(input_path))

    # Touch pages to ensure readable
    if len(reader.pages) > 0:
        _ = reader.pages[0]

    # Create writer and add all pages
    writer = PDFWriter()
    for page in reader.pages:
        writer.add_page(page)

    # Apply encryption with permissions
    if PERM_FLAGS_AVAILABLE:
        _encrypt_with_permission_set(writer, user_password, owner_password, permissions)
    else:
        _encrypt_with_permission_flag(writer, user_password, owner_password, permissions)

    # Write the encrypted PDF
    with open(output_path, "wb") as f:
        writer.write(f)


def _encrypt_with_permission_set(
    writer: PDFWriter,
    user_pwd: str,
    owner_pwd: str,
    permissions: PermissionConfig,
) -> None:
    """
    Encrypt using modern permission set API.

    Args:
        writer: PDF writer instance
        user_pwd: User password
        owner_pwd: Owner password
        permissions: Permission configuration
    """
    allowed = permissions.to_permission_set()

    try:
        # modern API: keyword args
        writer.encrypt(
            user_password=user_pwd,
            owner_password=owner_pwd,
            permissions=allowed,
        )
    except TypeError:
        # older signatures may be positional
        try:
            writer.encrypt(user_pwd, owner_pwd, permissions=allowed)
        except Exception:
            # fallback: try without permissions (still sets passwords)
            writer.encrypt(user_pwd, owner_pwd)


def _encrypt_with_permission_flag(
    writer: PDFWriter,
    user_pwd: str,
    owner_pwd: str,
    permissions: PermissionConfig,
) -> None:
    """
    Encrypt using fallback integer bitmask for permissions.

    Args:
        writer: PDF writer instance
        user_pwd: User password
        owner_pwd: Owner password
        permissions: Permission configuration
    """
    permissions_flag = permissions.to_permission_flag()

    try:
        writer.encrypt(user_pwd, owner_pwd, use_128bit=True, permissions_flag=permissions_flag)
    except TypeError:
        try:
            writer.encrypt(user_pwd, owner_pwd, use_128bit=True)
        except Exception:
            writer.encrypt(user_pwd, owner_pwd)


def validate_pdf(pdf_path: Path) -> bool:
    """
    Validate that a file is a readable PDF.

    Args:
        pdf_path: Path to PDF file

    Returns:
        bool: True if valid and readable, False otherwise
    """
    try:
        reader = PDFReader(str(pdf_path))
        # Try to access first page
        if len(reader.pages) > 0:
            _ = reader.pages[0]
        return True
    except Exception:
        return False
