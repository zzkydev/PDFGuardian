"""Password handling utilities."""
from utils.prompts import prompt_bool


def ask_password(prompt_text: str, allow_empty: bool = False) -> str:
    """
    Ask user for a password with option to allow empty passwords.

    Args:
        prompt_text: The prompt text to display
        allow_empty: Whether to allow empty password

    Returns:
        str: The password entered by user
    """
    try:
        # use getpass so password not echoed
        import getpass
        while True:
            pwd = getpass.getpass(prompt_text + ": ")
            if pwd == "" and not allow_empty:
                print("Password tidak boleh kosong. Jika ingin kosong ketik ulang dan pilih kosong dengan konfirmasi.")
                if prompt_bool("Tetap ingin password kosong (file akan dibuka tanpa password)?", False):
                    return ""
                else:
                    continue
            return pwd
    except Exception:
        # fallback to input
        pwd = input(prompt_text + ": ")
        return pwd
