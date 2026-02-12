import pyautogui
import pyperclip
import time
import random
import pytesseract
from PIL import ImageGrab
import os

# Налаштування шляху до Tesseract OCR (якщо потрібно)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def random_sleep():
    time.sleep(random.uniform(0.1, 1.0))

def select_and_copy_text():
    try:
        print("📋 Виділяю та копіюю текст...")
        
        x, y = pyautogui.position()
        print(f"   Курсор: ({x}, {y})")
        
        methods = [
            ("double_click", "Подвійний клік"),
            ("triple_click", "Потрійний клік"),
            ("ctrl_a", "Ctrl+A")
        ]
        
        for method_name, method_desc in methods:
            print(f"   Спробую: {method_desc}")
            
            try:
                # Спершу очистимо буфер обміну
                pyperclip.copy('')
                
                # Скинемо можливе контекстне меню
                pyautogui.click(button='right')
                time.sleep(0.05)  # Дуже коротка затримка для стабільності
                pyautogui.press('esc')
                time.sleep(0.05)  # Дуже коротка затримка для стабільності
                
                if method_name == "double_click":
                    pyautogui.doubleClick()
                elif method_name == "triple_click":
                    pyautogui.click(clicks=3)
                elif method_name == "ctrl_a":
                    pyautogui.hotkey('ctrl', 'a')
                
                time.sleep(0.2)  # Збільшена затримка для виділення тексту
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(0.3)  # Збільшена затримка для копіювання
                
                # Додаткова перевірка буферу обміну
                time.sleep(0.1)
                copied_text = pyperclip.paste()
                
                if copied_text:
                    copied_text = copied_text.strip()
                    if copied_text:
                        preview = copied_text[:100] + "..." if len(copied_text) > 100 else copied_text
                        print(f"   ✅ {method_desc} спрацював!")
                        print(f"   📋 Текст: {preview}")
                        return copied_text
                    else:
                        print(f"   ❌ {method_desc} не спрацював (текст порожній)")
                else:
                    print(f"   ❌ {method_desc} не спрацював (буфер порожній)")
                    
            except Exception as e:
                print(f"   ⚠️ Помилка: {e}")
                continue
        
        print("❌ Жоден метод не спрацював")
        return None
            
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return None

def copy_text_from_position(x, y):
    try:
        print(f"📍 Переміщую до ({x}, {y})")
        pyautogui.moveTo(x, y, duration=random.uniform(0.1, 1.0))
        random_sleep()
        
        return select_and_copy_text()
        
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return None

def select_and_delete_text():
    """Виділяє та видаляє текст (вирізає). Повертає True у разі успіху"""
    try:
        print("✂️ Виділяю та видаляю текст...")
        
        x, y = pyautogui.position()
        print(f"   Курсор: ({x}, {y})")
        
        methods = [
            ("double_click", "Подвійний клік"),
            ("triple_click", "Потрійний клік"),
            ("ctrl_a", "Ctrl+A")
        ]
        
        for method_name, method_desc in methods:
            print(f"   Спробую: {method_desc}")
            
            try:
                # Скинемо можливе контекстне меню
                pyautogui.click(button='right')
                time.sleep(0.05)
                pyautogui.press('esc')
                time.sleep(0.05)
                
                if method_name == "double_click":
                    pyautogui.doubleClick()
                elif method_name == "triple_click":
                    pyautogui.click(clicks=3)
                elif method_name == "ctrl_a":
                    pyautogui.hotkey('ctrl', 'a')
                
                time.sleep(0.1)  # Коротка затримка для виділення тексту
                
                # Видаляємо виділений текст (Delete)
                pyautogui.press('delete')
                time.sleep(0.1)
                
                print(f"   ✅ {method_desc} спрацював! Текст видалено.")
                return True
                    
            except Exception as e:
                print(f"   ⚠️ Помилка: {e}")
                continue
        
        print("❌ Жоден метод не спрацював")
        return False
            
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return False

def paste_text(text_to_paste):
    """Вставляє переданий текст різними способами (fallback-механізм). Повертає True у разі успіху"""
    try:
        print("📋 Вставляю текст...")
        
        if not text_to_paste:
            print("❌ Текст для вставки порожній")
            return False
        
        # МЕТОД 1: Спробувати ввести текст через write (без буфера обміну)
        print("   Спробую ввести текст через write...")
        try:
            pyautogui.write(text_to_paste, interval=0.01)
            time.sleep(0.1)
            print("✅ Текст успішно введено через write!")
            return True
        except Exception as e:
            print(f"   ❌ Помилка при введенні через write: {e}")
        
        # МЕТОД 2: Спробувати через typewrite
        print("   Спробую через typewrite...")
        try:
            pyautogui.typewrite(text_to_paste, interval=0.05)
            time.sleep(0.1)
            print("✅ Текст успішно введено через typewrite!")
            return True
        except Exception as e:
            print(f"   ❌ Помилка при введенні через typewrite: {e}")
        
        # МЕТОД 3: Спробувати вставити текст через Ctrl+V (з буфером обміну)
        print("   Спробую Ctrl+V з буфером обміну...")
        try:
            # Копіюємо текст в буфер обміну
            pyperclip.copy(text_to_paste)
            time.sleep(0.05)
            
            # Вставляємо через Ctrl+V
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.1)
            print("✅ Текст успішно вставлено через Ctrl+V!")
            return True
        except Exception as e:
            print(f"   ❌ Ctrl+V не спрацював: {e}")
        
        # МЕТОД 4: Остання спроба - посимвольний ввід
        print("   Спробую останній метод (посимвольний ввід)...")
        try:
            for char in text_to_paste:
                pyautogui.press(char)
                time.sleep(0.01)
            time.sleep(0.1)
            print("✅ Текст успішно введено посимвольно!")
            return True
        except Exception as e:
            print(f"   ❌ Останній метод не спрацював: {e}")
        
        print("❌ Жоден метод вставки тексту не спрацював")
        return False
        
    except Exception as e:
        print(f"❌ Загальна помилка при вставці тексту: {e}")
        return False

def copy_text_without_clipboard(x, y, width=200, height=50):
    """Копіює текст з екрану через OCR без використання буферу обміну"""
    try:
        print(f"🔍 Копіюю текст через OCR з позиції ({x}, {y})...")
        
        # Захоплюємо область екрану
        left = x - width // 2
        top = y - height // 2
        right = x + width // 2
        bottom = y + height // 2
        
        # Переконуємося, що координати в межах екрану
        screen_width, screen_height = pyautogui.size()
        left = max(0, left)
        top = max(0, top)
        right = min(screen_width, right)
        bottom = min(screen_height, bottom)
        
        # Захоплюємо зображення
        screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
        
        # Використовуємо OCR для розпізнавання тексту
        text = pytesseract.image_to_string(screenshot, lang='eng+ukr+rus')
        
        if text:
            text = text.strip()
            if text:
                preview = text[:100] + "..." if len(text) > 100 else text
                print(f"✅ Текст успішно розпізнано через OCR!")
                print(f"📋 Текст: {preview}")
                return text
            else:
                print("❌ OCR розпізнав порожній текст")
        else:
            print("❌ OCR не зміг розпізнати текст")
        
        return None
        
    except Exception as e:
        print(f"❌ Помилка при OCR: {e}")
        return None

def select_and_delete_from_position(x, y):
    """Переміщується до позиції та видаляє текст. Повертає True у разі успіху"""
    try:
        print(f"📍 Переміщую до ({x}, {y}) для видалення тексту")
        pyautogui.moveTo(x, y, duration=random.uniform(0.1, 1.0))
        random_sleep()
        
        return select_and_delete_text()
        
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return False
