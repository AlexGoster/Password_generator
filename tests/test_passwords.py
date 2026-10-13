import importlib.util
import itertools
from pathlib import Path
import string
import tkinter as tk

import pytest

spec = importlib.util.spec_from_file_location("password_gui", Path(__file__).parents[1] / "password_gen.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_character_options():
    for digits, specials, upper in itertools.product([False, True], repeat=3):
        for length in (4, 12, 64):
            password = module.generate_password(length, digits, specials, upper)
            assert len(password) == length
            assert any(c in string.ascii_lowercase for c in password)
            assert any(c.isdigit() for c in password) == digits
            assert any(c in string.ascii_uppercase for c in password) == upper
            assert any(c not in string.ascii_letters + string.digits for c in password) == specials
    with pytest.raises(ValueError):
        module.generate_password(3)


def test_invalid_widget_input_and_clipboard_failure(monkeypatch):
    errors = []
    monkeypatch.setattr(module.messagebox, "showerror", lambda *args: errors.append(args))
    root = tk.Tk()
    root.withdraw()
    try:
        app = module.PasswordGenApp(root)
        app.length_var.set("invalid")
        app.generate()
        assert errors
        app.length_var.set(12)
        app.count_var.set(-1)
        app.generate()
        assert len(errors) == 2
        app.count_var.set(1)
        app.generate()
        assert len(app.result_text.get("1.0", tk.END).strip()) == 12
        def fail(_):
            raise module.pyperclip.PyperclipException("Clipboard unavailable")
        monkeypatch.setattr(module.pyperclip, "copy", fail)
        app.copy_to_clipboard()
        assert len(errors) == 3
    finally:
        root.destroy()
