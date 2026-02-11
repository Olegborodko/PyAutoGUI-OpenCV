# Імпортуємо привітання
import greatings

# Імпортуємо наші функції
from image_utils import SearchSettings, find_image, click_at_position
from text_utils import copy_text_from_position
from random_utils import random_sleep

def find_and_click(image_name, settings):
    """Пошук зображення та клік по ньому. Повертає позицію або False"""
    print(f"\n🔍 Шукаю зображення '{image_name}'...")
    position = find_image(image_name, settings)
    
    if not position:
        print(f"❌ Не вдалося знайти зображення '{image_name}'.")
        return False
    
    print(f"✅ Зображення знайдено за координатами: {position}")
    
    random_sleep()
    
    print(f"🖱️ Клікаю по знайденій позиції...")
    if not click_at_position(position):
        print(f"❌ Не вдалося виконати клік для '{image_name}'.")
        return False
    
    print("✅ Клік виконано успішно!")
    return position

def copy_text_from_coords(x, y):
    """Копіювання тексту з позиції. Повертає текст або None"""
    print(f"\n📋 Копіюю текст з позиції ({x}, {y})...")
    copied_text = copy_text_from_position(x, y)
    
    if not copied_text:
        print("❌ Не вдалося скопіювати текст.")
        return None
    
    print(f"✅ Текст успішно скопійовано!")
    print(f"📄 Зміст тексту: {copied_text[:100]}..." if len(copied_text) > 100 else f"📄 Зміст тексту: {copied_text}")
    return copied_text

def main_workflow():
    # Базові налаштування пошуку зображення
    base_settings = SearchSettings(
        confidence=0.7,
        grayscale=False,
        blur=0,
        scales=[0.9, 1.0, 1.1],
        click_on="bottom",
        click_offset=(0, 0),
        max_attempts=3,
        search_timeout=10.0
    )
    
    # КРОК 1: Пошук та клік по зображенню
    position = find_and_click("1.png", base_settings)
    if not position:
        return False
    
    # Рандомна затримка між кроками
    random_sleep()
    
    # КРОК 2: Копіювання тексту з позиції
    copied_text = copy_text_from_coords(position[0], position[1])
    if not copied_text:
        return False
    
    # Рандомна затримка між кроками
    random_sleep()
    
    # КРОК 3: Пошук та клік по зображенню хром браузера
    base_settings.click_on = "center"
    base_settings.click_offset = (0, -3)
    
    position = find_and_click("11.png", base_settings)
    if not position:
        return False
    
    # Фіксована затримка 5 секунд після кроку 5
    print("\n⏳ Затримка 5 секунд...")
    time.sleep(5)
    
    # КРОК 4: Пошук та клік
    position = find_and_click("9.png", base_settings)
    if not position:
        return False
    
    time.sleep(1)
    
    # КРОК 5: Пошук та клік з іншими налаштуваннями
    # Змінюємо тільки click_on та click_offset
    base_settings.click_on = "right"
    base_settings.click_offset = (0, 0)
    
    position = find_and_click("12.png", base_settings)
    if not position:
        return False
    
    time.sleep(1)
    
    return True

def handle_error(error_message: str):
    """Обробка помилок"""
    print("\n" + "=" * 60)
    print("🚨 ПОМИЛКА В РОБОТІ")
    print("=" * 60)
    print(f"Повідомлення про помилку: {error_message}")
    print("Робота завершена з помилкою.")
    print("=" * 60)

def main():
    """Головна функція"""
    try:
        success = main_workflow()
        
        if success:
            print("\n" + "=" * 60)
            print("✅ РОБОТУ УСПІШНО ЗАВЕРШЕНО!")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("❌ РОБОТУ ЗАВЕРШЕНО З ПОМИЛКАМИ")
            print("=" * 60)
            
    except Exception as e:
        handle_error(str(e))
        return False
    
    return True

if __name__ == "__main__":
    main()