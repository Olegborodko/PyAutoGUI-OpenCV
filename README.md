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
   pip install pyautogui opencv-python pillow numpy keyboard pyperclip pytesseract
   ```

5. Проверьте установку:
   ```bash
   python -c "import pyautogui; import cv2; import PIL; import numpy; import keyboard; import pyperclip; import pytesseract; print('Все библиотеки загружены успешно!')"
   ```

## Скачайте и установите git на компьютер

## Как запустить run.py с компьютера

1. **Открыть Анаконду** - запустите Anaconda Prompt
   
2. **Перейти в папку C:\rdp_bot\run**:
   ```bash
   cd C:\rdp_bot\run
   ```
   Или пошагово:
   ```bash
   cd ..
   cd ..
   cd rdp_bot
   cd run
   ```

3. **Активировать среду**:
   ```bash
   conda activate r_bot
   ```

4. **Запустить скрипт run.py**:
   ```bash
   python run.py
   ```

5. **Остановить скрипт** - нажмите комбинацию клавиш **Ctrl+Shift+Q**

## Запуск программы

Основная программа находится в файле `C:\rdp_bot\run\run.py`

Для запуска выполните:
```bash
cd C:\rdp_bot\run
python run.py
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