"""Метод 10: UIA отримання тексту"""
import time
import pyperclip

# Спроба імпортувати uiautomation
try:
    import uiautomation as auto
    HAS_UIA = True
except ImportError:
    HAS_UIA = False

def clear_clipboard():
    """Очистити буфер обміну"""
    try:
        pyperclip.copy('')
        time.sleep(0.3)
        if pyperclip.paste() == '':
            return True
        else:
            pyperclip.copy('')
            time.sleep(0.5)
            return pyperclip.paste() == ''
    except Exception as e:
        print(f"⚠️ Помилка очищення буфера: {e}")
        return False

def test_uia_get_text(x, y):
    """Метод 10: UIA отримання тексту"""
    if not HAS_UIA:
        print("❌ Бібліотека uiautomation не встановлена")
        return None
    
    print("\n🧪 Метод 10: UIA отримання тексту")
    
    try:
        # Очищаємо буфер обміну перед тестом UIA
        print("🧹 Очищаю буфер обміну перед тестом UIA...")
        clear_clipboard()
        
        # Отримання елемента за координатами
        print(f"🔍 Отримую елемент за координатами ({x}, {y})...")
        control = auto.ControlFromPoint(x, y)
        
        if not control:
            print("❌ Не вдалося отримати елемент за координатами")
            return None
        
        # Спроба отримати текст різними способами
        text = None
        
        # Спосіб 1: GetValuePattern (для текстових полів)
        try:
            print("   Спробую GetValuePattern...")
            value_pattern = control.GetValuePattern()
            if value_pattern:
                text = value_pattern.Value
                if text and text.strip():
                    print(f"   ✅ GetValuePattern: '{text[:50]}...'")
                else:
                    print("   ❌ GetValuePattern повернув порожній текст")
        except Exception as e:
            print(f"   ⚠️ GetValuePattern помилка: {e}")
        
        # Спосіб 2: LegacyValue
        if not text or not text.strip():
            try:
                print("   Спробую LegacyValue...")
                text = control.LegacyValue
                if text and text.strip():
                    print(f"   ✅ LegacyValue: '{text[:50]}...'")
                else:
                    print("   ❌ LegacyValue повернув порожній текст")
            except Exception as e:
                print(f"   ⚠️ LegacyValue помилка: {e}")
        
        # Спосіб 3: Name property
        if not text or not text.strip():
            try:
                print("   Спробую Name property...")
                text = control.Name
                if text and text.strip():
                    print(f"   ✅ Name: '{text[:50]}...'")
                else:
                    print("   ❌ Name повернув порожній текст")
            except Exception as e:
                print(f"   ⚠️ Name помилка: {e}")
        
        if text and text.strip():
            text = text.strip()
            print(f"✅ UIA отримав текст: '{text[:50]}...'")
            return text
        else:
            print("❌ UIA не зміг отримати текст")
            return None
            
    except Exception as e:
        print(f"❌ Помилка UIA: {e}")
        return None