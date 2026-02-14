# Комплексний тестовий скрипт для перевірки всіх методів копіювання тексту
import time
import pyautogui
import pyperclip
import random
from enum import Enum

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

class TestMethod(Enum):
    """Перелік всіх методів тестування"""
    # Основні методи PyAutoGUI
    ORIGINAL_WITH_ESC = "Оригінальний (з Esc)"
    NEW_WITHOUT_ESC = "Новий (без Esc)"
    DOUBLE_CLICK_ONLY = "Тільки подвійний клік"
    TRIPLE_CLICK_ONLY = "Тільки потрійний клік"
    CTRL_A_ONLY = "Тільки Ctrl+A"
    HOME_SHIFT_END = "Home+Shift+End"
    
    # Альтернативні методи
    SENDKEYS_CTRL_A = "SendKeys Ctrl+A"
    SENDKEYS_SELECT_ALL = "SendKeys виділення"
    UIA_GET_TEXT = "UIA отримання тексту"
    
    # Комбіновані методи
    CLICK_THEN_CTRL_A = "Клік потім Ctrl+A"
    CLICK_THEN_DOUBLE = "Клік потім подвійний"
    RIGHT_CLICK_ESC = "Правий клік + Esc"

def countdown(seconds=10, message="Підготовка до тестування..."):
    """Відлік часу перед тестуванням"""
    print(f"\n{message}")
    for i in range(seconds, 0, -1):
        print(f"   Старт через {i} секунд...")
        time.sleep(1)
    print("✓ ГОТОВО! Починаю тестування...")

def get_current_position():
    """Отримати поточну позицію курсора"""
    x, y = pyautogui.position()
    print(f"📍 Поточна позиція курсора: ({x}, {y})")
    return x, y

def test_original_with_esc(x, y):
    """Оригінальний метод, який працював (з Esc)"""
    print("\n🧪 Тест: Оригінальний метод (з Esc)")
    
    # Переміщення
    pyautogui.moveTo(x, y, duration=0.3)
    time.sleep(0.3)
    
    # Оригінальна логіка
    pyautogui.click(button='right')
    time.sleep(0.05)
    pyautogui.press('esc')
    time.sleep(0.05)
    
    # Подвійний клік
    pyautogui.doubleClick()
    time.sleep(0.2)
    
    # Копіювання
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.3)
    
    # Перевірка
    return check_clipboard()

def test_new_without_esc(x, y):
    """Новий метод (без Esc)"""
    print("\n🧪 Тест: Новий метод (без Esc)")
    
    # Переміщення
    pyautogui.moveTo(x, y, duration=0.3)
    time.sleep(0.3)
    
    # Просто Ctrl+A
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.3)
    
    # Копіювання
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.2)
    
    # Перевірка
    return check_clipboard()

def test_double_click_only(x, y):
    """Тільки подвійний клік"""
    print("\n🧪 Тест: Тільки подвійний клік")
    
    pyautogui.moveTo(x, y, duration=0.3)
    time.sleep(0.3)
    pyautogui.doubleClick()
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.3)
    
    return check_clipboard()

def test_triple_click_only(x, y):
    """Тільки потрійний клік"""
    print("\n🧪 Тест: Тільки потрійний клік")
    
    pyautogui.moveTo(x, y, duration=0.3)
    time.sleep(0.3)
    pyautogui.click(clicks=3, interval=0.1)
    time.sleep(0.4)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.3)
    
    return check_clipboard()

def test_ctrl_a_only(x, y):
    """Тільки Ctrl+A"""
    print("\n🧪 Тест: Тільки Ctrl+A")
    
    pyautogui.moveTo(x, y, duration=0.3)
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.4)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.3)
    
    return check_clipboard()

def test_home_shift_end(x, y):
    """Home+Shift+End"""
    print("\n🧪 Тест: Home+Shift+End")
    
    pyautogui.moveTo(x, y, duration=0.3)
    time.sleep(0.3)
    pyautogui.press('home')
    time.sleep(0.1)
    pyautogui.hotkey('shift', 'end')
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.3)
    
    return check_clipboard()

def test_sendkeys_ctrl_a(x, y):
    """SendKeys Ctrl+A"""
    if not HAS_WIN32:
        print("❌ Бібліотека win32com не встановлена")
        return None
    
    print("\n🧪 Тест: SendKeys Ctrl+A")
    
    pyautogui.moveTo(x, y, duration=0.3)
    time.sleep(0.3)
    pyautogui.click()  # Фокус
    
    # Використання SendKeys
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys("^a")  # Ctrl+A
    time.sleep(0.3)
    shell.SendKeys("^c")  # Ctrl+C
    time.sleep(0.3)
    
    return check_clipboard()

def test_sendkeys_select_all(x, y):
    """SendKeys виділення"""
    if not HAS_WIN32:
        print("❌ Бібліотека win32com не встановлена")
        return None
    
    print("\n🧪 Тест: SendKeys виділення")
    
    pyautogui.moveTo(x, y, duration=0.3)
    time.sleep(0.3)
    pyautogui.click()  # Фокус
    
    shell = win32com.client.Dispatch("WScript.Shell")
    # Виділення з початку до кінця
    shell.SendKeys("{HOME}")
    time.sleep(0.1)
    shell.SendKeys("+{END}")  # Shift+End
    time.sleep(0.3)
    shell.SendKeys("^c")  # Ctrl+C
    time.sleep(0.3)
    
    return check_clipboard()

def test_uia_get_text(x, y):
    """UIA отримання тексту"""
    if not HAS_UIA:
        print("❌ Бібліотека uiautomation не встановлена")
        return None
    
    print("\n🧪 Тест: UIA отримання тексту")
    
    try:
        # Отримання елемента за координатами
        control = auto.ControlFromPoint(x, y)
        
        # Спроба отримати текст різними способами
        text = None
        
        # Спосіб 1: GetValuePattern
        try:
            value_pattern = control.GetValuePattern()
            if value_pattern:
                text = value_pattern.Value
        except:
            pass
        
        # Спосіб 2: LegacyValue
        if not text:
            try:
                text = control.LegacyValue
            except:
                pass
        
        # Спосіб 3: Name property
        if not text:
            try:
                text = control.Name
            except:
                pass
        
        if text and text.strip():
            print(f"✅ UIA отримав текст: '{text[:50]}...'")
            return text.strip()
        else:
            print("❌ UIA не зміг отримати текст")
            return None
            
    except Exception as e:
        print(f"❌ Помилка UIA: {e}")
        return None

def test_click_then_ctrl_a(x, y):
    """Клік потім Ctrl+A"""
    print("\n🧪 Тест: Клік потім Ctrl+A")
    
    pyautogui.moveTo(x, y, duration=0.3)
    time.sleep(0.3)
    pyautogui.click()  # Фокус
    time.sleep(0.5)  # Довша затримка для фокусу
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.4)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.3)
    
    return check_clipboard()

def test_click_then_double(x, y):
    """Клік потім подвійний"""
    print("\n🧪 Тест: Клік потім подвійний")
    
    pyautogui.moveTo(x, y, duration=0.3)
    time.sleep(0.3)
    pyautogui.click()  # Фокус
    time.sleep(0.5)
    pyautogui.doubleClick()
    time.sleep(0.4)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.3)
    
    return check_clipboard()

def test_right_click_esc(x, y):
    """Правий клік + Esc"""
    print("\n🧪 Тест: Правий клік + Esc")
    
    pyautogui.moveTo(x, y, duration=0.3)
    time.sleep(0.3)
    pyautogui.click(button='right')
    time.sleep(0.1)
    pyautogui.press('esc')
    time.sleep(0.1)
    pyautogui.doubleClick()
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.3)
    
    return check_clipboard()

def check_clipboard():
    """Перевірити буфер обміну та повернути текст"""
    time.sleep(0.2)
    try:
        text = pyperclip.paste()
        if text and text.strip():
            text = text.strip()
            preview = text[:50] + "..." if len(text) > 50 else text
            print(f"✅ Текст отримано: '{preview}'")
            return text
        else:
            print("❌ Буфер обміну порожній")
            return None
    except Exception as e:
        print(f"❌ Помилка буфера обміну: {e}")
        return None

def run_single_test(method, x, y):
    """Запустити один тест"""
    print(f"\n{'='*60}")
    print(f"🚀 ТЕСТУВАННЯ МЕТОДУ: {method.value}")
    print(f"{'='*60}")
    
    # Відлік 10 секунд
    countdown(10, f"Підготовка до тесту методу '{method.value}'...")
    
    # Виконання тесту
    result = None
    
    if method == TestMethod.ORIGINAL_WITH_ESC:
        result = test_original_with_esc(x, y)
    elif method == TestMethod.NEW_WITHOUT_ESC:
        result = test_new_without_esc(x, y)
    elif method == TestMethod.DOUBLE_CLICK_ONLY:
        result = test_double_click_only(x, y)
    elif method == TestMethod.TRIPLE_CLICK_ONLY:
        result = test_triple_click_only(x, y)
    elif method == TestMethod.CTRL_A_ONLY:
        result = test_ctrl_a_only(x, y)
    elif method == TestMethod.HOME_SHIFT_END:
        result = test_home_shift_end(x, y)
    elif method == TestMethod.SENDKEYS_CTRL_A:
        result = test_sendkeys_ctrl_a(x, y)
    elif method == TestMethod.SENDKEYS_SELECT_ALL:
        result = test_sendkeys_select_all(x, y)
    elif method == TestMethod.UIA_GET_TEXT:
        result = test_uia_get_text(x, y)
    elif method == TestMethod.CLICK_THEN_CTRL_A:
        result = test_click_then_ctrl_a(x, y)
    elif method == TestMethod.CLICK_THEN_DOUBLE:
        result = test_click_then_double(x, y)
    elif method == TestMethod.RIGHT_CLICK_ESC:
        result = test_right_click_esc(x, y)
    
    # Результат
    print(f"\n{'='*60}")
    if result:
        print(f"✅ МЕТОД '{method.value}' ПРАЦЮЄ!")
        print(f"📋 Текст: '{result[:100]}...'" if len(result) > 100 else f"📋 Текст: '{result}'")
    else:
        print(f"❌ МЕТОД '{method.value}' НЕ ПРАЦЮЄ")
    print(f"{'='*60}")
    
    return result

def main():
    """Головна функція"""
    print("\n" + "="*60)
    print("🧪 КОМПЛЕКСНИЙ ТЕСТ МЕТОДІВ КОПІЮВАННЯ ТЕКСТУ")
    print("="*60)
    
    # Вибір методу
    print("\n📋 Доступні методи тестування:")
    
    methods = list(TestMethod)
    for i, method in enumerate(methods, 1):
        print(f"{i:2}. {method.value}")
    
    print(f"{len(methods)+1:2}. Вихід")
    
    try:
        choice = int(input("\n🎯 Оберіть метод для тестування (1-{}): ".format(len(methods)+1)))
        
        if choice == len(methods) + 1:
            print("👋 Завершення тестування")
            return
        
        if 1 <= choice <= len(methods):
            selected_method = methods[choice - 1]
            
            # Вибір координат
            print("\n📍 Виберіть джерело координат:")
            print("1. Поточна позиція курсора")
            print("2. Ввести координати вручну")
            print("3. Знайти зображення 'test.png'")
            
            coord_choice = input("Ваш вибір (1-3): ").strip()
            
            x, y = 0, 0
            
            if coord_choice == "1":
                x, y = get_current_position()
            elif coord_choice == "2":
                try:
                    x = int(input("X координата: "))
                    y = int(input("Y координата: "))
                    print(f"✅ Використовую координати: ({x}, {y})")
                except ValueError:
                    print("❌ Некоректні координати")
                    return
            elif coord_choice == "3":
                print("🔍 Пошук зображення 'test.png'...")
                # Тут можна додати пошук зображення
                print("⚠️ Функція пошуку зображення поки не реалізована")
                x = int(input("X координата: "))
                y = int(input("Y координата: "))
            else:
                print("❌ Некоректний вибір")
                return
            
            # Запуск тесту
            run_single_test(selected_method, x, y)
            
        else:
            print("❌ Некоректний вибір")
            
    except ValueError:
        print("❌ Будь ласка, введіть число")
    except KeyboardInterrupt:
        print("\n\n🛑 Тестування перервано користувачем")
    except Exception as e:
        print(f"\n❌ Помилка: {e}")

if __name__ == "__main__":
    main()