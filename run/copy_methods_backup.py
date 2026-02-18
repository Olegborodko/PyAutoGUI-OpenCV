"""
Файл-бэкап всех методов копирования текста.
Содержит все методы, которые были в run.py, rdp_clipboard_fix.py, text_utils.py, uia_method.py.
Используется для сохранения кода на случай, если понадобится вернуться к какому-то методу.
"""

import time
import pyautogui
import pyperclip
import random

try:
    import win32clipboard
    HAS_WIN32CLIPBOARD = True
except ImportError:
    HAS_WIN32CLIPBOARD = False

try:
    import win32com.client
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

try:
    import uiautomation as auto
    HAS_UIA = True
except ImportError:
    HAS_UIA = False

# ========== ФУНКЦИИ ИЗ RUN.PY ==========

def clear_clipboard():
    """Очистити буфер обміну (покращена версія для RDP)"""
    try:
        if HAS_WIN32CLIPBOARD:
            try:
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.CloseClipboard()
                time.sleep(0.3)
                return True
            except Exception as e:
                print(f"⚠️ Помилка очищення буфера через win32clipboard: {e}")
        
        pyperclip.copy('')
        time.sleep(0.4)
        if pyperclip.paste() == '':
            return True
        else:
            pyperclip.copy('')
            time.sleep(0.6)
            return pyperclip.paste() == ''
    except Exception as e:
        print(f"⚠️ Помилка очищення буфера: {e}")
        return False

def check_clipboard():
    """Перевірити буфер обміну та повернути текст (покращена версія для RDP)"""
    time.sleep(0.3)
    
    if HAS_WIN32CLIPBOARD:
        try:
            win32clipboard.OpenClipboard()
            
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
                try:
                    text = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
                    if text and text.strip():
                        text = text.strip()
                        preview = text[:50] + "..." if len(text) > 50 else text
                        print(f"✅ Текст отримано (Unicode): '{preview}'")
                        win32clipboard.CloseClipboard()
                        return text
                except Exception as e:
                    print(f"⚠️ Помилка читання Unicode формату: {e}")
            
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_TEXT):
                try:
                    text = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
                    if text and text.strip():
                        if isinstance(text, bytes):
                            try:
                                text = text.decode('utf-8')
                            except:
                                text = text.decode('cp1251', errors='ignore')
                        
                        text = text.strip()
                        preview = text[:50] + "..." if len(text) > 50 else text
                        print(f"✅ Текст отримано (ANSI): '{preview}'")
                        win32clipboard.CloseClipboard()
                        return text
                except Exception as e:
                    print(f"⚠️ Помилка читання ANSI формату: {e}")
            
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_OEMTEXT):
                try:
                    text = win32clipboard.GetClipboardData(win32clipboard.CF_OEMTEXT)
                    if text and text.strip():
                        if isinstance(text, bytes):
                            try:
                                text = text.decode('cp866')
                            except:
                                text = text.decode('cp1251', errors='ignore')
                        
                        text = text.strip()
                        preview = text[:50] + "..." if len(text) > 50 else text
                        print(f"✅ Текст отримано (OEM): '{preview}'")
                        win32clipboard.CloseClipboard()
                        return text
                except Exception as e:
                    print(f"⚠️ Помилка читання OEM формату: {e}")
            
            win32clipboard.CloseClipboard()
            
        except Exception as e:
            print(f"⚠️ Помилка роботи з win32clipboard: {e}")
            try:
                win32clipboard.CloseClipboard()
            except:
                pass
    
    try:
        text = pyperclip.paste()
        if text and text.strip():
            text = text.strip()
            preview = text[:50] + "..." if len(text) > 50 else text
            print(f"✅ Текст отримано (pyperclip): '{preview}'")
            return text
        else:
            print("❌ Буфер обміну порожній")
            return None
    except Exception as e:
        print(f"❌ Помилка буфера обміну: {e}")
        return None

def test_original_with_esc(x, y):
    """Метод 1: Оригінальний метод, який працював (з Esc)"""
    print("\n🧪 Метод 1: Оригінальний метод (з Esc)")
    
    pyautogui.click(button='right')
    time.sleep(0.05)
    pyautogui.press('esc')
    time.sleep(0.05)
    
    pyautogui.doubleClick()
    time.sleep(0.2)
    
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)
    
    return check_clipboard()

def test_triple_click_only(x, y):
    """Метод 3: Тільки потрійний клік"""
    print("\n🧪 Метод 3: Тільки потрійний клік")
    
    pyautogui.click(clicks=3, interval=0.1)
    time.sleep(0.4)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)
    
    return check_clipboard()

def test_ctrl_a_only(x, y):
    """Метод 4: Тільки Ctrl+A"""
    print("\n🧪 Метод 4: Тільки Ctrl+A")
    
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.4)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)
    
    return check_clipboard()

def test_sendkeys_ctrl_a(x, y):
    """Метод 8: SendKeys Ctrl+A"""
    if not HAS_WIN32:
        print("❌ Бібліотека win32com не встановлена")
        return None
    
    print("\n🧪 Метод 8: SendKeys Ctrl+A")
    
    pyautogui.click()
    time.sleep(0.3)
    
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys("^a")
    time.sleep(0.3)
    shell.SendKeys("^c")
    time.sleep(0.3)
    
    return check_clipboard()

def test_sendkeys_select_all(x, y):
    """Метод 9: SendKeys виділення"""
    if not HAS_WIN32:
        print("❌ Бібліотека win32com не встановлена")
        return None
    
    print("\n🧪 Метод 9: SendKeys виділення")
    
    time.sleep(0.5)
    
    pyautogui.click()
    time.sleep(0.5)
    
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys("{HOME}")
    time.sleep(0.2)
    shell.SendKeys("+{END}")
    time.sleep(0.5)
    shell.SendKeys("^c")
    time.sleep(0.5)
    
    return check_clipboard()

# ========== ФУНКЦИИ ИЗ RDP_CLIPBOARD_FIX.PY ==========

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
    """
    print(f"\n[RDP] Копіюю з ({x}, {y})...")
    pyautogui.moveTo(x, y, duration=random.uniform(0.15, 0.35))
    time.sleep(0.2)

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

# ========== ФУНКЦИИ ИЗ TEXT_UTILS.PY ==========

def select_and_copy_text():
    """
    Виділяє та копіює текст з поточної позиції курсора.
    """
    try:
        print("📋 Виділяю та копіюю текст...")
        
        x, y = pyautogui.position()
        print(f"   Курсор: ({x}, {y})")
        
        try:
            original_clipboard = pyperclip.paste()
        except:
            original_clipboard = ""
        
        methods = [
            ("ctrl_a", "Ctrl+A", 0.3),
            ("double_click", "Подвійний клік", 0.4),
            ("triple_click", "Потрійний клік", 0.5),
            ("home_shift_end", "Home+Shift+End", 0.3),
        ]
        
        for method_name, method_desc, base_delay in methods:
            print(f"   Спробую: {method_desc}")
            
            for attempt in range(1, 4):
                print(f"      Спроба {attempt}/3...")
                
                try:
                    pyperclip.copy('')
                    time.sleep(0.1)
                    
                    if method_name == "ctrl_a":
                        pyautogui.hotkey('ctrl', 'a')
                    elif method_name == "double_click":
                        pyautogui.doubleClick()
                    elif method_name == "triple_click":
                        pyautogui.click(clicks=3, interval=0.1)
                    elif method_name == "home_shift_end":
                        pyautogui.press('home')
                        time.sleep(0.05)
                        pyautogui.hotkey('shift', 'end')
                    
                    delay = base_delay * attempt
                    time.sleep(delay)
                    
                    pyautogui.hotkey('ctrl', 'c')
                    time.sleep(0.2 * attempt)
                    
                    time.sleep(0.1)
                    copied_text = pyperclip.paste()
                    
                    if copied_text and copied_text.strip():
                        copied_text = copied_text.strip()
                        preview = copied_text[:100] + "..." if len(copied_text) > 100 else copied_text
                        print(f"      ✅ {method_desc} спрацював на спробі {attempt}!")
                        print(f"      📋 Текст: {preview}")
                        
                        try:
                            pyperclip.copy(original_clipboard)
                        except:
                            pass
                            
                        return copied_text
                    else:
                        print(f"      ❌ Буфер порожній, пробую знову...")
                        
                except Exception as e:
                    print(f"      ⚠️ Помилка при спробі {attempt}: {e}")
                    time.sleep(0.2 * attempt)
                    continue
            
            print(f"   ❌ {method_desc} не спрацював після 3 спроб")
        
        print("❌ Жоден метод не спрацював")
        
        try:
            pyperclip.copy(original_clipboard)
        except:
            pass
            
        return None
            
    except Exception as e:
        print(f"❌ Загальна помилка: {e}")
        
        try:
            pyperclip.copy(original_clipboard)
        except:
            pass
            
        return None

def copy_text_from_position(x, y):
    try:
        print(f"📍 Переміщую до ({x}, {y})")
        pyautogui.moveTo(x, y, duration=random.uniform(0.1, 1.0))
        time.sleep(random.uniform(0.1, 1.0))
        
        return select_and_copy_text()
        
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return None

# ========== ФУНКЦИИ ИЗ UIA_METHOD.PY ==========

def test_uia_get_text(x, y):
    """Метод 10: UIA отримання тексту"""
    if not HAS_UIA:
        print("❌ Бібліотека uiautomation не встановлена")
        return None
    
    print("\n🧪 Метод 10: UIA отримання тексту")
    
    try:
        clear_clipboard()
        
        control = auto.ControlFromPoint(x, y)
        
        if not control:
            print("❌ Не вдалося отримати елемент за координатами")
            return None
        
        print(f"   📋 Тип елемента: {control.ControlTypeName}")
        print(f"   🏷️  Назва елемента: '{control.Name}'")
        
        if control.ControlTypeName not in ['EditControl', 'DocumentControl', 'TextControl']:
            print("   🔍 Шукаю текстове поле серед дочірніх елементів...")
            
            text_control = None
            
            try:
                edit_control = control.GetFirstChildControl(ControlType=auto.ControlType