import pyautogui
import time

print("=" * 50)
print("ТЕСТ: Ручная активация RDP окна")
print("=" * 50)
print("\nИНСТРУКЦИЯ:")
print("1. Запусти этот скрипт")
print("2. У тебя есть 10 секунд чтобы:")
print("   - Открыть/развернуть окно RDP")
print("   - Сделать его активным (кликнуть в него)")
print("3. Скрипт выполнит действия в активном окне")
print("=" * 50)

# Ожидание 10 секунд
for i in range(10, 0, -1):
    print(f"Осталось {i} секунд...")
    time.sleep(1)

print("\nВыполняю действия...")

# Последовательность действий для имитации активности
actions = [
    ('F5 (Обновить)', lambda: pyautogui.press('f5')),
    ('TAB (Переместить фокус)', lambda: pyautogui.press('tab')),
    ('ESC (Отмена)', lambda: pyautogui.press('esc')),
    ('Клик в центр', lambda: pyautogui.click(pyautogui.size()[0]//2, pyautogui.size()[1]//2)),
    ('Alt+Left (Назад)', lambda: pyautogui.hotkey('alt', 'left')),
]

for action_name, action_func in actions:
    print(f"  → {action_name}")
    action_func()
    time.sleep(1.5)  # Пауза между действиями

print("\n" + "=" * 50)
print("Готово! Проверь в RDP:")
print("1. Обновилась ли страница?")
print("2. Фокус переместился?")
print("3. Произошёл клик в центре?")
print("=" * 50)