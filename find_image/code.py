import cv2
import numpy as np
import pyautogui
import time
from dataclasses import dataclass
from typing import Tuple, Optional

@dataclass
class SearchSettings:
    """Налаштування пошуку"""
    confidence: float = 0.7          # Чутливість (0.1-0.9)
    grayscale: bool = False          # Ч/Б пошук
    blur: int = 0                    # Розмиття (0-10)
    scales: list = None              # Масштаби [0.8, 0.9, 1.0, 1.1]
    method: int = cv2.TM_CCOEFF_NORMED  # Метод пошуку
    click_offset: Tuple[int, int] = (0, 0)  # Зміщення кліку (x, y)
    click_on: str = "center"         # Де клікати: "center", "top", "bottom", "left", "right"

class ImageSearcher:
    def __init__(self):
        self.settings = SearchSettings()
        
    def find_image(self, template_path: str, custom_settings: Optional[SearchSettings] = None) -> Optional[Tuple[int, int]]:
        """Шукає картинку з гнучкими налаштуваннями"""
        settings = custom_settings or self.settings
        
        # Завантажуємо шаблон
        template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
        if template is None:
            print(f"Не вдалося завантажити: {template_path}")
            return None
        
        # Обробка альфа-каналу
        if template.shape[2] == 4:
            template = cv2.cvtColor(template, cv2.COLOR_BGRA2BGR)
        
        # Робимо скріншот
        screenshot = pyautogui.screenshot()
        screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # Застосовуємо налаштування до шаблона
        template_processed = self._process_image(template, settings)
        screen_processed = self._process_image(screen, settings)
        
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
            
            # Пошук
            result = cv2.matchTemplate(screen_processed, scaled_template, settings.method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val > best_confidence and max_val >= settings.confidence:
                best_confidence = max_val
                h, w = scaled_template.shape[:2]
                
                # Обчислюємо точку кліку згідно налаштувань
                click_point = self._calculate_click_point(max_loc, w, h, settings)
                best_match = click_point
        
        if best_match:
            print(f"✅ Знайдено '{template_path}'")
            print(f"   Впевненість: {best_confidence:.3f}")
            print(f"   Координати: {best_match}")
            return best_match
        else:
            print(f"❌ Не знайдено '{template_path}' (найкраще: {best_confidence:.3f})")
            return None
    
    def _process_image(self, image, settings):
        """Обробка зображення згідно налаштувань"""
        processed = image.copy()
        
        # Конвертація у ч/б
        if settings.grayscale:
            processed = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
        
        # Розмиття
        if settings.blur > 0:
            kernel_size = settings.blur * 2 + 1  # Непарне число
            processed = cv2.GaussianBlur(processed, (kernel_size, kernel_size), 0)
        
        return processed
    
    def _calculate_click_point(self, top_left, width, height, settings):
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
            click_y = y + 5 + offset_y  # Трохи нижче верху
        elif settings.click_on == "bottom":
            click_x = x + width // 2 + offset_x
            click_y = y + height - 5 + offset_y  # Трохи вище низу
        elif settings.click_on == "left":
            click_x = x + 5 + offset_x  # Трохи правіше лівого краю
            click_y = y + height // 2 + offset_y
        elif settings.click_on == "right":
            click_x = x + width - 5 + offset_x  # Трохи лівіше правого краю
            click_y = y + height // 2 + offset_y
        elif settings.click_on == "topleft":
            click_x = x + 5 + offset_x
            click_y = y + 5 + offset_y
        elif settings.click_on == "bottomright":
            click_x = x + width - 5 + offset_x
            click_y = y + height - 5 + offset_y
        else:
            click_x = x + width // 2 + offset_x
            click_y = y + height // 2 + offset_y
        
        return (click_x, click_y)
    
    def click_image(self, template_path: str, max_attempts: int = 3, **kwargs) -> bool:
        """Клікає по знайденій картинці"""
        # Можна передати налаштування як ключові аргументи
        custom_settings = None
        if kwargs:
            custom_settings = SearchSettings(**kwargs)
        
        for attempt in range(max_attempts):
            location = self.find_image(template_path, custom_settings)
            if location:
                pyautogui.moveTo(location[0], location[1], duration=0.3)
                pyautogui.click()
                print(f"🖱️ Клікнуто за координатами: {location}")
                return True
            
            print(f"   Спроба {attempt + 1}/{max_attempts} невдала")
            if attempt < max_attempts - 1:
                time.sleep(1)
        
        return False

# ========== ПРИКЛАДИ ВИКОРИСТАННЯ ==========
def main():
    searcher = ImageSearcher()
    
    # ПРИКЛАД 1: Простий пошук
    print("=== Приклад 1: Простий пошук ===")
    location = searcher.find_image("button.png")
    if location:
        pyautogui.click(location)
    
    # ПРИКЛАД 2: З налаштуваннями
    print("\n=== Приклад 2: З налаштуваннями ===")
    settings = SearchSettings(
        confidence=0.6,      # Нижча чутливість
        grayscale=True,      # Ч/Б пошук
        blur=2,             # Легке розмиття
        scales=[0.9, 1.0, 1.1],  # Три масштаби
        click_on="bottom",   # Клікати внизу картинки
        click_offset=(0, -5) # На 5 пікселів вище
    )
    
    location = searcher.find_image("field.png", settings)
    if location:
        pyautogui.click(location)
    
    # ПРИКЛАД 3: Прямо в методі click_image
    print("\n=== Приклад 3: Одним методом ===")
    searcher.click_image(
        "submit.png",
        confidence=0.5,
        grayscale=False,
        blur=1,
        click_on="center",
        max_attempts=2
    )
    
    # ПРИКЛАД 4: Експерименти з різними методами пошуку
    print("\n=== Приклад 4: Тестування різних методів ===")
    
    methods = [
        ("CCOEFF_NORMED", cv2.TM_CCOEFF_NORMED),
        ("CCORR_NORMED", cv2.TM_CCORR_NORMED),
        ("SQDIFF_NORMED", cv2.TM_SQDIFF_NORMED),
    ]
    
    for method_name, method_code in methods:
        print(f"\nМетод: {method_name}")
        settings = SearchSettings(
            confidence=0.6,
            method=method_code,
            click_on="bottom"
        )
        searcher.find_image("test.png", settings)

if __name__ == "__main__":
    main()