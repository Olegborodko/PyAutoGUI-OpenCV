import time
import pyperclip
import pyautogui
import random

try:
    import win32clipboard
    HAS_WIN32CLIPBOARD = True
except ImportError:
    HAS_WIN32CLIPBOARD = False


def _read_clipboard_raw():
    """Читає буфер — win32clipboard надійніше для RDP."""
    if HAS_WIN32CLIPBOARD:
        try:
            win32clipboard.OpenClipboard()
            text = None
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
                text = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
            elif win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_TEXT):
                raw = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
                if isinstance(raw, bytes):
                    text = raw.decode('utf-8', errors='ignore')
            win32clipboard.CloseClipboard()
            return text
        except Exception:
            try:
                win32clipboard.CloseClipboard()
            except Exception:
                pass
    return pyperclip.paste()


def wait_for_clipboard_change(previous_content="", timeout=4.0, poll_interval=0.1):
    """
    КЛЮЧОВА ФУНКЦІЯ для RDP.
    Замість time.sleep(0.5) — чекаємо РЕАЛЬНОЇ зміни буфера.
    RDP синхронізує буфер із затримкою до 2 секунд, тому фіксований
    sleep ненадійний. Polling чекає скільки треба (але не більше timeout).
    """
    start = time.time()
    while (time.time() - start) < timeout:
        try:
            current = _read_clipboard_raw()
            if current and current.strip() and current != previous_content:
                return current.strip()
        except Exception:
            pass
        time.sleep(poll_interval)
    return None


def copy_text_from_coords_rdp(x, y):
    """
    Замінює copy_text_from_coords() у main.py для роботи через RDP.

    Алгоритм:
    1. Запам'ятовуємо поточний вміст буфера (snapshot)
    2. Виділяємо текст різними методами
    3. Після кожного Ctrl+C — polling поки буфер не зміниться
    4. Повертаємо новий текст або None
    """
    print(f"\n[RDP] Копіюю з ({x}, {y})...")
    pyautogui.moveTo(x, y, duration=random.uniform(0.15, 0.35))
    time.sleep(0.2)

    # Snapshot поточного буфера — щоб зрозуміти чи він змінився
    snapshot = _read_clipboard_raw() or ""
    print(f"   Поточний буфер: '{snapshot[:40]}...'" if len(snapshot) > 40 else f"   Поточний буфер: '{snapshot}'")

    methods = [
        ("triple_click",     _do_triple_click),
        ("ctrl_a",           _do_ctrl_a),
        ("home_shift_end",   _do_home_shift_end),
        ("right_esc_double", _do_right_esc_double),
        ("ctrl_shift_end",   _do_ctrl_shift_end),
    ]

    for name, action in methods:
        print(f"   -> Метод: {name}")
        action(x, y)
        pyautogui.hotkey('ctrl', 'c')

        result = wait_for_clipboard_change(snapshot, timeout=4.0)
        if result:
            print(f"   [OK] Текст: '{result[:80]}{'...' if len(result) > 80 else ''}'")
            return result

        print(f"   [--] {name} не дав результату")
        time.sleep(0.3)

    print("[FAIL] Жоден метод не спрацював")
    return None


def _do_triple_click(x, y):
    pyautogui.click(x, y, clicks=3, interval=0.12)
    time.sleep(0.15)

def _do_ctrl_a(x, y):
    pyautogui.click(x, y)
    time.sleep(0.15)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.15)

def _do_home_shift_end(x, y):
    pyautogui.click(x, y)
    time.sleep(0.15)
    pyautogui.press('home')
    time.sleep(0.1)
    pyautogui.hotkey('shift', 'end')
    time.sleep(0.15)

def _do_right_esc_double(x, y):
    pyautogui.click(x, y, button='right')
    time.sleep(0.1)
    pyautogui.press('esc')
    time.sleep(0.15)
    pyautogui.doubleClick(x, y)
    time.sleep(0.2)

def _do_ctrl_shift_end(x, y):
    pyautogui.click(x, y)
    time.sleep(0.15)
    pyautogui.hotkey('ctrl', 'home')
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'shift', 'end')
    time.sleep(0.15)


if __name__ == "__main__":
    print("Наведи курсор на поле з артикулом в RDP за 4 секунди...")
    time.sleep(4)
    x, y = pyautogui.position()
    result = copy_text_from_coords_rdp(x, y)
    print(f"\nРезультат: '{result}'" if result else "\nНе вдалося")