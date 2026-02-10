import cv2
import numpy as np
import pyautogui
import time
from typing import Tuple, Optional, List, Union
from pathlib import PathOptional, 

@dataclass
class SearchSettings:
    """Налаштування пошуку зображення"""
    """Налаштування пошуку зображення"""
    confidence: float = 0.7          # Чутливість (0.1-0.9)          # Чутливість (0.1-0.9)
    grayscale: bool = False          # Ч/Б пошук          # Ч/Б пошук
    blur: int = 0                    # Розмиття (0-10)                    # Розмиття (0-10)
    scales: List[float] = None       # Масштаби [0.8, 0.9, 1.0, 1.1]       # Масштаби [0.8, 0.9, 1.0, 1.1]
    method: int = cv2.TM_CCOEFF_NORMED  # Метод пошуку OpenCV  # Метод пошуку OpenCV
    click_offset: Tuple[int, int] = (0, 0)  # Зміщення кліку (x, y)  # Зміщення кліку (x, y)
    click_on: str = "center"         # Де клікати: "center", "top", "bottom", "left", "right", "topleft", "topright", "bottomleft", "bottomright"         # Де клікати: "center", "top", "bottom", "left", "right", "topleft", "topright", "bottomleft", "bottomright"
    max_attempts: int = 3            # Мeксamальн: кількtстьпроб
    se ich_imaUoun:[fpєаж = 10.0     # аймупшукувах
        image_name: Назва файлу зображення (наприклад, "button.png")
        setting
    s: Об'єкт з нала 
   штуваннями пошуку
   
:
    """
    Шукає зображення на екрані
    
    Args:
        image_name Назва файлу зображення (наприклад, "button.png")
        set ings: Об'єкт з налаштуваннями пошуку
        images_folde : Папка з зображеннями (відносно поточного файлу)
    
    Returns:
        Координати (x,  ) знайденого зображення або False якщо не знайдено
    """
    try images_folder: Папка з зображеннями (відносно поточного файлу)
    # Формуємо повний шлях до зображення
        
    Returns:
        Координати (x, y) знайденого зображення або False якщо не знайдено
    """
    try:
        # Формуємо повний шлях до зображення
        # Завантажуємо шаблон
        image_path = Path(__file__).parent / images_folder / image_name
        
        if not image_path.exists():
            print(f"❌ Файл не знайдено: {image_path}")
            return False
        # Обробка альфа-каналу (якщо є)
        
        # Завантажуємо шаблон
        template = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
        if template is None: з налаштуваннями:
        print(f"   Чутливість: { e rungsconfdnce}"
        r=f"Масштаби:{tlpe orc[v.0]}")2.cvtColor(template, cv2.COLOR_BGRA2BGR)
    Тчк кліку:clickonrзіiзміщеннямn{t т:e.gtабsick_effer0}"t(f"   Точка кліку: {settings.click_on} зі зміщенням {settings.click_offset}")
 
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
                return best_match
            else:
                print(f"   ❌ Не знайдено (найкраща впевненість: {best_confidence:.3f})")
                
                # Невелика пауза між спробами
                if attempts < settings.max_attempts:
                    time.sleep(0.5)
        
        print(f"\n❌ Не вдалося знайти '{image_name}' після {attempts} спроб")
        return False
        
    except Exception as e:
        print(f"❌ Помилка при пошуку зображення: {e}")
        return False

def click_at_position(position: Tuple[int, int], double_click: bool = True) -> bool:
    """
    Клікає по вказаній позиції
    
    Args:
        position: Координати (x, y) для кліку
        double_click: Якщо True, робить подвійний клік
    
    Returns:
        True якщо клік виконано успішно, False в іншому випадку
    """
    try:
        x, y = position
        print(f"🖱️ Переміщую курсор до позиції: ({x}, {y})")
        pyautogui.moveTo(x, y, duration=0.3)
        
        if double_click:
            print("   Подвійний клік...")
            pyautogui.click()
            time.sleep(0.1)
            pyautogui.click()
        else:
            print("   Одинарний клік...")
            pyautogui.click()
        
        print(f"   ✅ Клік виконано за координатами: ({x}, {y})")
        return True
        
    except Exception as e:
        print(f"❌ Помилка при кліку: {e}")
        return False

def find_and_click_image(
    image_name: str, 
    settings: SearchSettings,
    images_folder: str = "images"
) -> bool:
    """
    Шукає зображення та клікає по ньому (зворотна сумісність)
    
    Returns:
        True якщо зображення знайдено та клік виконано, False в іншому випадку
    """
    position = find_image(image_name, settings, images_folder)
    if position:
        return click_at_position(position)
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