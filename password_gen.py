import secrets
import string
import tkinter as tk
from tkinter import messagebox
import pyperclip


def generate_password(length=12, use_digits=True, use_specials=True, use_uppercase=True):
    if length < 4:
        raise ValueError("Длина пароля должна быть не менее 4 символов.")

    lower = string.ascii_lowercase
    upper = string.ascii_uppercase if use_uppercase else ""
    digits = string.digits if use_digits else ""
    specials = "!@#$%^&*()_+-=[]{}|;:,.<>?/" if use_specials else ""

    all_chars = lower + upper + digits + specials
    if not all_chars:
        raise ValueError("Не выбрано ни одного набора символов.")

    password = []
    if use_uppercase:
        password.append(secrets.choice(upper))
    if use_digits:
        password.append(secrets.choice(digits))
    if use_specials:
        password.append(secrets.choice(specials))
    password.append(secrets.choice(lower))

    remaining_length = length - len(password)
    password.extend(secrets.choice(all_chars) for _ in range(remaining_length))

    secrets.SystemRandom().shuffle(password)
    return ''.join(password)


class PasswordGenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор паролей")
        self.root.resizable(False, False)

        tk.Label(root, text="Длина пароля:").grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
        self.length_var = tk.IntVar(value=12)
        tk.Spinbox(root, from_=4, to=64, textvariable=self.length_var, width=5).grid(row=0, column=1, padx=10, pady=(10, 0))

        tk.Label(root, text="Количество:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.count_var = tk.IntVar(value=1)
        tk.Spinbox(root, from_=1, to=20, textvariable=self.count_var, width=5).grid(row=1, column=1, padx=10, pady=5)

        self.digits_var = tk.BooleanVar(value=True)
        self.specials_var = tk.BooleanVar(value=True)
        self.uppercase_var = tk.BooleanVar(value=True)

        tk.Checkbutton(root, text="Цифры", variable=self.digits_var).grid(row=2, column=0, sticky="w", padx=10)
        tk.Checkbutton(root, text="Спецсимволы", variable=self.specials_var).grid(row=2, column=1, sticky="w")
        tk.Checkbutton(root, text="Заглавные буквы", variable=self.uppercase_var).grid(row=3, column=0, columnspan=2, sticky="w", padx=10)

        tk.Button(root, text="Сгенерировать", command=self.generate, width=20).grid(row=4, column=0, columnspan=2, pady=10)

        self.result_text = tk.Text(root, height=10, width=40, font=("Consolas", 12))
        self.result_text.grid(row=5, column=0, columnspan=2, padx=10, pady=(0, 10))

        tk.Button(root, text="Копировать", command=self.copy_to_clipboard, width=20).grid(row=6, column=0, columnspan=2, pady=(0, 10))

    def generate(self):
        try:
            length = self.length_var.get()
            count = self.count_var.get()
            if not 4 <= length <= 64 or not 1 <= count <= 20:
                raise ValueError("Длина: 4–64 символа; количество: 1–20 паролей.")
            self.result_text.delete("1.0", tk.END)
            for _ in range(count):
                pwd = generate_password(
                    length=length,
                    use_digits=self.digits_var.get(),
                    use_specials=self.specials_var.get(),
                    use_uppercase=self.uppercase_var.get()
                )
                self.result_text.insert(tk.END, pwd + "\n")
        except (ValueError, tk.TclError) as e:
            messagebox.showerror("Ошибка", str(e))

    def copy_to_clipboard(self):
        text = self.result_text.get("1.0", tk.END).strip()
        if text:
            try:
                pyperclip.copy(text)
            except pyperclip.PyperclipException as exc:
                messagebox.showerror("Ошибка", f"Буфер обмена недоступен: {exc}")
                return
            messagebox.showinfo("Скопировано", "Пароль скопирован в буфер обмена!")
        else:
            messagebox.showwarning("Внимание", "Нет пароля для копирования.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenApp(root)
    root.mainloop()
