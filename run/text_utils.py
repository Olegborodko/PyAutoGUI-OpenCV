import pyautogui
import pyperclip
import time
import random

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
                
                time.sleep(0.1)  # Коротка затримка для виділення тексту
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(0.1)  # Коротка затримка для копіювання
                
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
        return False
            
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return False

def copy_text_from_position(x, y):
    try:
        print(f"📍 Переміщую до ({x}, {y})")
        pyautogui.moveTo(x, y, duration=random.uniform(0.1, 1.0))
        random_sleep()
        
        return select_and_copy_text()
        
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return False