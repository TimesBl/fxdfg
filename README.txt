# Timelyx Portfolio System - Инструкция по развертыванию на хостинге

## 📦 Файлы в архиве:
- app.py - основное Flask приложение
- passenger_wsgi.py - для запуска на хостинге (Passenger)
- wsgi.py - альтернатива для Gunicorn
- requirements.txt - зависимости Python
- .htaccess - конфигурация Apache
- index.html - веб-интерфейс
- reviews.json - файл с отзывами
- README.txt - эта инструкция

## 🚀 Инструкция по установке на хостинг:

### Шаг 1: Загрузка файлов
1. Загрузите все файлы на хостинг через FTP или файловый менеджер
2. Разместите в корневой директории вашего домена

### Шаг 2: Настройка виртуального окружения
Подключитесь к хостингу по SSH и выполните:

```bash
# Создание виртуального окружения
python3 -m venv venv

# Активация
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

### Шаг 3: Настройка файлов

#### В файле passenger_wsgi.py:
Замените путь к виртуальному окружению:
```python
VENV_PATH = os.path.expanduser('~/venv/lib/python3.9/site-packages')
```
На ваш путь (узнайте у хостинг-провайдера)

#### В файле .htaccess:
Замените:
- USERNAME - на ваш логин хостинга
- DOMAIN.COM - на ваш домен
- путь к Python - на путь к вашему виртуальному окружению

#### В файле app.py:
В списке ALLOWED_ORIGINS замените:
```python
'https://yourdomain.com'  # на ваш реальный домен
```

### Шаг 4: Права доступа
Установите права на файлы:
```bash
chmod 755 passenger_wsgi.py
chmod 644 app.py
chmod 644 reviews.json
chmod 644 .htaccess
```

### Шаг 5: Telegram бот (опционально)
Если хотите использовать Telegram бота для сбора отзывов:
1. Загрузите telegram_bot.py на хостинг
2. Измените API_URL в telegram_bot.py на URL вашего сайта
3. Запустите бота: `python telegram_bot.py`

## 🎯 Популярные хостинги и особенности:

### Beget.com:
- Используйте passenger_wsgi.py
- Python 3.9+ доступен
- Путь к venv: /home/username/.local/share/virtualenvs/

### Timeweb:
- Используйте index.wsgi вместо passenger_wsgi.py
- Поддержка через панель управления
- Документация: https://timeweb.com/ru/docs/

### Reg.ru:
- Поддержка Flask через ISPmanager
- Используйте passenger_wsgi.py
- Включите CGI и Python в настройках домена

### PythonAnywhere (бесплатный):
- Не нужен passenger_wsgi.py
- Настройка через веб-интерфейс
- Ограничение: 100 000 запросов/день

## ❓ Проблемы и решения:

### "500 Internal Server Error":
1. Проверьте логи хостинга
2. Убедитесь что все пути правильные
3. Проверьте права на файлы

### Отзывы не загружаются:
1. Проверьте что reviews.json существует
2. Проверьте права на запись (chmod 666 reviews.json)
3. Убедитесь что CORS настроен правильно

### Telegram бот не отправляет отзывы:
1. Проверьте что API_URL указывает на ваш домен
2. Убедитесь что сервер доступен извне
3. Проверьте CORS настройки в app.py

## 📞 Контакты:
Если возникли проблемы - напишите в Telegram: @timelyx
