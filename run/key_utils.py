"""
Утилиты для работы с клавишами и предотвращения залипания клавиш в RDP.
Минимальная версия - только самое необходимое.
"""

import pyautogui
import time


def release_all_keys():
    """
    Освобождает все модификаторы, которые могли остаться зажатыми.
    Это предотвращает появление Input Capture Window overlay в RDP.
    """
    print("🔓 Освобождаю все зажатые клавиши...")
    keys = ['ctrl', 'shift', 'alt', 'win']
    for k in keys:
        try:
            pyautogui.keyUp(k)
            time.sleep(0.05)
        except Exception:
            pass
    
    # Дополнительная проверка
    for k in keys:
        try:
            pyautogui.keyUp(k)
        except:
            pass
    
    time.sleep(0.1)
    print("✅ Все клавиши освобождены")


def ensure_focus_and_wait(x=None, y=None, wait_time=0.6):
    """
    Гарантирует фокус на элементе и ждет достаточное время для RDP.
    
    Args:
        x, y: Координаты для клика (если None, клик не выполняется)
        wait_time: Время ожидания после клика (рекомендуется 0.6+ для RDP)
    """
    if x is not None and y is not None:
        print(f"🎯 Устанавливаю фокус на ({x}, {y})...")
        pyautogui.click(x, y)
    
    print(f"⏳ Жду {wait_time} сек для стабилизации фокуса в RDP...")
    time.sleep(wait_time)


def safe_hotkey(*keys, delay_before=0.1, delay_after=0.3):
    """
    Безопасное нажатие горячих клавиш с освобождением модификаторов.
    
    Args:
        *keys: Клавиши для hotkey (например, 'ctrl', 'c')
        delay_before: Задержка перед нажатием
        delay_after: Задержка после нажатия
    """
    time.sleep(delay_before)
    
    # Освобождаем клавиши перед нажатием
    release_all_keys()
    
    # Нажимаем горячие клавиши
    pyautogui.hotkey(*keys)
    
    time.sleep(delay_after)
    
    # Освобождаем клавиши после нажатия
    release_all_keys()


def stable_copy_text(x, y):
    """
    НАЙСТАБИЛЬНІШИЙ МЕТОД КОПІЮВАННЯ (RDP)
    Алгоритм:
    1. Освобождаем все клавиши
    2. Устанавливаем фокус с достаточным ожиданием
    3. Выделяем текст
    4. Копируем с освобождением клавиш
    5. Проверяем буфер обмена
    """
    print(f"\n📋 Стабильное копирование с позиции ({x}, {y})...")
    
    # 1. Освобождаем все клавиши
    release_all_keys()
    time.sleep(0.3)
    
    # 2. Гарантированный фокус
    ensure_focus_and_wait(x, y, wait_time=0.6)
    
    # 3. Выделяем текст (Ctrl+A)
    print("🎯 Выделяю текст (Ctrl+A)...")
    safe_hotkey('ctrl', 'a', delay_after=0.4)
    
    # 4. Копируем
    print("📋 Копирую текст (Ctrl+C)...")
    safe_hotkey('ctrl', 'c', delay_after=0.6)
    
    # 5. Проверяем буфер обмена
    try:
        from rdp_clipboard_fix import wait_for_clipboard_change
        result = wait_for_clipboard_change("", timeout=3.0)
    except ImportError:
        # Резервный вариант
        import pyperclip
        time.sleep(0.5)
        result = pyperclip.paste()
        if result:
            result = result.strip()
    
    if result and result.strip():
        print(f"✅ Текст успешно скопирован: '{result[:80]}{'...' if len(result) > 80 else ''}'")
        return result
    else:
        print("❌ Не удалось скопировать текст")
        return None


def wait_for_overlay_disappearance(timeout=2.0):
    """
    Ожидает исчезновения Input Capture Window overlay.
    В RDP overlay может появляться на короткое время.
    """
    print("👁️ Ожидаю исчезновения overlay...")
    time.sleep(0.5)
    release_all_keys()
    time.sleep(0.3)
    
    # Дополнительное ожидание для стабилизации
    start_time = time.time()
    while time.time() - start_time < timeout:
        release_all_keys()
        time.sleep(0.1)
    
    print("✅ Overlay должен был исчезнуть")


def disable_problematic_methods():
    """
    Отключает проблемные методы, которые создают overlay.
    Возвращает список методов, которые НЕ следует использовать.
    """
    problematic_methods = [
        "test_original_with_esc",  # Right click + esc
        "_do_right_esc_double",     # Right click + esc + double click
        "test_sendkeys_ctrl_a",     # SendKeys + pyautogui смешивание
        "test_sendkeys_select_all", # SendKeys + pyautogui смешивание
    ]
    
    print(f"🚫 Отключены проблемные методы: {', '.join(problematic_methods)}")
    return problematic_methods