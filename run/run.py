# Імпортуємо привітання
import greatings
import time
import pyautogui

# Імпортуємо наші функції
from image_utils import SearchSettings, find_image, click_at_position
from text_utils import copy_text_from_position, select_and_delete_from_position, paste_text
from random_utils import random_sleep
from error_handler import handle_error

def find_and_click(image_name, settings):
    """Пошук зображення та клік по ньому. Повертає позицію або False"""
    print(f"\n🔍 Шукаю зображення '{image_name}'...")
    position = find_image(image_name, settings)
    
    if not position:
        print(f"❌ Не вдалося знайти зображення '{image_name}'.")
        return False
    
    print(f"✅ Зображення знайдено за координатами: {position}")
    
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
    # center, top, bottom, left, right, ...
    base_settings = SearchSettings(
        confidence=0.7,
        grayscale=False,
        blur=0,
        scales=[0.9, 1.0, 1.1],
        click_on="center",
        click_offset=(0, 0),
        max_attempts=3,
        search_timeout=10.0
    )
    
    # КРОК 1: Пошук та клік по зображенню
    base_settings.click_on = "bottom"
    base_settings.click_offset = (0, 3) # на 3px нижче
    position = find_and_click("1.png", base_settings)
    if not position:
        return False
    
    # Рандомна затримка між кроками
    random_sleep(0.3, 1)
    
    # КРОК 2: Копіювання тексту з позиції
    copied_text_from_steep2 = copy_text_from_coords(position[0], position[1])
    if not copied_text_from_steep2:
        return False
    
    # Рандомна затримка між кроками
    random_sleep(0.3, 1)
    
    # КРОК 3: Пошук та клік по зображенню хром браузера
    base_settings.click_on = "center"
    base_settings.click_offset = (0, 0)
    
    position = find_and_click("11.png", base_settings)
    if not position:
        return False
    
    print("\n⏳ Затримка 3 секунд щоб відкрився браузер")
    time.sleep(3)
    
    # КРОК 4: Пошук та клік
    position = find_and_click("9.png", base_settings)
    if not position:
        return False
    
    random_sleep(1, 2)
    
    # КРОК 5: Пошук та клік з іншими налаштуваннями
    base_settings.click_on = "right"
    base_settings.click_offset = (3, 0) # на 3px правіше
    
    position = find_and_click("12.png", base_settings)
    if not position:
        return False
    
    random_sleep(0.3, 1)

    # КРОК 6: Виділяємо та видаляємо текст з текстового поля
    print("\n✂️ Виділяю та видаляю текст з текстового поля...")
    deleted_text = select_and_delete_from_position(position[0], position[1])
    
    if not deleted_text:
        print("❌ Не вдалося виділити та видалити текст")
        return False
    
    print(f"✅ Текст успішно видалено: {deleted_text[:100]}..." if len(deleted_text) > 100 else f"✅ Текст успішно видалено: {deleted_text}")
    
    random_sleep(0.3, 1)

    # КРОК 7: Пошук та клік
    base_settings.click_on = "right"
    base_settings.click_offset = (3, 0) # на 3px правіше
    
    position = find_and_click("12.png", base_settings)
    if not position:
        return False
    
    random_sleep(0.5, 1)
    
    # КРОК 8
    if not paste_text(copied_text_from_steep2):
        print("❌ Не вдалося вставити текст")
        return False
    
    random_sleep(0.5, 1)
    
    # КРОК 9
    print("\n↵ Натискаю клавішу Enter...")
    pyautogui.press('enter')

    random_sleep(1, 2)

    # КРОК 10
    base_settings.click_on = "center"
    base_settings.click_offset = (0, 0)
    
    position = find_and_click("10.png", base_settings)
    if not position:
        return False
    
    random_sleep(1, 2)

    # КРОК 11
    base_settings.click_on = "bottom"
    base_settings.click_offset = (0, 1)
    position = find_and_click("13.png", base_settings)
    if not position:
        return False
    
    random_sleep(0.5, 1)

    # КРОК 12
    if not paste_text(copied_text_from_steep2):
        print("❌ Не вдалося вставити текст")
        return False
    
    random_sleep(0.5, 1)

    # КРОК 13
    print("\n↵ Натискаю клавішу Enter...")
    pyautogui.press('enter')

    # КРОК 14
    position = find_and_click("14.png", base_settings)
    if not position:
        return False
    
    random_sleep(1, 2)

    
    
    return True

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