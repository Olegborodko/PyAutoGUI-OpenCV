import pyautogui
import pyperclip
import time
import random

# ─────────────────────────────────────────────
# Вспомогательные функции
# ─────────────────────────────────────────────

def random_sleep(a=0.1, b=0.4):
    time.sleep(random.uniform(a, b))


def _clear_clipboard(retries=3):
    """Очищает буфер обмена и проверяет что он действительно пуст."""
    for _ in range(retries):
        try:
            pyperclip.copy("")
            time.sleep(0.15)
            if pyperclip.paste() == "":
                return True
        except Exception:
            time.sleep(0.2)
    return False


def _wait_for_clipboard_change(timeout=2.0, interval=0.1):
    """
    Ждёт пока в буфере появится непустой текст.
    Возвращает текст или None если timeout истёк.
    """
    elapsed = 0.0
    while elapsed < timeout:
        time.sleep(interval)
        elapsed += interval
        try:
            current = pyperclip.paste()
            if current and current.strip():
                return current
        except Exception:
            pass
    return None


def _do_copy(method):
    """
    Выделяет текст указанным методом и копирует через Ctrl+C.
    БЕЗ нажатия Esc — чтобы не сбрасывать состояние формы/страницы.
    """
    try:
        if method == "home_shift_end":
            pyautogui.press("home")
            time.sleep(0.08)
            pyautogui.hotkey("shift", "end")

        elif method == "ctrl_a":
            pyautogui.hotkey("ctrl", "a")

        elif method == "double_click":
            pyautogui.doubleClick()

        elif method == "triple_click":
            pyautogui.click(clicks=3, interval=0.08)

        time.sleep(0.2)
        pyautogui.hotkey("ctrl", "c")

    except Exception as e:
        print(f"      ⚠️ _do_copy({method}): {e}")


# ─────────────────────────────────────────────
# Основная функция копирования
# ─────────────────────────────────────────────

def _copy_at_current_position(max_attempts=3):
    """
    Пытается скопировать текст в текущей позиции курсора.
    Методы — от самого безопасного к агрессивному.
    Каждый метод пробуется max_attempts раз.
    Возвращает текст или None.
    """
    methods = [
        ("home_shift_end", "Home + Shift+End"),  # ✅ безопасно для строки ввода
        ("ctrl_a",         "Ctrl+A"),            # ✅ безопасно если фокус в поле
        ("double_click",   "Двойной клик"),      # ⚠️ выделяет одно слово
        ("triple_click",   "Тройной клик"),      # ⚠️ последний — самый агрессивный
    ]

    for method_id, method_name in methods:
        print(f"   [{method_name}]")

        for attempt in range(1, max_attempts + 1):
            print(f"      Попытка {attempt}/{max_attempts}...")

            # Очищаем буфер перед попыткой
            if not _clear_clipboard():
                print("      ⚠️ Буфер не очистился, продолжаю...")

            # Выделяем и копируем
            _do_copy(method_id)

            # Ждём появления текста в буфере
            text = _wait_for_clipboard_change(timeout=1.5)

            if text:
                text = text.strip()
                if text:
                    print(f"      ✅ Получено: '{text[:80]}{'...' if len(text) > 80 else ''}'")
                    return text

            print(f"      — Буфер пуст")
            time.sleep(0.3 * attempt)  # пауза растёт с каждой неудачной попыткой

        print(f"   ✗ {method_name} не дал результата")

    return None


# ─────────────────────────────────────────────
# Публичные функции (используются в main.py)
# ─────────────────────────────────────────────

def copy_text_from_position(x, y):
    """
    Перемещает курсор к (x, y), один клик для фокуса,
    затем читает текст через буфер обмена.
    Возвращает текст или None.
    """
    try:
        print(f"\n📋 Читаю текст с позиции ({x}, {y})...")

        # Сохраняем буфер чтобы восстановить после
        try:
            saved_clipboard = pyperclip.paste()
        except Exception:
            saved_clipboard = ""

        # Плавно перемещаемся и кликаем один раз — только для фокуса
        pyautogui.moveTo(x, y, duration=random.uniform(0.15, 0.35))
        time.sleep(0.2)
        pyautogui.click(x, y)
        time.sleep(0.4)  # даём полю время получить фокус

        result = _copy_at_current_position()

        # Восстанавливаем буфер
        try:
            pyperclip.copy(saved_clipboard)
        except Exception:
            pass

        if result:
            print(f"✅ Текст успешно получен!")
        else:
            print(f"❌ Не удалось прочитать текст")

        return result

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None


def copy_text_without_clipboard(x, y, width=300, height=80):
    """
    Обёртка для совместимости с main.py.
    Возвращает None — чтобы main.py перешёл к copy_text_from_position.
    """
    return None


def select_and_delete_from_position(x, y):
    """
    Переходит к полю и удаляет его содержимое.
    Использует Home+Shift+End для безопасного выделения.
    Возвращает True при успехе.
    """
    try:
        print(f"\n🗑️ Удаляю текст в позиции ({x}, {y})...")

        pyautogui.moveTo(x, y, duration=random.uniform(0.15, 0.35))
        time.sleep(0.2)
        pyautogui.click(x, y)
        time.sleep(0.4)

        # Только безопасные методы выделения — без Esc, без тройного клика
        for method_id, method_name in [
            ("home_shift_end", "Home + Shift+End"),
            ("ctrl_a",         "Ctrl+A"),
        ]:
            try:
                if method_id == "home_shift_end":
                    pyautogui.press("home")
                    time.sleep(0.08)
                    pyautogui.hotkey("shift", "end")
                elif method_id == "ctrl_a":
                    pyautogui.hotkey("ctrl", "a")

                time.sleep(0.15)
                pyautogui.press("backspace")  # backspace безопаснее delete
                time.sleep(0.1)
                print(f"   ✅ Удалено ({method_name})")
                return True
            except Exception as e:
                print(f"   ⚠️ {method_name}: {e}")

        print("❌ Не удалось удалить текст")
        return False

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


def paste_text(text_to_paste):
    """
    Вставляет текст в активное поле.
    Ctrl+V — главный метод (работает с Unicode и кириллицей).
    write() — fallback только для ASCII.
    """
    if not text_to_paste:
        print("❌ Пустой текст для вставки")
        return False

    print("📋 Вставляю текст...")

    # Метод 1: Ctrl+V через буфер (работает с любым текстом)
    try:
        pyperclip.copy(text_to_paste)
        time.sleep(0.15)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.2)
        print("✅ Вставлено через Ctrl+V")
        return True
    except Exception as e:
        print(f"   ❌ Ctrl+V: {e}")

    # Метод 2: write() — только ASCII, без спецсимволов
    try:
        pyautogui.write(text_to_paste, interval=0.02)
        time.sleep(0.1)
        print("✅ Вставлено через write()")
        return True
    except Exception as e:
        print(f"   ❌ write(): {e}")

    print("❌ Не удалось вставить текст")
    return False
