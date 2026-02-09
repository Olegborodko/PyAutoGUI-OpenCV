# RDP Bot

PyAutoGUI + OpenCV бот для автоматизации задач.

## Установка

1. Скачайте [Anaconda](https://www.anaconda.com/download)

2. Создайте виртуальное окружение:
   ```bash
   conda create -n r_bot python=3.9
   ```

3. Активируйте окружение:
   ```bash
   conda activate r_bot
   ```

4. Установите зависимости:
   ```bash
   pip install pyautogui opencv-python pillow numpy
   ```

5. Проверьте установку:
   ```bash
   python -c "import pyautogui; import cv2; import PIL; import numpy; print('Все библиотеки загружены успешно!')"
   ```

## Установка проекта

```bash
git clone <project_url>
cd <project_folder>
```

## Тестирование

### Тест 1: Поиск изображения

1. Перейдите на [Google Translate](https://translate.google.com/) в виртуальной машине
2. Запустите скрипт:
   ```bash
   python find_image.py
   ```
   Бот должен найти и кликнуть по иконке документа

### Тест 2: Ввод текста

1. Перейдите на [Google](https://google.com/) в виртуальной машине
2. Поместите курсор в текстовое поле ввода
3. Запустите скрипт:
   ```bash
   python test_dupl_fixed.py
   ```
   Бот должен ввести текст "abc..." и нажать Enter
