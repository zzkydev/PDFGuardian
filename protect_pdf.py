"""Main entry point for PDF protection tool."""
from __future__ import annotations

import sys
from pathlib import Path

from utils.prompts import prompt_bool
from utils.password import ask_password
from pdf.permissions import ask_permissions
from pdf.encrypt import encrypt_pdf, validate_pdf


def get_output_path(input_path: Path) -> Path:
    """
    Determine output path for protected PDF, handling existing files.

    Args:
        input_path: Input PDF file path

    Returns:
        Path: Output file path
    """
    out_name = f"protected_{input_path.name}"
    out_path = Path.cwd() / out_name

    # If file exists, ask overwrite
    if out_path.exists():
        if not prompt_bool(f"File {out_path} sudah ada. Timpa?", False):
            # Build an alternate name
            i = 1
            while True:
                alt = Path.cwd() / f"protected_{i}_{input_path.name}"
                if not alt.exists():
                    out_path = alt
                    break
                i += 1

    return out_path


def main() -> None:
    """Main function to protect PDF with password and permissions."""
    print("=== Proteksi Permission PDF (+ password user & owner) ===")
    pdf_path = input("Masukkan path file PDF: ").strip().strip('"').strip("'")

    if not pdf_path:
        print("Path kosong.")
        sys.exit(1)

    p = Path(pdf_path)

    if p.suffix.lower() != ".pdf":
        print("ini bukan format pdf")
        sys.exit(1)

    if not p.exists():
        print("File tidak ditemukan.")
        sys.exit(1)

    # Validate PDF
    if not validate_pdf(p):
        print("File tidak dapat dibuka sebagai PDF.")
        sys.exit(1)

    # Get permission settings
    permissions = ask_permissions()

    # Get password settings
    print("\n=== Password settings ===")
    print("User password: diperlukan agar file hanya bisa dibuka jika mengisi password.")
    print("Owner password: diperlukan agar permission/setting dapat diubah (harus diisi).")
    user_pwd = ask_password(
        "Masukkan user password (kosong = file bisa dibuka tanpa password)",
        allow_empty=True
    )
    owner_pwd = ask_password(
        "Masukkan owner password (wajib, jangan lupa simpan)",
        allow_empty=False
    )

    if owner_pwd == "":
        print("Owner password tidak boleh kosong.")
        sys.exit(1)

    # Display summary
    permissions.display_summary()
    print(f"- User password: {'ada' if user_pwd else 'tidak ada (file dapat dibuka tanpa password)'}")
    print(f"- Owner password: diset (tidak ditampilkan)")

    if not prompt_bool("\nLanjutkan dan terapkan pengaturan ini?", True):
        print("Dibatalkan.")
        sys.exit(0)

    # Get output path
    out_path = get_output_path(p)

    # Encrypt the PDF
    try:
        encrypt_pdf(p, out_path, user_pwd, owner_pwd, permissions)
    except Exception as e:
        print(f"Gagal menyimpan file: {e}")
        sys.exit(1)

    print(f"\nBerhasil! File tersimpan: {out_path}")
    print("\nCatatan penting:")
    print("- Permission PDF bersifat 'advisory' dan bisa di-bypass oleh beberapa PDF reader/alat.")
    print("- Untuk proteksi sangat sensitif, gunakan DRM atau viewer terkendali.")
    print("- Simpan owner password dengan aman; tanpa owner password, setting bisa diubah.")
    print("- User password diperlukan agar file hanya bisa dibuka setelah memasukkan password.")


if __name__ == "__main__":
    main()
