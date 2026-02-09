import pyautogui
import time
import ctypes

print("Тест клавиатуры через RDP")
print("У тебя 20 секунд чтобы открыть RDP окно и поставить курсор в текстовое поле")
print("Таймер пошёл...")

# Ждём 20 секунд
for i in range(20, 0, -1):
    print(f"Осталось: {i} сек")
    time.sleep(1)

print("\nНачинаю тест всех методов...")
print("=" * 50)

# Уникальный символ для каждого теста
tests = []

# Методы PyAutoGUI
tests.append(("1. PyAutoGUI press('A')", lambda: pyautogui.press('a')))
tests.append(("2. PyAutoGUI press('B')", lambda: pyautogui.press('b')))
tests.append(("3. PyAutoGUI press('C')", lambda: pyautogui.press('c')))

tests.append(("4. PyAutoGUI typewrite('D')", lambda: pyautogui.typewrite('d')))
tests.append(("5. PyAutoGUI typewrite('E')", lambda: pyautogui.typewrite('e')))

tests.append(("6. PyAutoGUI write('F')", lambda: pyautogui.write('f')))
tests.append(("7. PyAutoGUI write('G')", lambda: pyautogui.write('g')))

tests.append(("8. PyAutoGUI keyDown/keyUp('H')", 
              lambda: (pyautogui.keyDown('h'), time.sleep(0.05), pyautogui.keyUp('h'))))

tests.append(("9. PyAutoGUI keyDown/keyUp('I')",
              lambda: (pyautogui.keyDown('i'), time.sleep(0.05), pyautogui.keyUp('i'))))

# Windows API методы
def win_api(char):
    """Windows API для символа"""
    # Получаем код клавиши из символа (прописная буква)
    vk_code = ord(char.upper())
    KEYEVENTF_KEYDOWN = 0x0000
    KEYEVENTF_KEYUP = 0x0002
    
    ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_KEYDOWN, 0)
    time.sleep(0.02)
    ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)

tests.append(("10. Windows API keybd_event('J')", lambda: win_api('j')))
tests.append(("11. Windows API keybd_event('K')", lambda: win_api('k')))
tests.append(("12. Windows API keybd_event('L')", lambda: win_api('l')))

# Scan Code методы
def scancode(char):
    """Scan code для символа (раскладка US)"""
    # Маппинг символов на scan codes (US раскладка)
    scan_map = {
        'm': 0x32,  # M
        'n': 0x31,  # N
        'o': 0x18,  # O
        'p': 0x19,  # P
    }
    
    if char.lower() in scan_map:
        KEYEVENTF_SCANCODE = 0x0008
        scan = scan_map[char.lower()]
        ctypes.windll.user32.keybd_event(0, scan, KEYEVENTF_SCANCODE, 0)
        time.sleep(0.02)
        ctypes.windll.user32.keybd_event(0, scan, KEYEVENTF_SCANCODE | 0x0002, 0)

tests.append(("13. Scan Code('M')", lambda: scancode('m')))
tests.append(("14. Scan Code('N')", lambda: scancode('n')))

# Запускаем все тесты
for test_name, test_func in tests:
    print(f"\nТестирую: {test_name}")
    try:
        # Выполняем тестовую функцию
        if isinstance(test_func(), tuple):  # Если функция возвращает кортеж действий
            for action in test_func():
                if callable(action):
                    action()
        else:
            test_func()
        print("✓ Метод выполнен")
    except Exception as e:
        print(f"✗ Ошибка: {e}")
    
    time.sleep(1)  # Пауза между тестами

print("\n" + "=" * 50)
print("Все тесты завершены!")
print("\nПРОВЕРЬ В RDP (в текстовом поле):")
print("Появились ли символы A, B, C, D, E, F, G, H, I, J, K, L, M, N?")
print("Какие именно появились?")
print("\nЕсли символ появился - значит метод работает.")