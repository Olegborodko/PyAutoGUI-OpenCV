# Імпортуємо привітання
import greatings
import time
import pyautogui
import keyboard  # Для отслеживания горячих клавиш
import random

# Імпортуємо наші функції
from image_utils import SearchSettings, find_image, click_at_position
from random_utils import random_sleep

# Глобальная переменная для контроля выполнения
should_stop = False

def stop_program():
    """Функция для остановки программы по горячей клавише"""
    global should_stop
    should_stop = True
    print("\n🛑 Сигнал остановки получен! Завершаю текущий цикл...")

def find_and_click(image_name, settings):
    """Пошук зображення та клік по ньому. Повертає позицію або False"""
    print(f"\n🔍 Шукаю зображення '{image_name}'...")
    position = find_image(image_name, settings)
    
    if not position:
        print(f"❌ Не вдалося знайти зображення '{image_name}'.")
        return False
    
    print(f"✅ Зображення знайдено за координатами: {position}")
    
    if not click_at_position(position):
        print(f"❌ Не вдалося виконати клік для '{image_name}'.")
        return False

    return position

def check_image_on_screen(image_name, settings):
    """
    Перевіряє чи є зображення на екрані.
    НЕ рухає мишку, НЕ клікає. Просто повертає True/False.
    """
    print(f"\n🔍 Перевіряю '{image_name}' на екрані...")
    position = find_image(image_name, settings)
    
    if position:
        print(f"✅ ЗНАЙДЕНО на позиції {position}")
        return True
    else:
        print(f"❌ НЕ знайдено")
        return False

def run_random_images(settings, images_list):
    """
    Функція: випадкова кількість картинок шукається, ті що знайдені - клікаються.
    """
    if not images_list:
        return True
    
    # Скільки картинок шукаємо (від 1 до всіх)
    num = random.randint(1, len(images_list))
    
    # Перемішуємо і беремо перші num
    random.shuffle(images_list)
    to_search = images_list[:num]
    
    print(f"🎲 Шукаємо {num} картинок: {to_search}")
    
    for img in to_search:
        if not find_and_click(img, settings):
            return False
        random_sleep(0.5, 2)
    
    return True

def move_mouse_randomly():
    """Просте водіння мишкою по екрану до 1.5 секунд, повільно і по-людськи"""
    print("🖱️ Рухаю мишкою...")
    
    # Рандомний час руху (0.3 - 1.5 секунди)
    duration = random.uniform(0.3, 1.5)
    start_time = time.time()
    
    # Отримуємо розміри екрану
    screen_width, screen_height = pyautogui.size()
    
    while time.time() - start_time < duration:
        # Випадкові координати на екрані
        x = random.randint(0, screen_width - 1)
        y = random.randint(0, screen_height - 1)
        
        # Повільна швидкість руху (0.5 - 1.2 секунди)
        move_duration = random.uniform(0.5, 1.2)
        
        pyautogui.moveTo(x, y, duration=move_duration)
        
        # Пауза між рухами
        time.sleep(random.uniform(0.1, 0.3))
    
    print("✅ Рух мишкою завершено")

def main_workflow():
    """Основной рабочий процесс (один проход - один choice)"""
    global should_stop
    
    # Базові налаштування пошуку зображення
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
    
    # Рух мишкою перед вибором
    move_mouse_randomly()
    
    # Випадковий вибір: 1 або 2
    choice = random.randint(1, 2)
    
    if choice == 1:
        # ВАРІАНТ 1: клік по 11.png, потім випадкові з [18, 9, 10]
        print("\n=== ВАРІАНТ 1: 11.png ===")
        
        # Клікаємо 11.png поки не з'явиться 18.png
        while True:
            if not find_and_click("11.png", base_settings):
                return False
            
            random_sleep(0.5, 2)
            
            # Перевіряємо чи є 18.png
            if check_image_on_screen("18.png", base_settings):
                print("✅ 18.png знайдено, рухаємось далі")
                break
            else:
                print("🔄 18.png не знайдено, повторюємо 11.png...")
        
        random_sleep(0.5, 2)
        
        # Випадкові з 18, 9, 10
        if not run_random_images(base_settings, ["18.png", "9.png", "10.png"]):
            return False
    
    else:
        # ВАРІАНТ 2: клік по 21.png, потім можливо ще один
        print("\n=== ВАРІАНТ 2: 21.png ===")
        
        # Клікаємо 21.png поки не з'явиться 22.png
        while True:
            if not find_and_click("21.png", base_settings):
                return False
            
            random_sleep(0.5, 2)
            
            # Перевіряємо чи є 22.png
            if check_image_on_screen("22.png", base_settings):
                print("✅ 22.png знайдено, рухаємось далі")
                break
            else:
                print("🔄 22.png не знайдено, повторюємо 21.png...")
        
        random_sleep(0.5, 2)
        
        # Наводимо мишку на низ 22.png і клікаємо на 10px нижче
        bottom_settings = SearchSettings(
            confidence=0.7,
            grayscale=False,
            blur=0,
            scales=[0.9, 1.0, 1.1],
            click_on="bottom",
            click_offset=(0, 10),
            max_attempts=3,
            search_timeout=10.0
        )
        find_and_click("22.png", bottom_settings)
        
        random_sleep(0.5, 2)
        
        # 50% шанс ввести 3 випадкові символи (по-людськи)
        if random.random() < 0.5:
            # Генеруємо 3 випадкові символи (англійські літери або цифри)
            chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            text = ''.join(random.choice(chars) for _ in range(3))
            print(f"🎲 Вводимо текст: {text}")
            
            # Вводимо кожен символ окремо з випадковою затримкою
            for char in text:
                pyautogui.press(char)
                # Рандомна затримка між натисканнями (0.05 - 0.8 сек)
                time.sleep(random.uniform(0.05, 0.8))
            
            random_sleep(0.5, 1)
    
    # Рух мишкою після всього коду
    move_mouse_randomly()
    
    return True

def main():
    """Головна функція"""
    global should_stop
    
    print("\n" + "=" * 60)
    print("🚀 ПРОГРАМА ЗАПУЩЕНА")
    print("📌 Для зупинки натисніть Ctrl+F8")
    print("=" * 60)
    
    # Регистрируем горячую клавишу для остановки (Ctrl+F8 более надежно)
    keyboard.add_hotkey('ctrl+F8', stop_program)
    
    cycle_count = 0
    
    try:
        while not should_stop:
            cycle_count += 1
            print(f"\n🔄 ЦИКЛ #{cycle_count}")
            print("-" * 40)
            
            success = main_workflow()
            
            if not success:
                print("❌ РОБОТУ ЗАВЕРШЕНО З ПОМИЛКАМИ - ПРОГРАМА ЗУПИНЯЄТЬСЯ")
                break
            
            print(f"\n✅ Цикл #{cycle_count} успішно завершено!")
            
            # Небольшая пауза между циклами
            if not should_stop:
                print("⏳ Підготовка до наступного циклу...")
                time.sleep(1)
            
    except Exception as e:
        print(f"\n❌ Помилка: {e}")
        return False
    finally:
        # Убираем обработчик горячей клавиши
        keyboard.unhook_all()
    
    print("\n")
    print("🏁 ПРОГРАМА ЗУПИНЕНА")
    
    return True

if __name__ == "__main__":
    main()
