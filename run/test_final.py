# Фінальний тестовий скрипт - знаходить поле по зображенню та тестує методи
import time
import pyautogui
import pyperclip
from enum import Enum

# Імпортуємо функції пошуку зображень
from image_utils import SearchSettings, find_image, click_at_position

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
    """Перелік методів тестування"""
    ORIGINAL_WITH_ESC = "Оригінальний (з Esc)"
    DOUBLE_CLICK_ONLY = "Тільки подвійний клік"
    TRIPLE_CLICK_ONLY = "Тільки потрійний клік"
    CTRL_A_ONLY = "Тільки Ctrl+A"
    CLICK_THEN_CTRL_A = "Клік потім Ctrl+A"
    CLICK_THEN_DOUBLE = "Клік потім подвійний"
    RIGHT_CLICK_ESC = "Правий клік + Esc"
    SENDKEYS_CTRL_A = "SendKeys Ctrl+A"
    SENDKEYS_SELECT_ALL = "SendKeys виділення"
    UIA_GET_TEXT = "UIA отримання тексту"

def countdown(seconds=10, message="Підготовка до тестування..."):
    """Відлік часу перед тестуванням"""
    print(f"\n{message}")
    for i in range(seconds, 0, -1):
        print(f"   Старт через {i} секунд...")
        time.sleep(1)
    print("✓ ГОТОВО! Починаю тестування...")

def find_and_click_test_image():
    """Знайти зображення test.png та клікнути по ньому"""
    print("\n🔍 Шукаю зображення 'test.png'...")
    
    settings = SearchSettings(
        confidence=0.7,
        grayscale=False,
        blur=0,
        scales=[0.9, 1.0, 1.1],
        click_on="right",
        click_offset=(10, 0),
        max_attempts=3,
        search_timeout=10.0
    )
    
    settings.click_on = "bottom"
    settings.click_offset = (0, 3)
    position = find_image("test.png", settings)
    
    if not position:
        print("❌ Не вдалося знайти зображення 'test.png'.")
        return None
    
    print(f"✅ Зображення знайдено за координатами: {position}")
    
    if not click_at_position(position):
        print(f"❌ Не вдалося виконати клік.")
        return None
    
    print(f"✅ Клік виконано за координатами: {position}")
    return position

def test_original_with_esc(x, y):
    """Оригінальний метод, який працював (з Esc)"""
    print("\n🧪 Тест: Оригінальний метод (з Esc)")
    
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

def test_double_click_only(x, y):
    """Тільки подвійний клік"""
    print("\n🧪 Тест: Тільки подвійний клік")
    
    pyautogui.doubleClick()
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.3)
    
    return check_clipboard()

def test_triple_click_only(x, y):
    """Тільки потрійний клік"""
    print("\n🧪 Тест: Тільки потрійний клік")
    
    pyautogui.click(clicks=3, interval=0.1)
    time.sleep(0.4)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.3)
    
    return check_clipboard()

def test_ctrl_a_only(x, y):
    """Тільки Ctrl+A"""
    print("\n🧪 Тест: Тільки Ctrl+A")
    
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.4)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.3)
    
    return check_clipboard()

def test_click_then_ctrl_a(x, y):
    """Клік потім Ctrl+A"""
    print("\n🧪 Тест: Клік потім Ctrl+A")
    
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
    
    pyautogui.click(button='right')
    time.sleep(0.1)
    pyautogui.press('esc')
    time.sleep(0.1)
    pyautogui.doubleClick()
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
    """SendKeys виділення"""
    if not HAS_WIN32:
        print("❌ Бібліотека win32com не встановлена")
        return None
    
    print("\n🧪 Тест: SendKeys виділення")
    
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

def test_uia_get_text(x, y):
    """UIA отримання тексту"""
    if not HAS_UIA:
        print("❌ Бібліотека uiautomation не встановлена")
        return None
    
    print("\n🧪 Тест: UIA отримання тексту")
    
    try:
        # Очищаємо буфер обміну перед тестом UIA
        print("🧹 Очищаю буфер обміну перед тестом UIA...")
        clear_clipboard()
        
        # Отримання елемента за координатами
        print(f"🔍 Отримую елемент за координатами ({x}, {y})...")
        control = auto.ControlFromPoint(x, y)
        
        if not control:
            print("❌ Не вдалося отримати елемент за координатами")
            return None
        
        # Спроба отримати текст різними способами
        text = None
        
        # Спосіб 1: GetValuePattern (для текстових полів)
        try:
            print("   Спробую GetValuePattern...")
            value_pattern = control.GetValuePattern()
            if value_pattern:
                text = value_pattern.Value
                if text and text.strip():
                    print(f"   ✅ GetValuePattern: '{text[:50]}...'")
                else:
                    print("   ❌ GetValuePattern повернув порожній текст")
        except Exception as e:
            print(f"   ⚠️ GetValuePattern помилка: {e}")
        
        # Спосіб 2: LegacyValue
        if not text or not text.strip():
            try:
                print("   Спробую LegacyValue...")
                text = control.LegacyValue
                if text and text.strip():
                    print(f"   ✅ LegacyValue: '{text[:50]}...'")
                else:
                    print("   ❌ LegacyValue повернув порожній текст")
            except Exception as e:
                print(f"   ⚠️ LegacyValue помилка: {e}")
        
        # Спосіб 3: Name property
        if not text or not text.strip():
            try:
                print("   Спробую Name property...")
                text = control.Name
                if text and text.strip():
                    print(f"   ✅ Name: '{text[:50]}...'")
                else:
                    print("   ❌ Name повернув порожній текст")
            except Exception as e:
                print(f"   ⚠️ Name помилка: {e}")
        
        # Спосіб 4: Додаткові методи для текстових елементів
        if not text or not text.strip():
            try:
                print("   Спробую додаткові методи...")
                # Спроба отримати текст через DocumentPattern
                if hasattr(control, 'GetTextPattern'):
                    text_pattern = control.GetTextPattern()
                    if text_pattern:
                        text_range = text_pattern.DocumentRange
                        if text_range:
                            text = text_range.GetText(-1)
                            if text and text.strip():
                                print(f"   ✅ TextPattern: '{text[:50]}...'")
            except Exception as e:
                print(f"   ⚠️ Додаткові методи помилка: {e}")
        
        # Спосіб 5: Пошук дочірніх елементів з текстом
        if not text or not text.strip():
            try:
                print("   Спробую пошук дочірніх елементів...")
                # Шукаємо перший дочірній елемент з текстом
                for child in control.GetChildren():
                    try:
                        child_text = child.Name
                        if child_text and child_text.strip():
                            text = child_text
                            print(f"   ✅ Знайдено текст у дочірньому елементі: '{text[:50]}...'")
                            break
                    except:
                        continue
            except Exception as e:
                print(f"   ⚠️ Пошук дочірніх елементів помилка: {e}")
        
        if text and text.strip():
            text = text.strip()
            print(f"✅ UIA отримав текст: '{text[:50]}...'")
            return text
        else:
            print("❌ UIA не зміг отримати текст")
            return None
            
    except Exception as e:
        print(f"❌ Помилка UIA: {e}")
        return None

def clear_clipboard():
    """Очистити буфер обміну"""
    try:
        pyperclip.copy('')
        time.sleep(0.3)  # Збільшена затримка
        # Перевірити, що буфер справді очищений
        if pyperclip.paste() == '':
            return True
        else:
            # Спроба ще раз з більшою затримкою
            pyperclip.copy('')
            time.sleep(0.5)
            return pyperclip.paste() == ''
    except Exception as e:
        print(f"⚠️ Помилка очищення буфера: {e}")
        return False

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

def run_test(method_choice, position):
    """Запустити тест обраного методу"""
    x, y = position
    
    print(f"\n{'='*60}")
    print(f"🚀 ТЕСТУВАННЯ: {method_choice.value}")
    print(f"📍 Координати: ({x}, {y})")
    print(f"{'='*60}")
    
    # Очищаємо буфер обміну перед тестом
    print("🧹 Очищаю буфер обміну перед тестом...")
    if clear_clipboard():
        print("✅ Буфер обміну очищено")
    else:
        print("⚠️ Не вдалося повністю очистити буфер обміну")
    
    result = None
    
    if method_choice == TestMethod.ORIGINAL_WITH_ESC:
        result = test_original_with_esc(x, y)
    elif method_choice == TestMethod.DOUBLE_CLICK_ONLY:
        result = test_double_click_only(x, y)
    elif method_choice == TestMethod.TRIPLE_CLICK_ONLY:
        result = test_triple_click_only(x, y)
    elif method_choice == TestMethod.CTRL_A_ONLY:
        result = test_ctrl_a_only(x, y)
    elif method_choice == TestMethod.CLICK_THEN_CTRL_A:
        result = test_click_then_ctrl_a(x, y)
    elif method_choice == TestMethod.CLICK_THEN_DOUBLE:
        result = test_click_then_double(x, y)
    elif method_choice == TestMethod.RIGHT_CLICK_ESC:
        result = test_right_click_esc(x, y)
    elif method_choice == TestMethod.SENDKEYS_CTRL_A:
        result = test_sendkeys_ctrl_a(x, y)
    elif method_choice == TestMethod.SENDKEYS_SELECT_ALL:
        result = test_sendkeys_select_all(x, y)
    elif method_choice == TestMethod.UIA_GET_TEXT:
        result = test_uia_get_text(x, y)
    
    # Результат
    print(f"\n{'='*60}")
    if result:
        print(f"✅ МЕТОД '{method_choice.value}' ПРАЦЮЄ!")
        print(f"📋 Текст: '{result[:100]}...'" if len(result) > 100 else f"📋 Текст: '{result}'")
    else:
        print(f"❌ МЕТОД '{method_choice.value}' НЕ ПРАЦЮЄ")
    print(f"{'='*60}")
    
    return result

def main():
    """Головна функція тестування"""
    print("\n" + "="*60)
    print("🧪 ТЕСТУВАННЯ МЕТОДІВ КОПІЮВАННЯ ТЕКСТУ")
    print("="*60)
    
    # Вибір методу
    print("\n📋 Оберіть метод для тестування:")
    
    methods = list(TestMethod)
    for i, method in enumerate(methods, 1):
        print(f"{i:2}. {method.value}")
    
    print(f"{len(methods)+1:2}. Вихід")
    
    try:
        choice = int(input("\n🎯 Ваш вибір (1-{}): ".format(len(methods)+1)))
        
        if choice == len(methods) + 1:
            print("👋 Завершення тестування")
            return
        
        if 1 <= choice <= len(methods):
            selected_method = methods[choice - 1]
            
            print(f"\n✅ Обрано: {selected_method.value}")
            print("⏳ Натисніть Enter для початку тестування...")
            input()  # Чекаємо натискання Enter
            
            # 10-секундний відлік
            countdown(10, "Підготовка до пошуку зображення...")
            
            # Пошук зображення та отримання координат
            position = find_and_click_test_image()
            
            if not position:
                print("❌ Не вдалося знайти поле для тестування")
                return
            
            # Запуск тесту
            run_test(selected_method, position)
            
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