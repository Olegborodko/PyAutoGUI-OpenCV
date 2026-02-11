import cv2
import numpy as np
import pyautogui
import time
import random
from dataclasses import dataclass
from typing import Tuple, List, Union

@dataclass
class SearchSettings:
    confidence: float = 0.7
    grayscale: bool = False
    blur: int = 0
    scales: List[float] = None
    method: int = cv2.TM_CCOEFF_NORMED
    click_offset: Tuple[int, int] = (0, 0)
    click_on: str = "center"
    max_attempts: int = 3
    search_timeout: float = 10.0

def random_sleep():
    time.sleep(random.uniform(0.1, 1.0))

def random_duration():
    return random.uniform(0.1, 1.0)

def find_image(image_name, settings, images_folder="images"):
    try:
        import os
        from pathlib import Path
        
        image_path = Path(__file__).parent / images_folder / image_name
        
        if not image_path.exists():
            print(f"❌ Файл не знайдено: {image_path}")
            return False
        
        template = cv2.imread(str(image_path))
        if template is None:
            print(f"❌ Не вдалося завантажити: {image_path}")
            return False
        
        if template.shape[2] == 4:
            template = cv2.cvtColor(template, cv2.COLOR_BGRA2BGR)
        
        print(f"🔍 Шукаю '{image_name}'...")
        
        start_time = time.time()
        attempts = 0
        
        while attempts < settings.max_attempts and (time.time() - start_time) < settings.search_timeout:
            attempts += 1
            print(f"   Спроба {attempts}/{settings.max_attempts}")
            
            screenshot = pyautogui.screenshot()
            screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            template_processed = _process_image(template, settings)
            screen_processed = _process_image(screen, settings)
            
            best_match = None
            best_confidence = 0
            
            scales = settings.scales or [1.0]
            
            for scale in scales:
                if scale != 1.0:
                    h, w = template_processed.shape[:2]
                    new_size = (int(w * scale), int(h * scale))
                    scaled_template = cv2.resize(template_processed, new_size)
                else:
                    scaled_template = template_processed
                
                result = cv2.matchTemplate(screen_processed, scaled_template, settings.method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                if max_val > best_confidence and max_val >= settings.confidence:
                    best_confidence = max_val
                    h, w = scaled_template.shape[:2]
                    click_point = _calculate_click_point(max_loc, w, h, settings)
                    best_match = click_point
            
            if best_match:
                print(f"   ✅ Знайдено! Впевненість: {best_confidence:.3f}")
                print(f"   📍 Координати: {best_match}")
                return best_match
            else:
                print(f"   ❌ Не знайдено (найкраща впевненість: {best_confidence:.3f})")
                if attempts < settings.max_attempts:
                    random_sleep()
        
        print(f"❌ Не вдалося знайти '{image_name}'")
        return False
        
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return False

def click_at_position(position, double_click=True):
    try:
        x, y = position
        print(f"🖱️ Переміщую до ({x}, {y})")
        pyautogui.moveTo(x, y, duration=random_duration())
        
        if double_click:
            print("   Подвійний клік...")
            pyautogui.doubleClick()
        else:
            print("   Одинарний клік...")
            pyautogui.click()
        
        print(f"   ✅ Клік виконано")
        return True
        
    except Exception as e:
        print(f"❌ Помилка при кліку: {e}")
        return False

def find_and_click_image(image_name, settings, images_folder="images"):
    position = find_image(image_name, settings, images_folder)
    if position:
        return click_at_position(position)
    return False

def _process_image(image, settings):
    processed = image.copy()
    
    if settings.grayscale:
        if len(processed.shape) == 3:
            processed = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
    
    if settings.blur > 0:
        kernel_size = settings.blur * 2 + 1
        processed = cv2.GaussianBlur(processed, (kernel_size, kernel_size), 0)
    
    return processed

def _calculate_click_point(top_left, width, height, settings):
    x, y = top_left
    offset_x, offset_y = settings.click_offset
    
    if settings.click_on == "center":
        click_x = x + width // 2 + offset_x
        click_y = y + height // 2 + offset_y
    elif settings.click_on == "top":
        click_x = x + width // 2 + offset_x
        click_y = y + offset_y
    elif settings.click_on == "bottom":
        click_x = x + width // 2 + offset_x
        click_y = y + height + offset_y
    elif settings.click_on == "left":
        click_x = x + offset_x
        click_y = y + height // 2 + offset_y
    elif settings.click_on == "right":
        click_x = x + width + offset_x
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
        click_x = x + width // 2 + offset_x
        click_y = y + height // 2 + offset_y
    
    return (click_x, click_y)