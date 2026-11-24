# Password Generator

Криптостойкая генерация через secrets. Проверены комбинации наборов символов, длина, неверный ввод GUI и недоступный clipboard. В GUI допустимы длина 4–64 и количество 1–20. Копирование в проверке имитировалось, реальный буфер обмена не изменялся.

Требуется Python с Tkinter для GUI-проектов.

```bash
python -m pip install pyperclip
python password_gen.py
```

Проверка:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

GUI-тесты создают настоящие виджеты в скрытых окнах.
