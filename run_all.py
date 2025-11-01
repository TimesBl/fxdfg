"""
ГЛАВНЫЙ ФАЙЛ ЗАПУСКА
Запускает всю систему Timelyx Portfolio одной командой

Использование:
    python run_all.py
"""
import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

print("\n" + "="*70)
print("🚀 TIMELYX PORTFOLIO SYSTEM - ПОЛНЫЙ ЗАПУСК")
print("="*70 + "\n")

# ==================== ШАГ 1: ЗАПУСК AUTOSTART ====================
print("📦 Шаг 1: Создание и запуск веб-сервера...\n")

if not Path('autostart.py').exists():
    print("❌ Файл autostart.py не найден!")
    print("💡 Убедитесь что файл autostart.py находится в той же папке")
    sys.exit(1)

# Запускаем autostart.py в отдельном процессе
try:
    print("🌐 Запуск Flask сервера...")
    server_process = subprocess.Popen(
        [sys.executable, 'autostart.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Ждём пока сервер запустится
    time.sleep(3)
    
    if server_process.poll() is None:
        print("✅ Flask сервер запущен успешно!")
        print("📍 Адрес: http://localhost:5000\n")
    else:
        print("❌ Ошибка запуска сервера")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Ошибка: {e}")
    sys.exit(1)

# ==================== ШАГ 2: TELEGRAM БОТ (ОПЦИОНАЛЬНО) ====================
print("="*70)
print("🤖 Шаг 2: Запуск Telegram бота (опционально)")
print("="*70 + "\n")

if Path('telegram_bot.py').exists():
    answer = input("Запустить Telegram бота? (y/n): ").lower()
    
    if answer in ['y', 'yes', 'д', 'да', '']:
        try:
            print("\n🤖 Запуск Telegram бота...")
            bot_process = subprocess.Popen(
                [sys.executable, 'telegram_bot.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            time.sleep(2)
            
            if bot_process.poll() is None:
                print("✅ Telegram бот запущен успешно!\n")
            else:
                print("⚠️ Бот не запустился, но сайт работает\n")
                bot_process = None
        except Exception as e:
            print(f"⚠️ Ошибка запуска бота: {e}")
            print("💡 Сайт продолжает работать без бота\n")
            bot_process = None
    else:
        print("⏭️ Бот не будет запущен\n")
        bot_process = None
else:
    print("ℹ️ Файл telegram_bot.py не найден")
    print("💡 Сайт будет работать без Telegram бота\n")
    bot_process = None

# ==================== ШАГ 3: ОТКРЫТИЕ САЙТА ====================
print("="*70)
print("🌐 Шаг 3: Открытие сайта в браузере")
print("="*70 + "\n")

try:
    # Открываем index.html
    index_path = Path('index.html').absolute()
    webbrowser.open(f'file://{index_path}')
    print("✅ Сайт открыт в браузере!\n")
except Exception as e:
    print(f"⚠️ Не удалось открыть браузер: {e}")
    print("💡 Откройте index.html вручную\n")

# ==================== ИНФОРМАЦИЯ ====================
print("="*70)
print("🎉 ВСЁ ГОТОВО! СИСТЕМА ЗАПУЩЕНА")
print("="*70)
print("\n📍 ЧТО РАБОТАЕТ:\n")
print(f"✅ Flask сервер: http://localhost:5000")
print(f"✅ API отзывов: http://localhost:5000/api/reviews")
print(f"✅ Веб-сайт: открыт в браузере")

if bot_process and bot_process.poll() is None:
    print(f"✅ Telegram бот: работает")
else:
    print(f"⚪ Telegram бот: не запущен")

print("\n💡 ПОЛЕЗНАЯ ИНФОРМАЦИЯ:\n")
print("• Для остановки нажмите Ctrl+C")
print("• Отзывы сохраняются в reviews.json")
print("• Логи бота в bot.log (если бот запущен)")
print("• Сайт автоматически обновляет отзывы каждые 30 секунд")

print("\n" + "="*70)
print("📱 КОНТАКТЫ И ПОДДЕРЖКА")
print("="*70)
print("Telegram: @timelyx")
print("GitHub: github.com/timelyx")
print("="*70 + "\n")

# ==================== МОНИТОРИНГ ====================
print("⏳ Система работает... (Ctrl+C для остановки)\n")

try:
    # Мониторим процессы
    while True:
        time.sleep(1)
        
        # Проверяем что сервер работает
        if server_process.poll() is not None:
            print("\n❌ Сервер остановился!")
            break
        
        # Проверяем бота если он запущен
        if bot_process and bot_process.poll() is not None:
            print("\n⚠️ Telegram бот остановился, но сервер продолжает работать")
            bot_process = None

except KeyboardInterrupt:
    print("\n\n" + "="*70)
    print("🛑 ОСТАНОВКА СИСТЕМЫ")
    print("="*70 + "\n")
    
    # Останавливаем процессы
    print("🔴 Остановка Flask сервера...")
    try:
        server_process.terminate()
        server_process.wait(timeout=5)
        print("✅ Flask сервер остановлен")
    except:
        server_process.kill()
        print("✅ Flask сервер принудительно остановлен")
    
    if bot_process:
        print("🔴 Остановка Telegram бота...")
        try:
            bot_process.terminate()
            bot_process.wait(timeout=5)
            print("✅ Telegram бот остановлен")
        except:
            bot_process.kill()
            print("✅ Telegram бот принудительно остановлен")
    
    print("\n👋 Система полностью остановлена. До встречи!")
    print("="*70 + "\n")

except Exception as e:
    print(f"\n❌ Ошибка: {e}")
    # Останавливаем всё при ошибке
    if server_process:
        server_process.kill()
    if bot_process:
        bot_process.kill()