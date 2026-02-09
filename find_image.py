import pyautogui
import cv2
import numpy as np
import time
import os
from pathlib import Path

print("=" * 60)
print("ПОИСК И КЛИК ПО КАРТИНКЕ В RDP")
print("=" * 60)

# 1. Настройки
IMAGE_TO_FIND = "1.png"  # Имя файла с картинкой
CONFIDENCE = 0.7  # Уверенность распознавания (0.0-1.0)
SEARCH_TIMEOUT = 10  # Сколько секунд искать

# 2. Проверяем, есть ли файл с картинкой
image_path = Path(IMAGE_TO_FIND)
if not image_path.exists():
    print(f"ФАЙЛ НЕ НАЙДЕН: {IMAGE_TO_FIND}")
    print("Создай скриншот кнопки в RDP и сохрани как 1.png")
    print("Размести файл в той же папке, где этот скрипт")
    print(f"Текущая папка: {os.getcwd()}")
    exit()

# 3. Загружаем шаблон для поиска
template = cv2.imread(str(image_path))
if template is None:
    print(f"ОШИБКА: Не могу загрузить {IMAGE_TO_FIND}")
    print("Убедись что это PNG или JPG файл")
    exit()

template_height, template_width = template.shape[:2]
print(f"Загружен шаблон: {IMAGE_TO_FIND}")
print(f"Размер шаблона: {template_width}x{template_height}")

# 4. Ждём когда пользователь активирует RDP окно
print("\n" + "=" * 60)
print("ИНСТРУКЦИЯ:")
print(f"1. Открой в RDP окно с нужной кнопкой")
print(f"2. Убедись что кнопка '{IMAGE_TO_FIND.replace('.png', '')}' видна")
print(f"3. Активируй RDP окно (кликни в него)")
print(f"4. У тебя есть {SEARCH_TIMEOUT} секунд")
print("=" * 60)

for i in range(10, 0, -1):
    print(f"Старт через {i}...")
    time.sleep(1)

# 5. Поиск картинки на экране
print(f"\nИщу '{IMAGE_TO_FIND}' на экране...")
found = False
start_time = time.time()

while time.time() - start_time < SEARCH_TIMEOUT and not found:
    try:
        # Делаем скриншот ВСЕГО экрана
        screenshot = pyautogui.screenshot()
        screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # Ищем совпадение
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        print(f"Уверенность распознавания: {max_val:.2f} (нужно {CONFIDENCE})")
        
        if max_val >= CONFIDENCE:
            found = True
            # Вычисляем центр найденной области
            top_left = max_loc
            center_x = top_left[0] + template_width // 2
            center_y = top_left[1] + template_height // 2
            
            print(f"✓ НАЙДЕНО! Координаты: ({center_x}, {center_y})")
            
            # Подсвечиваем найденное место
            pyautogui.moveTo(center_x - 100, center_y, duration=0.3)
            pyautogui.moveTo(center_x, center_y, duration=0.3)
            
            # Кликаем
            print(f"Кликаю в найденную кнопку...")
            pyautogui.click(center_x, center_y)
            
            # Двойной клик для надёжности
            time.sleep(0.2)
            pyautogui.click(center_x, center_y)
            
            print("✓ КЛИК ВЫПОЛНЕН!")
            break
            
        time.sleep(0.5)  # Небольшая пауза между попытками
        
    except Exception as e:
        print(f"Ошибка при поиске: {e}")
        break

if not found:
    print(f"\n✗ Не удалось найти '{IMAGE_TO_FIND}' за {SEARCH_TIMEOUT} секунд")
    print("Возможные причины:")
    print("1. Картинка не видна на экране")
    print("2. CONFIDENCE слишком высокий (попробуй 0.6)")
    print("3. RDP сжатие мешает распознаванию")
    print("4. Неправильный скриншот")

print("\n" + "=" * 60)
print("Тест завершён!")
print("=" * 60)