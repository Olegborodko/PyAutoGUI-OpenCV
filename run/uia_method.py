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
    """Очистити буфер обміну (покращена версія)"""
    try:
        # Спроба використання win32clipboard, якщо доступно
        try:
            import win32clipboard
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.CloseClipboard()
            time.sleep(0.3)
            return True
        except ImportError:
            pass  # Продовжуємо з pyperclip
        except Exception as e:
            print(f"⚠️ Помилка очищення буфера через win32clipboard: {e}")
        
        # Резервний варіант з pyperclip
        pyperclip.copy('')
        time.sleep(0.4)
        if pyperclip.paste() == '':
            return True
        else:
            pyperclip.copy('')
            time.sleep(0.6)
            return pyperclip.paste() == ''
    except Exception as e:
        print(f"⚠️ Помилка очищення буфера: {e}")
        return False

def test_uia_get_text(x, y):
    """Метод 10: UIA отримання тексту (покращена версія для RDP)"""
    if not HAS_UIA:
        print("❌ Бібліотека uiautomation не встановлена")
        return None
    
    print("\n🧪 Метод 10: UIA отримання тексту (покращена версія)")
    
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
        
        print(f"   📋 Тип елемента: {control.ControlTypeName}")
        print(f"   🏷️  Назва елемента: '{control.Name}'")
        
        # Якщо це не текстове поле, шукаємо текстове поле серед дочірніх елементів
        if control.ControlTypeName not in ['EditControl', 'DocumentControl', 'TextControl']:
            print("   🔍 Шукаю текстове поле серед дочірніх елементів...")
            
            # Пошук текстового поля серед дочірніх елементів
            text_control = None
            
            # Спроба 1: Шукаємо EditControl
            try:
                edit_control = control.GetFirstChildControl(ControlType=auto.ControlType.EditControl)
                if edit_control:
                    text_control = edit_control
                    print("   ✅ Знайдено EditControl")
            except:
                pass
            
            # Спроба 2: Шукаємо DocumentControl
            if not text_control:
                try:
                    doc_control = control.GetFirstChildControl(ControlType=auto.ControlType.DocumentControl)
                    if doc_control:
                        text_control = doc_control
                        print("   ✅ Знайдено DocumentControl")
                except:
                    pass
            
            # Спроба 3: Шукаємо TextControl
            if not text_control:
                try:
                    text_ctrl = control.GetFirstChildControl(ControlType=auto.ControlType.TextControl)
                    if text_ctrl:
                        text_control = text_ctrl
                        print("   ✅ Знайдено TextControl")
                except:
                    pass
            
            # Спроба 4: Рекурсивний пошук серед усіх дочірніх елементів
            if not text_control:
                try:
                    print("   🔍 Рекурсивний пошук текстового поля...")
                    for child in control.GetChildren():
                        try:
                            if child.ControlTypeName in ['EditControl', 'DocumentControl', 'TextControl']:
                                text_control = child
                                print(f"   ✅ Знайдено {child.ControlTypeName}")
                                break
                        except:
                            continue
                except Exception as e:
                    print(f"   ⚠️ Помилка рекурсивного пошуку: {e}")
            
            # Якщо знайшли текстове поле, використовуємо його
            if text_control:
                control = text_control
                print(f"   📋 Тип знайденого елемента: {control.ControlTypeName}")
        
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
        
        # Спосіб 3: TextPattern для DocumentControl
        if not text or not text.strip():
            try:
                print("   Спробую TextPattern...")
                text_pattern = control.GetTextPattern()
                if text_pattern:
                    text_range = text_pattern.DocumentRange
                    if text_range:
                        text = text_range.GetText(-1)
                        if text and text.strip():
                            print(f"   ✅ TextPattern: '{text[:50]}...'")
                        else:
                            print("   ❌ TextPattern повернув порожній текст")
            except Exception as e:
                print(f"   ⚠️ TextPattern помилка: {e}")
        
        # Спосіб 4: Name property (останній варіант)
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
        
        # Спосіб 5: Отримання тексту з дочірніх текстових елементів
        if not text or not text.strip():
            try:
                print("   Спробую отримати текст з дочірніх текстових елементів...")
                all_text = []
                for child in control.GetChildren():
                    try:
                        child_text = child.Name
                        if child_text and child_text.strip():
                            all_text.append(child_text.strip())
                    except:
                        continue
                
                if all_text:
                    text = " ".join(all_text)
                    print(f"   ✅ Текст з дочірніх елементів: '{text[:50]}...'")
            except Exception as e:
                print(f"   ⚠️ Помилка отримання тексту з дочірніх елементів: {e}")
        
        if text and text.strip():
            text = text.strip()
            # Перевіряємо, чи це не заголовок вікна
            if "Input Capture Window" in text or "Window" in text and len(text) < 50:
                print(f"   ⚠️ Можливо це заголовок вікна, а не текст: '{text}'")
                # Спробуємо отримати реальний текст іншим способом
                return None
            else:
                print(f"✅ UIA отримав текст: '{text[:50]}...'")
                return text
        else:
            print("❌ UIA не зміг отримати текст")
            return None
            
    except Exception as e:
        print(f"❌ Помилка UIA: {e}")
        return None
