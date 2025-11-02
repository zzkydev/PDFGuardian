"""PDF library compatibility layer for PyPDF2 and pypdf."""
from __future__ import annotations

import sys
from typing import Any

# ---- Import PyPDF2 / pypdf compatible ----
PDFReader: Any = None
PDFWriter: Any = None
Permissions: Any = None
ImportSource: str | None = None

try:
    # Try PyPDF2 (common)
    from PyPDF2 import PdfReader as _PdfReader, PdfWriter as _PdfWriter
    try:
        from PyPDF2.constants import Permissions as _Permissions
    except Exception:
        _Permissions = None
    PDFReader = _PdfReader
    PDFWriter = _PdfWriter
    Permissions = _Permissions
    ImportSource = "PyPDF2"
except Exception:
    try:
        # Try pypdf (newer)
        from pypdf import PdfReader as _PdfReader, PdfWriter as _PdfWriter
        try:
            from pypdf import Permissions as _Permissions
        except Exception:
            _Permissions = None
        PDFReader = _PdfReader
        PDFWriter = _PdfWriter
        Permissions = _Permissions
        ImportSource = "pypdf"
    except Exception:
        print("Gagal mengimpor PyPDF2 atau pypdf. Install salah satu dengan:")
        print("  pip install PyPDF2")
        print("atau")
        print("  pip install pypdf")
        sys.exit(1)

# If library doesn't expose Permissions enum, we'll use fallback bitmasks.
PERM_FLAGS_AVAILABLE = Permissions is not None

# Common permission bitmask approximations (library/version dependent)
PERM_PRINT = 0x0004
PERM_MODIFY_CONTENTS = 0x0008
PERM_COPY = 0x0010  # some libs use 0x0020; heuristic
PERM_MODIFY_ANNOTATIONS = 0x0020
PERM_FILL_FORM = 0x0100
PERM_ACCESSIBILITY = 0x0200
PERM_PRINT_HIGH = 0x0800
