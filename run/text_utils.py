import pyautogui
import pyperclip
import time
from typing import Union

def select_and_copy_text() -> Union[str, bool]:
    """
    Виділяє текст на місці де зараз курсор та копіює його.
    Перевіряє методи по порядку: подвійний клік, потрійний клік, Ctrl+A.
    
    Returns:
        Скопійований текст або False якщо жоден метод не спрацював
    """
    try:
        print("📋 Починаю виділення та копіювання тексту...")
        
        # Зберігаємо поточну позицію курсора
        current_x, current_y = pyautogui.position()
        print(f"   Поточні координати курсора: ({current_x}, {current_y})")
        
        # Список методів для спроб (у порядку пріоритету)
        methods = [
            ("double_click", "Подвійний клік для виділення слова"),
            ("triple_click", "Потрійний клік для виділення рядка"),
            ("ctrl_a", "Виділити весь текст (Ctrl+A)")
        ]
        
        for method_name, method_desc in methods:
            print(f"\n   Спробую метод: {method_desc}")
            
            try:
                # Скидаємо виділення перед кожною спробою (клік в інше місце)
                pyautogui.click(button='right')  # Правий клік для скидання
                time.sleep(0.1)
                pyautogui.press('esc')  # ESC для скасування контекстного меню
                time.sleep(0.1)
                
                if method_name == "double_click":
                    pyautogui.doubleClick()
                    time.sleep(0.2)
                    
                elif method_name == "triple_click":
                    pyautogui.click(clicks=3)
                    time.sleep(0.2)
                    
                elif method_name == "ctrl_a":
                    pyautogui.hotkey('ctrl', 'a')
                    time.sleep(0.2)
                
                # Копіюємо виділений текст
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(0.3)
                
                # Перевіряємо чи щось скопіювалось
                copied_text = pyperclip.paste()
                
                if copied_text:
                    copied_text = copied_text.strip()
                    if copied_text:
                        # Показуємо перші 100 символів для перевірки
                        preview = copied_text[:100] + "..." if len(copied_text) > 100 else copied_text
                        print(f"   ✅ Метод '{method_name}' спрацював!")
                        print(f"   📋 Текст скопійовано ({len(copied_text)} символів): {preview}")
                        return copied_text
                    else:
                        print(f"   ❌ Метод '{method_name}' не спрацював (текст порожній)")
                else:
                    print(f"   ❌ Метод '{method_name}' не спрацював (буфер порожній)")
                    
            except Exception as e:
                print(f"   ⚠️ Помилка при використанні методу '{method_name}': {e}")
                continue
        
        # Якщо жоден метод не спрацював
        print("\n❌ Жоден метод виділення тексту не спрацював")
        return False
            
    except Exception as e:
        print(f"❌ Критична помилка при виділенні/копіюванні тексту: {e}")
        return False

def copy_text_from_position(x: int, y: int) -> Union[str, bool]:
    """
    Переміщує курсор до вказаної позиції, виділяє текст та копіює його
    
    Args:
        x: X координата
        y: Y координата
    
    Returns:
        Скопійований текст або False якщо не вдалося
    """
    try:
        print(f"📍 Переміщую курсор до позиції: ({x}, {y})")
        pyautogui.moveTo(x, y, duration=0.3)
        time.sleep(0.2)
        
        return select_and_copy_text()
        
    except Exception as e:
        print(f"❌ Помилка при переміщенні курсора: {e}")
        return False