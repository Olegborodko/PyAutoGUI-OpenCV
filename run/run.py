print("=" * 60)
print("ІНСТРУКЦІЇ ДЛЯ ПІДГОТОВКИ RDP ВІКНА")
print("=" * 60)

print("\nІНСТРУКЦІЯ:")
print("1. Відкрий віддалений рабочий стіл з потрібними вкладками")
print("3. Активуй вікно (клікни в нього), перше вікно з Latest Accession # кодом")
print("4. У тебе є 15 секунд для підготовки")

print("\n" + "=" * 60)

import time

# Відлік 15 секунд
for i in range(15, 0, -1):
    print(f"Старт через {i} секунд...")
    time.sleep(1)

print("\n✓ ГОТОВО! Починаю роботу...")

# Імпортуємо нашу функцію
from image_utils import SearchSettings, find_and_click_image

# Налаштування пошуку (можна змінювати)
settings = SearchSettings(
    confidence=0.7,          # Чутливість розпізнавання
    grayscale=False,         # Ч/Б пошук
    blur=0,                  # Розмиття
    scales=[0.9, 1.0, 1.1],  # Масштаби для пошуку
    click_on="bottom",       # Де клікати: "center", "top", "bottom", "left", "right"
    click_offset=(0, -3),     # Зміщення кліку (x, y)
    max_attempts=3,          # Кількість спроб
    search_timeout=10.0      # Таймаут пошуку
)

# Приклад використання:
# Шукаємо та клікаємо по зображенню "button.png" в папці images
success = find_and_click_image("1.png", settings)

if success:
    print("\n✅ Завдання виконано успішно!")
else:
    print("\n❌ Не вдалося виконати завдання")