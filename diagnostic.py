import pyautogui
import time
import sys

print("=" * 60)
print("ДИАГНОСТИКА RDP АВТОМАТИЗАЦИИ 2026")
print("=" * 60)

# 1. Проверка что PyAutoGUI видит правильные нажатия
print("\n1. ТЕСТ БАЗОВОЙ ФУНКЦИОНАЛЬНОСТИ...")
print("Сейчас будет нажата клавиша 'A' в активном окне")
time.sleep(10)
pyautogui.press('a')
print("Нажата 'A'. Проверь, появилась ли буква в текстовом поле RDP?")

# 2. Тест альтернативных способов отправки F5
print("\n2. ТЕСТ РАЗНЫХ СПОСОБОВ ОТПРАВКИ F5...")
time.sleep(3)

f5_methods = [
    ("pyautogui.press('f5')", lambda: pyautogui.press('f5')),
    ("pyautogui.hotkey('ctrl', 'r')", lambda: pyautogui.hotkey('ctrl', 'r')),
    ("pyautogui.keyDown('f5'); keyUp('f5')", 
     lambda: (pyautogui.keyDown('f5'), pyautogui.keyUp('f5'))),
    ("Отправка через write", lambda: pyautogui.write('{f5}')),
]

for method_name, method_func in f5_methods:
    print(f"\n  Пробую: {method_name}")
    time.sleep(1)
    method_func()
    time.sleep(2)  # Ждём реакции

# 3. Тест в разных приложениях
print("\n3. ТЕСТ В РАЗНЫХ ПРИЛОЖЕНИЯХ RDP...")
print("Открой в RDP: 1) Браузер 2) Проводник 3) Блокнот")
time.sleep(5)

applications = [
    ("Браузер (Chrome/Edge)", 'f5'),
    ("Проводник (F5 обновляет список)", 'f5'),
    ("Блокнот (F5 вставляет время)", 'f5'),
]

for app_name, key in applications:
    print(f"\n  Тест в {app_name}. Нажимаю {key.upper()}...")
    time.sleep(3)
    pyautogui.press(key)
    time.sleep(2)

# 4. Проверка режимов RDP
print("\n4. ПРОВЕРКА РЕЖИМОВ RDP...")
print("""
ВНИМАНИЕ! Возможные причины в 2026:
1. Виртуализация клавиатуры в RDP
2. Безопасность Windows блокирует
3. Изменения в протоколе RDP
4. Требуется настройка разрешений
""")

print("\n" + "=" * 60)
print("РЕКОМЕНДАЦИЯ ПО ДИАГНОСТИКЕ:")
print("1. Попробуй в RDP: Браузер → Инструменты разработчика (F12)")
print("2. Затем запусти этот скрипт - должен сработать F12 в браузере")
print("3. Если F12 работает, а F5 нет - это защита RDP")
print("=" * 60)