PyAutoGUI + OpenCV

1. https://www.anaconda.com/download

2. conda create -n r_bot python=3.9

3. conda activate r_bot

4. pip install pyautogui opencv-python pillow numpy

5. python -c "import pyautogui; import cv2; import PIL; import numpy; print('Все библиотеки загружены успешно!')"

6. git clone project

7. в папці проекта запускаєм скрипти для тестування - 

   Тест перший. переходим в віртуальній машині на https://translate.google.com/
   Запускаєм скрипт python find_image.py
   має мишка нажати на іконку документа

   Другий тест. переходим в віртуальній машині на https://google.com/
   Курсор ставим на текстове поле для вводу тексту
   Запускаєм скрипт python test_dupl_fixed.py
   має написатися - abc... та нажатися Enter
   

