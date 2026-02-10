import cv2
import numpy as np
import pyautogui
import time
from dataclasses import dataclass
from typing import Tuple, Optional, List
from pathlib import Path

@dataclass
class SearchSettings:
    """Налаштування пошуку зображення"""
    confidence: float = 0.7          # Чутливість (0.1-0.9)
    grayscale: bool = False          # Ч/Б пошук
    blur: int = 0                    # Розмиття (0-10)
    scales: List[float] = None       # Масштаби [0.8, 0.9, 1.0, 1.1]
    method: int = cv2.TM_CCOEFF_NORMED  # Метод пошуку OpenCV
    click_offset: Tuple[int, int] = (0, 0)  # Зміщення кліку (x, y)
    click_on: str = "center"         # Де клікати: "center", "top", "bottom", "left", "right", "topleft", "topright", "bottomleft", "bottomright"
    max_attempts: int = 3            # Максимальна кількість спроб
    search_timeout: float = 10.0     # Таймаут пошуку в секундах

def find_and_click_image(
    image_name: str, 
    settings: SearchSettings,
    images_folder: str = "images"
) -> bool:
    """
    Шукає зображення та клікає по ньому
    
    Args:
        image_name: Назва файлу зображення (наприклад, "button.png")
        settings: Об'єкт з налаштуваннями пошуку
        images_folder: Папка з зображеннями (відносно поточного файлу)
    
    Returns:
        True якщо зображення знайдено та клік виконано, False в іншому випадку
    """
    # Формуємо повний шлях до зображення
    image_path = Path(__file__).parent / images_folder / image_name
    
    if not image_path.exists():
        print(f"❌ Файл не знайдено: {image_path}")
        return False
    
    # Завантажуємо шаблон
    template = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
    if template is None:
        print(f"❌ Не вдалося завантажити зображення: {image_path}")
        return False
    
    # Обробка альфа-каналу (якщо є)
    if template.shape[2] == 4:
        template = cv2.cvtColor(template, cv2.COLOR_BGRA2BGR)
    
    print(f"🔍 Шукаю '{image_name}' з налаштуваннями:")
    print(f"   Чутливість: {settings.confidence}")
    print(f"   Масштаби: {settings.scales or [1.0]}")
    print(f"   Клік на: {settings.click_on} зі зміщенням {settings.click_offset}")
    
    start_time = time.time()
    attempts = 0
    
    while attempts < settings.max_attempts and (time.time() - start_time) < settings.search_timeout:
        attempts += 1
        print(f"\n   Спроба {attempts}/{settings.max_attempts}")
        
        # Робимо скріншот
        screenshot = pyautogui.screenshot()
        screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # Обробляємо зображення згідно налаштувань
        template_processed = _process_image(template, settings)
        screen_processed = _process_image(screen, settings)
        
        best_match = None
        best_confidence = 0
        
        # Шукаємо у різних масштабах
        scales = settings.scales or [1.0]
        
        for scale in scales:
            if scale != 1.0:
                # Масштабуємо шаблон
                h, w = template_processed.shape[:2]
                new_size = (int(w * scale), int(h * scale))
                scaled_template = cv2.resize(template_processed, new_size)
            else:
                scaled_template = template_processed
            
            # Пошук зображення
            result = cv2.matchTemplate(screen_processed, scaled_template, settings.method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val > best_confidence and max_val >= settings.confidence:
                best_confidence = max_val
                h, w = scaled_template.shape[:2]
                
                # Обчислюємо точку кліку
                click_point = _calculate_click_point(max_loc, w, h, settings)
                best_match = click_point
        
        if best_match:
            print(f"   ✅ Знайдено! Впевненість: {best_confidence:.3f}")
            print(f"   📍 Координати: {best_match}")
            
            # Переміщуємо курсор з анімацією
            pyautogui.moveTo(best_match[0], best_match[1], duration=0.3)
            
            # Клікаємо двічі для надійності
            pyautogui.click()
            time.sleep(0.1)
            pyautogui.click()
            
            print(f"   🖱️ Клік виконано за координатами: {best_match}")
            return True
        else:
            print(f"   ❌ Не знайдено (найкраща впевненість: {best_confidence:.3f})")
            
            # Невелика пауза між спробами
            if attempts < settings.max_attempts:
                time.sleep(0.5)
    
    print(f"\n❌ Не вдалося знайти '{image_name}' після {attempts} спроб")
    return False

def _process_image(image, settings: SearchSettings):
    """Обробка зображення згідно налаштувань"""
    processed = image.copy()
    
    # Конвертація у ч/б
    if settings.grayscale:
        if len(processed.shape) == 3:
            processed = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
    
    # Розмиття
    if settings.blur > 0:
        kernel_size = settings.blur * 2 + 1  # Непарне число
        processed = cv2.GaussianBlur(processed, (kernel_size, kernel_size), 0)
    
    return processed

def _calculate_click_point(top_left: Tuple[int, int], width: int, height: int, settings: SearchSettings) -> Tuple[int, int]:
    """Обчислює куди клікати на знайденій картинці"""
    x, y = top_left
    
    # Зміщення за замовчуванням
    offset_x, offset_y = settings.click_offset
    
    # Вибираємо точку кліку
    if settings.click_on == "center":
        click_x = x + width // 2 + offset_x
        click_y = y + height // 2 + offset_y
    elif settings.click_on == "top":
        click_x = x + width // 2 + offset_x
        click_y = y + offset_y  # Самий верх
    elif settings.click_on == "bottom":
        click_x = x + width // 2 + offset_x
        click_y = y + height + offset_y  # Самий низ
    elif settings.click_on == "left":
        click_x = x + offset_x  # Лівий край
        click_y = y + height // 2 + offset_y
    elif settings.click_on == "right":
        click_x = x + width + offset_x  # Правий край
        click_y = y + height // 2 + offset_y
    elif settings.click_on == "topleft":
        click_x = x + offset_x
        click_y = y + offset_y
    elif settings.click_on == "topright":
        click_x = x + width + offset_x
        click_y = y + offset_y
    elif settings.click_on == "bottomleft":
        click_x = x + offset_x
        click_y = y + height + offset_y
    elif settings.click_on == "bottomright":
        click_x = x + width + offset_x
        click_y = y + height + offset_y
    else:
        # За замовчуванням - центр
        click_x = x + width // 2 + offset_x
        click_y = y + height // 2 + offset_y
    
    return (click_x, click_y)