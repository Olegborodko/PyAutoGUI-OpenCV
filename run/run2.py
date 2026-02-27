# Імпортуємо привітання
import greatings
import time
import pyautogui
import keyboard  # Для отслеживания горячих клавиш

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

def main_workflow():
    """Основной рабочий процесс (пока пустой - будут добавляться шаги)"""
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
    
    # КРОК 1: Пошук та клік
    position = find_and_click("18.png", base_settings)
    if not position:
        return False
    
    random_sleep(0.5, 3)
    
    # Заглушка - пока просто ожидание
    time.sleep(1)
    
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
