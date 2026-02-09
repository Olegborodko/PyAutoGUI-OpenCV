import time
import ctypes

print("Тест Scan Code метода (исправление дублирования)")
print("У тебя 20 секунд чтобы открыть RDP окно и поставить курсор в текстовое поле")
print("Таймер пошёл...")

# Ждём 20 секунд
for i in range(20, 0, -1):
    print(f"Осталось: {i} сек")
    time.sleep(1)

print("\nНачинаю тест...")
print("=" * 50)

def send_scancode_safe(scancode, delay=0.1):
    """Безопасная отправка scan code с задержкой"""
    KEYEVENTF_SCANCODE = 0x0008
    KEYEVENTF_KEYUP = 0x0002
    
    # Нажимаем клавишу
    ctypes.windll.user32.keybd_event(0, scancode, KEYEVENTF_SCANCODE, 0)
    time.sleep(delay)  # Задержка перед отпусканием
    
    # Отпускаем клавишу
    ctypes.windll.user32.keybd_event(0, scancode, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0)
    time.sleep(0.05)

# Тест 1: Проверка задержек (буквы A-E)
print("\nТест 1: Буквы A-E с разными задержками")
scan_codes = {
    'A': 0x1E,
    'B': 0x30,
    'C': 0x2E,
    'D': 0x20,
    'E': 0x12
}

for char, code in scan_codes.items():
    print(f"Печатаю '{char}' (задержка 0.2 сек)")
    send_scancode_safe(code, delay=0.2)
    time.sleep(1)  # Пауза между буквами

# Тест 2: Цифры 1-3
print("\n\nТест 2: Цифры 1-3")
digits = {'1': 0x02, '2': 0x03, '3': 0x04}

for digit, code in digits.items():
    print(f"Печатаю '{digit}'")
    send_scancode_safe(code, delay=0.15)
    time.sleep(0.8)

# Тест 3: Пробел и Enter
print("\n\nТест 3: Пробел и Enter")
print("Должно появиться: 'ABC 123'")

# Печатаем ABC
for char in ['A', 'B', 'C']:
    send_scancode_safe(scan_codes[char], delay=0.15)
    time.sleep(0.1)

# Пробел (Space)
print("Пробел")
ctypes.windll.user32.keybd_event(0, 0x39, 0x0008, 0)  # Space down
time.sleep(0.15)
ctypes.windll.user32.keybd_event(0, 0x39, 0x0008 | 0x0002, 0)  # Space up
time.sleep(0.5)

# Печатаем 123
for digit in ['1', '2', '3']:
    send_scancode_safe(digits[digit], delay=0.15)
    time.sleep(0.1)

# Enter
print("Enter (новая строка)")
ctypes.windll.user32.keybd_event(0, 0x1C, 0x0008, 0)  # Enter down
time.sleep(0.15)
ctypes.windll.user32.keybd_event(0, 0x1C, 0x0008 | 0x0002, 0)  # Enter up

print("\n" + "=" * 50)
print("Тест завершён!")
print("\nПроверь в RDP:")
print("1. Появились ли буквы A, B, C, D, E? (без дублирования?)")
print("2. Появились ли цифры 1, 2, 3?")
print("3. Появилась ли строка 'ABC 123' с пробелом?")
print("4. Enter перевёл на новую строку?")