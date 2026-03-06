import random

# Імпортуємо привітання
import greatings
import time
import pyautogui
import keyboard  # Для отслеживания горячих клавиш
import pyperclip

# Спроба імпортувати win32clipboard для роботи з буфером обміну
try:
    import win32clipboard
    HAS_WIN32CLIPBOARD = True
except ImportError:
    HAS_WIN32CLIPBOARD = False
    print("⚠️ Бібліотека win32clipboard не встановлена. Буде використано pyperclip.")

# Імпортуємо наші функції
from image_utils import SearchSettings, find_image, click_at_position
from text_utils import copy_text_from_position, select_and_delete_from_position, paste_text
from random_utils import random_sleep
from error_handler import handle_error
from uia_method import test_uia_get_text
from key_utils import release_all_keys, ensure_focus_and_wait, safe_hotkey, stable_copy_text, wait_for_overlay_disappearance

# Імпортуємо RDP-фікс для буфера обміну
try:
    from rdp_clipboard_fix import copy_text_from_coords_rdp, wait_for_clipboard_change
    HAS_RDP_FIX = True
except ImportError:
    HAS_RDP_FIX = False
    print("⚠️ Файл rdp_clipboard_fix.py не знайдено. Буде використано стандартні методи.")

# Спроба імпортувати альтернативні бібліотеки
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

# Глобальная переменная для контроля выполнения
should_stop = False

def stop_program():
    """Функция для остановки программы по горячей клавише"""
    global should_stop
    should_stop = True
    print("\n🛑 Сигнал остановки получен! Завершаю текущий цикл...")

def find_and_click(image_name, settings):
    """Пошук зображення та клік по ньому. Повертає позицію або False"""
    print(f"\n🔍 Шукаю зображення '{image_name}'...")
    position = find_image(image_name, settings)
    
    if not position:
        print(f"❌ Не вдалося знайти зображення '{image_name}'.")
        return False
    
    print(f"✅ Зображення знайдено за координатами: {position}")
    
    if not click_at_position(position):
        print(f"❌ Не вдалося виконати клік для '{image_name}'.")
        return False

    return position

def clear_clipboard():
    """Очистити буфер обміну (покращена версія для RDP)"""
    try:
        # Спроба 1: Використання win32clipboard для кращої очистки
        if HAS_WIN32CLIPBOARD:
            try:
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.CloseClipboard()
                time.sleep(0.3)  # Затримка для RDP
                return True
            except Exception as e:
                print(f"⚠️ Помилка очищення буфера через win32clipboard: {e}")
                # Продовжуємо з pyperclip
        
        # Спроба 2: Використання pyperclip (резервний варіант)
        pyperclip.copy('')
        time.sleep(0.4)  # Збільшена затримка для RDP
        # Перевірити, що буфер справді очищений
        if pyperclip.paste() == '':
            return True
        else:
            # Спроба ще раз з більшою затримкою
            pyperclip.copy('')
            time.sleep(0.6)  # Ще більша затримка для RDP
            return pyperclip.paste() == ''
    except Exception as e:
        print(f"⚠️ Помилка очищення буфера: {e}")
        return False

def check_clipboard():
    """Перевірити буфер обміну та повернути текст (покращена версія для RDP)"""
    time.sleep(0.3)  # Збільшена затримка для RDP
    
    # Спроба 1: Використання win32clipboard (найкращий варіант для RDP)
    if HAS_WIN32CLIPBOARD:
        try:
            win32clipboard.OpenClipboard()
            
            # Спроба отримати текст у форматі Unicode (CF_UNICODETEXT = 13)
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
            
            # Спроба отримати текст у форматі ANSI (CF_TEXT = 1)
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_TEXT):
                try:
                    text = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
                    if text and text.strip():
                        # Конвертуємо bytes в str якщо потрібно
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
            
            # Спроба отримати текст у форматі OEM (CF_OEMTEXT = 7)
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
    
    # Спроба 2: Використання pyperclip (резервний варіант)
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

def right_click_at_position(x, y):
    """Виконує клік правою кнопкою миші по заданим координатам."""
    print(f"\n🖱️ Клікаю правою кнопкою миші за координатами ({x}, {y})...")
    try:
        pyautogui.click(x=x, y=y, button='right')
        time.sleep(0.5) # Даем время на появление контекстного меню
        print(f"✅ Клік правою кнопкою миші успішно виконано за координатами ({x}, {y}).")
        return True
    except Exception as e:
        print(f"❌ Помилка при кліку правою кнопкою миші за координатами ({x}, {y}): {e}")
        return False

def move_mouse_randomly():
    """Просте водіння мишкою по екрану до 1.5 секунд, повільно і по-людськи"""
    print("🖱️ Рухаю мишкою...")
    
    # Рандомний час руху (0.3 - 1.5 секунди)
    duration = random.uniform(0.3, 1.5)
    start_time = time.time()
    
    # Отримуємо розміри екрану
    screen_width, screen_height = pyautogui.size()
    
    while time.time() - start_time < duration:
        # Випадкові координати на екрані
        x = random.randint(0, screen_width - 1)
        y = random.randint(0, screen_height - 1)
        
        # Повільна швидкість руху (0.5 - 1.2 секунди)
        move_duration = random.uniform(0.5, 1.2)
        
        pyautogui.moveTo(x, y, duration=move_duration)
        
        # Пауза між рухами
        time.sleep(random.uniform(0.1, 0.3))
    
    print("✅ Рух мишкою завершено")


def test_original_with_esc(x, y):
    """Метод 1: Оригінальний метод, який працював (з Esc)"""
    print("\n🧪 Метод 1: Оригінальний метод (з Esc)")
    
    # Оригінальна логіка
    pyautogui.click(button='right')
    time.sleep(0.05)
    pyautogui.press('esc')
    time.sleep(0.05)
    
    # Подвійний клік
    pyautogui.doubleClick()
    time.sleep(0.2)
    
    # Копіювання (збільшена затримка для RDP)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)  # Збільшено з 0.3 до 0.5 для RDP
    
    # Перевірка
    return check_clipboard()

def test_triple_click_only(x, y):
    """Метод 3: Тільки потрійний клік"""
    print("\n🧪 Метод 3: Тільки потрійний клік")
    
    pyautogui.click(clicks=3, interval=0.1)
    time.sleep(0.4)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)  # Збільшено з 0.3 до 0.5 для RDP
    
    return check_clipboard()

def test_ctrl_a_only(x, y):
    """Метод 4: Тільки Ctrl+A"""
    print("\n🧪 Метод 4: Тільки Ctrl+A")
    
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.4)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)  # Збільшено з 0.3 до 0.5 для RDP
    
    return check_clipboard()

def test_sendkeys_ctrl_a(x, y):
    """Метод 8: SendKeys Ctrl+A"""
    if not HAS_WIN32:
        print("❌ Бібліотека win32com не встановлена")
        return None
    
    print("\n🧪 Метод 8: SendKeys Ctrl+A")
    
    pyautogui.click()  # Фокус
    time.sleep(0.3)
    
    # Використання SendKeys
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys("^a")  # Ctrl+A
    time.sleep(0.3)
    shell.SendKeys("^c")  # Ctrl+C
    time.sleep(0.3)
    
    return check_clipboard()

def test_sendkeys_select_all(x, y):
    """Метод 9: SendKeys виділення"""
    if not HAS_WIN32:
        print("❌ Бібліотека win32com не встановлена")
        return None
    
    print("\n🧪 Метод 9: SendKeys виділення")
    
    # Додаткова пауза після очищення буфера
    time.sleep(0.5)
    
    pyautogui.click()  # Фокус
    time.sleep(0.5)  # Збільшена затримка для фокусу
    
    shell = win32com.client.Dispatch("WScript.Shell")
    # Виділення з початку до кінця
    shell.SendKeys("{HOME}")
    time.sleep(0.2)
    shell.SendKeys("+{END}")  # Shift+End
    time.sleep(0.5)
    shell.SendKeys("^c")  # Ctrl+C
    time.sleep(0.5)
    
    return check_clipboard()

def copy_text_from_coords(x, y):
    """Копіювання тексту з позиції. Повертає текст або None"""
    print(f"\n📋 Копіюю текст з позиції ({x}, {y})...")
    
    # ОСНОВНОЙ МЕТОД: стабильное копирование с освобождением клавиш
    print("🔧 Використовую стабильний метод копіювання для RDP...")
    result = stable_copy_text(x, y)
    
    if result:
        print(f"✅ Стабильний метод спрацював!")
        print(f"📄 Зміст тексту: {result[:100]}..." if len(result) > 100 else f"📄 Зміст тексту: {result}")
        return result
    
    # РЕЗЕРВНЫЙ МЕТОД: если стабильный не сработал, пробуем RDP-фикс
    if HAS_RDP_FIX:
        print("🔧 Пробую RDP-оптимізований метод копіювання...")
        result = copy_text_from_coords_rdp(x, y)
        if result:
            print(f"✅ RDP-метод спрацював!")
            print(f"📄 Зміст тексту: {result[:100]}..." if len(result) > 100 else f"📄 Зміст тексту: {result}")
            return result
    
    # ЕЩЕ ОДИН РЕЗЕРВ: оригінальна функція з text_utils.py
    print("🔧 Пробую оригінальну функцію копіювання...")
    result = copy_text_from_position(x, y)
    
    if result:
        print(f"✅ Оригінальна функція спрацювала!")
        print(f"📄 Зміст тексту: {result[:100]}..." if len(result) > 100 else f"📄 Зміст тексту: {result}")
        return result
    
    print("❌ Не вдалося скопіювати текст жодним методом.")
    return None

def main_workflow():
    global should_stop
    
    # Базові налаштування пошуку зображення
    # center, top, bottom, left, right, ...
    base_settings = SearchSettings(
        confidence=0.7,
        grayscale=False,
        blur=0,
        scales=[0.9, 1.0, 1.1],
        click_on="center",
        click_offset=(0, 0),
        max_attempts=3,
        search_timeout=10.0
    )
    
    # КРОК 1: Пошук та клік по зображенню
    base_settings.click_on = "bottom"
    base_settings.click_offset = (0, 3) # на 3px нижче
    position = find_and_click("1.png", base_settings)
    if not position:
        return False
    
    # Перевірка на зупинку
    if should_stop:
        return False
    
    # Рандомна затримка між кроками
    random_sleep(0.3, 1)

    # КРОК 1.1: Клік правою кнопкою миші по позиції
    if not right_click_at_position(position[0], position[1]):
        return False

    random_sleep(0.3, 1)
    
    base_settings.click_on = "bottom"
    base_settings.click_offset = (0, 5)
    position_next = find_and_click("select_all.png", base_settings)
    if not position_next:
        return False

    random_sleep(0.3, 1)

    base_settings.click_on = "bottom"
    base_settings.click_offset = (0, 3) # на 3px нижче
    position_next = find_and_click("1.png", base_settings)
    if not position_next:
        return False

    random_sleep(0.3, 1)
    
    # КРОК 2: Клік правою кнопкою миші по позиції
    if not right_click_at_position(position[0], position[1]):
        return False

    random_sleep(0.3, 1)

    # КРОК 2.1: клік копіювати
    base_settings.click_on = "center"
    base_settings.click_offset = (0, 0)
    position = find_and_click("copy.png", base_settings)
    if not position:
        return False
    
    # Перевірка на зупинку
    if should_stop:
        return False
    
    # Рандомна затримка між кроками
    random_sleep(0.3, 1)
    
    # Перевірка на зупинку
    if should_stop:
        return False
    
    # КРОК 3: Пошук та клік по зображенню хром браузера
    base_settings.click_on = "center"
    base_settings.click_offset = (0, 0)
    
    position = find_and_click("11.png", base_settings)
    if not position:
        return False
    
    # Перевірка на зупинку
    if should_stop:
        return False

    move_mouse_randomly()
    
    print("\n⏳ Затримка 3 секунд щоб відкрився браузер")
    time.sleep(3)
    
    # Перевірка на зупинку після довгої затримки
    if should_stop:
        return False
    
    # КРОК 4: Пошук та клік
    position = find_and_click("9.png", base_settings)
    if not position:
        return False
    
    # Перевірка на зупинку
    if should_stop:
        return False
    
    random_sleep(1, 2)
    
    # Перевірка на зупинку
    if should_stop:
        return False
    
    # КРОК 5: Пошук та клік з іншими налаштуваннями
    base_settings.click_on = "right"
    base_settings.click_offset = (3, 0) # на 3px правіше
    
    position = find_and_click("12.png", base_settings)
    if not position:
        return False
    
    # Перевірка на зупинку
    if should_stop:
        return False
    
    random_sleep(0.3, 1)
    
    # Перевірка на зупинку
    if should_stop:
        return False

    # КРОК 6: Виділяємо та видаляємо текст з текстового поля
    if not right_click_at_position(position[0], position[1]):
        return False
    
    random_sleep(0.3, 1)

    # КРОК 6.1:
    base_settings.click_on = "cener"
    base_settings.click_offset = (0, 0)
    position = find_and_click("select_all_2.png", base_settings)
    if not position:
        return False
    
    random_sleep(0.3, 1)

    # КРОК 7: Пошук та клік
    if not right_click_at_position(position[0], position[1]):
        return False
    
    random_sleep(0.5, 1)

    position = find_and_click("insert.png", base_settings)
    if not position:
        return False

    random_sleep(0.5, 1)
    
    # КРОК 9
    print("\n↵ Натискаю клавішу Enter...")
    pyautogui.press('enter')

    random_sleep(1, 2)

    move_mouse_randomly()

    # КРОК 10
    base_settings.click_on = "center"
    base_settings.click_offset = (0, 0)
    
    position = find_and_click("10.png", base_settings)
    if not position:
        return False
    
    random_sleep(1, 2)

    # КРОК 11
    base_settings.click_on = "bottom"
    base_settings.click_offset = (0, 3)
    position = find_and_click("13.png", base_settings)
    if not position:
        return False
    
    random_sleep(1)

    # КРОК 12: Виділяємо та видаляємо текст з текстового поля
    if not right_click_at_position(position[0], position[1]):
        return False
    
    random_sleep(0.3, 1)

    # КРОК 12.1:
    base_settings.click_on = "center"
    base_settings.click_offset = (0, 0)
    position = find_and_click("select_all_2.png", base_settings)
    if not position:
        return False

    random_sleep(0.3, 1)

    # КРОК 14
    if not right_click_at_position(position[0], position[1]):
        return False
    
    random_sleep(0.5, 1)

    position = find_and_click("insert.png", base_settings)
    if not position:
        return False
    
    random_sleep(0.5, 1)

    # КРОК 15
    print("\n↵ Натискаю клавішу Enter...")
    pyautogui.press('enter')

    move_mouse_randomly()

    # КРОК 16
    base_settings.click_on = "bottom"
    base_settings.click_offset = (0, 10)
    position = find_and_click("20.png", base_settings)
    if not position:
        return False
    
    random_sleep(1)

     # КРОК 17
    base_settings.click_on = "bottom"
    base_settings.click_offset = (0, 10)
    position = find_and_click("20.png", base_settings)
    if not position:
        return False
    
    random_sleep(1)

    # КРОК 18
    base_settings.click_on = "center"
    position = find_and_click("16.png", base_settings)
    # Не зупиняємо виконання, якщо зображення не знайдено
    if not position:
        print("⚠️ Зображення '16.png' не знайдено, продовжую виконання...")
    
    random_sleep(1, 2)

    # КРОК 19
    base_settings.click_on = "center"
    position = find_and_click("17.png", base_settings)
    # Не зупиняємо виконання, якщо зображення не знайдено
    if not position:
        print("⚠️ Зображення '17.png' не знайдено, продовжую виконання...")
    
    random_sleep(0.5, 1)

    move_mouse_randomly()

    # КРОК 20
    position = find_and_click("14.png", base_settings)
    if not position:
        return False
    
    random_sleep(2, 2)

    move_mouse_randomly()

    # КРОК 21
    position = find_and_click("18.png", base_settings)
    if not position:
        return False
    
    random_sleep(2, 3)

    move_mouse_randomly()

    # КРОК 22
    position = find_and_click("19.png", base_settings)
    if not position:
        return False
    
    random_sleep(2, 3)

    # КРОК 20.1
    position = find_and_click("21.png", base_settings)
    if not position:
        return False

    random_sleep(2, 2)

    move_mouse_randomly()

    # КРОК 20.2
    base_settings.click_on = "bottom"
    base_settings.click_offset = (0, 10)
    position = find_and_click("22.png", base_settings)
    if not position:
        return False
    
    random_sleep(0.5, 2)

    # Випадкова кількість символів (1-3)
    num_chars = random.randint(1, 3)
    # Генеруємо випадкові символи (англійські літери або цифри)
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    text = ''.join(random.choice(chars) for _ in range(num_chars))
    print(f"🎲 Вводимо текст: {text} (довжина: {len(text)})")

    # Перевіряємо, чи текст не порожній
    if not text:
        print("⚠️ Текст порожній, пропускаємо введення")
    else:
        # Вводимо кожен символ окремо з випадковою затримкою
        for i, char in enumerate(text):
            print(f"  Вводжу символ {i+1}/{len(text)}: '{char}'")
            pyautogui.press(char)
            time.sleep(random.uniform(0.2, 0.7))
    
    # КРОК 23
    position = find_and_click("15.png", base_settings)
    if not position:
        return False
    
    random_sleep(3, 4)

    # КРОК 24
    position = find_and_click("2.png", base_settings)
    if not position:
        return False
    
    random_sleep(2, 2)
    
    return True

def main():
    """Головна функція"""
    global should_stop
    
    print("\n" + "=" * 60)
    print("🚀 ПРОГРАМА ЗАПУЩЕНА")
    print("📌 Для зупинки натисніть Ctrl+F8")
    print("=" * 60)
    
    # Регистрируем горячую клавишу для остановки (Ctrl+F8 более надежно)
    keyboard.add_hotkey('ctrl+F8', stop_program)
    
    cycle_count = 0
    
    try:
        while not should_stop:
            cycle_count += 1
            print(f"\n🔄 ЦИКЛ #{cycle_count}")
            print("-" * 40)
            
            success = main_workflow()
            
            if not success:
                print("❌ РОБОТУ ЗАВЕРШЕНО З ПОМИЛКАМИ - ПРОГРАМА ЗУПИНЯЄТЬСЯ")
                break
            
            print(f"\n✅ Цикл #{cycle_count} успішно завершено!")
            
            # Небольшая пауза между циклами
            if not should_stop:
                print("⏳ Підготовка до наступного циклу...")
                time.sleep(1)
            
    except Exception as e:
        handle_error(str(e))
        return False
    finally:
        # Убираем обработчик горячей клавиши
        keyboard.unhook_all()
    
    print("\n")
    print("🏁 ПРОГРАМА ЗУПИНЕНА")
    
    return True

if __name__ == "__main__":
    main()