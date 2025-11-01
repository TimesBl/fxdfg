"""
Timelyx Portfolio System - ВЕРСИЯ ДЛЯ ХОСТИНГА
Создает все файлы для деплоя на хостинг
"""
import os
import json
import time
from pathlib import Path

# ==================== FLASK APP (для хостинга) ====================
FLASK_APP_CODE = '''"""
Flask приложение для хостинга
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime
from pathlib import Path
import time
import os

# Создаем приложение
app = Flask(__name__)

# CORS - разрешаем доступ с вашего домена
# Замените на свой домен после размещения на хостинге
ALLOWED_ORIGINS = [
    'http://localhost:5000',
    'http://127.0.0.1:5000',
    'https://yourdomain.com',  # ЗАМЕНИТЕ НА ВАШ ДОМЕН
]

CORS(app, origins=ALLOWED_ORIGINS)

REVIEWS_FILE = 'reviews.json'

def load_reviews():
    """Загрузка отзывов из файла"""
    try:
        if Path(REVIEWS_FILE).exists():
            with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Ошибка загрузки отзывов: {e}")
        return []

def save_reviews(reviews):
    """Сохранение отзывов в файл"""
    try:
        with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
            json.dump(reviews, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка сохранения отзывов: {e}")
        return False

@app.route('/')
def index():
    return jsonify({
        "status": "running",
        "message": "Timelyx Portfolio API работает",
        "endpoints": {
            "reviews": "/api/reviews"
        }
    })

@app.route('/api/reviews', methods=['GET', 'POST'])
def handle_reviews():
    """Обработка запросов отзывов"""
    if request.method == 'GET':
        reviews = load_reviews()
        return jsonify(reviews)
    
    elif request.method == 'POST':
        try:
            review_data = request.json
            
            # Генерируем ID если его нет
            if 'id' not in review_data:
                review_data['id'] = time.time()
            
            # Добавляем дату если её нет
            if 'date' not in review_data:
                review_data['date'] = datetime.now().isoformat()
            
            # Загружаем существующие отзывы
            reviews = load_reviews()
            
            # Добавляем новый отзыв в начало списка
            reviews.insert(0, review_data)
            
            # Сохраняем
            if save_reviews(reviews):
                return jsonify({"success": True, "message": "Отзыв добавлен"}), 200
            else:
                return jsonify({"success": False, "message": "Ошибка сохранения"}), 500
                
        except Exception as e:
            print(f"Ошибка обработки отзыва: {e}")
            return jsonify({"success": False, "message": str(e)}), 400

# Для локального запуска
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

# Для хостинга (passenger_wsgi.py будет импортировать application)
application = app
'''

# ==================== PASSENGER_WSGI.PY (для большинства хостингов) ====================
PASSENGER_WSGI = '''"""
Файл для запуска на хостинге через Passenger (Beget, Timeweb, Reg.ru и др.)
"""
import sys
import os

# ВАЖНО: Замените путь на ваш путь к виртуальному окружению на хостинге
# Например: /home/u1234567/venv/lib/python3.9/site-packages
VENV_PATH = os.path.expanduser('~/venv/lib/python3.9/site-packages')
if os.path.exists(VENV_PATH):
    sys.path.insert(0, VENV_PATH)

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(__file__))

# Импортируем приложение
from app import application

# Для некоторых хостингов
if __name__ == '__main__':
    application.run()
'''

# ==================== WSGI.PY (альтернатива для других хостингов) ====================
WSGI_PY = '''"""
Альтернативный файл для запуска (для Gunicorn и др.)
"""
import sys
import os

# Добавляем путь к приложению
sys.path.insert(0, os.path.dirname(__file__))

from app import application

if __name__ == "__main__":
    application.run()
'''

# ==================== REQUIREMENTS.TXT ====================
REQUIREMENTS = '''Flask==3.0.0
Flask-CORS==4.0.0
Werkzeug==3.0.1
waitress==2.1.2
gunicorn==21.2.0
'''

# ==================== .HTACCESS (для Apache хостингов) ====================
HTACCESS = '''# Настройки для Flask на Apache хостинге
PassengerEnabled On
PassengerAppRoot /home/USERNAME/DOMAIN.COM/
PassengerPython /home/USERNAME/venv/bin/python3

# Замените USERNAME на ваш логин хостинга
# Замените DOMAIN.COM на ваш домен
# Замените путь к Python на путь к вашему виртуальному окружению

# Дополнительные настройки
RewriteEngine On
RewriteBase /
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ passenger_wsgi.py/$1 [L]
'''

# ==================== INDEX.HTML (для хостинга) ====================
INDEX_HTML = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Timelyx - Python Developer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a0033 0%, #2d0052 50%, #1a0033 100%);
            color: #e0d4f7;
            min-height: 100vh;
            overflow-x: hidden;
        }

        .stars {
            position: fixed;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
        }

        .star {
            position: absolute;
            width: 2px;
            height: 2px;
            background: #fff;
            border-radius: 50%;
            animation: twinkle 3s infinite;
        }

        @keyframes twinkle {
            0%, 100% { opacity: 0.3; }
            50% { opacity: 1; }
        }

        .welcome-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #1a0033 0%, #2d0052 100%);
            z-index: 1000;
            transition: opacity 0.5s, visibility 0.5s;
        }

        .welcome-screen.hidden {
            opacity: 0;
            visibility: hidden;
        }

        .welcome-title {
            font-size: 4rem;
            font-weight: bold;
            background: linear-gradient(45deg, #b794f6, #e879f9, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 2rem;
            animation: fadeInUp 1s ease-out;
        }

        .welcome-subtitle {
            font-size: 1.5rem;
            color: #c4b5fd;
            cursor: pointer;
            padding: 1rem 2rem;
            border: 2px solid #a78bfa;
            border-radius: 10px;
            transition: all 0.3s;
            animation: fadeInUp 1s ease-out 0.3s both;
        }

        .welcome-subtitle:hover {
            background: #a78bfa;
            color: #1a0033;
            transform: scale(1.05);
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            opacity: 0;
            transition: opacity 0.5s;
            position: relative;
            z-index: 1;
        }

        .container.visible {
            opacity: 1;
        }

        header {
            text-align: center;
            padding: 3rem 0;
        }

        .avatar {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            border: 4px solid #a78bfa;
            margin: 0 auto 1.5rem;
            display: block;
            box-shadow: 0 0 30px rgba(167, 139, 250, 0.5);
            animation: float 3s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }

        h1 {
            font-size: 3rem;
            background: linear-gradient(45deg, #b794f6, #e879f9);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
        }

        .subtitle {
            font-size: 1.2rem;
            color: #c4b5fd;
            margin-bottom: 1rem;
        }

        .bio {
            background: rgba(167, 139, 250, 0.1);
            border: 1px solid rgba(167, 139, 250, 0.3);
            border-radius: 15px;
            padding: 2rem;
            margin: 2rem 0;
            backdrop-filter: blur(10px);
        }

        .section {
            margin: 3rem 0;
        }

        h2 {
            font-size: 2rem;
            color: #a78bfa;
            margin-bottom: 1.5rem;
            text-align: center;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }

        .stat-card {
            background: rgba(167, 139, 250, 0.15);
            border: 1px solid rgba(167, 139, 250, 0.3);
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(167, 139, 250, 0.3);
        }

        .stat-number {
            font-size: 2.5rem;
            font-weight: bold;
            color: #e879f9;
            display: block;
            margin-bottom: 0.5rem;
        }

        .stat-label {
            color: #c4b5fd;
            font-size: 0.9rem;
        }

        .projects-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }

        .project-card {
            background: rgba(167, 139, 250, 0.1);
            border: 1px solid rgba(167, 139, 250, 0.3);
            border-radius: 15px;
            padding: 1.5rem;
            transition: all 0.3s;
        }

        .project-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(167, 139, 250, 0.3);
            border-color: #a78bfa;
        }

        .project-title {
            font-size: 1.3rem;
            color: #e879f9;
            margin-bottom: 0.5rem;
        }

        .project-desc {
            color: #c4b5fd;
            line-height: 1.6;
        }

        .contact-section {
            display: flex;
            justify-content: center;
            gap: 2rem;
            flex-wrap: wrap;
        }

        .contact-btn {
            background: rgba(167, 139, 250, 0.2);
            border: 2px solid #a78bfa;
            color: #e0d4f7;
            padding: 1rem 2rem;
            border-radius: 10px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.3s;
            font-size: 1rem;
        }

        .contact-btn:hover {
            background: #a78bfa;
            color: #1a0033;
            transform: translateY(-3px);
        }

        .reviews-container {
            max-width: 800px;
            margin: 0 auto;
        }

        .review-card {
            background: rgba(167, 139, 250, 0.1);
            border: 1px solid rgba(167, 139, 250, 0.3);
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: all 0.3s;
            animation: slideIn 0.5s ease-out;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .review-card:hover {
            box-shadow: 0 5px 20px rgba(167, 139, 250, 0.2);
        }

        .review-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }

        .review-author {
            font-weight: bold;
            color: #e879f9;
        }

        .review-rating {
            color: #fbbf24;
        }

        .review-text {
            color: #c4b5fd;
            line-height: 1.6;
        }

        .review-date {
            color: #9ca3af;
            font-size: 0.85rem;
            margin-top: 0.5rem;
        }

        .loading {
            text-align: center;
            color: #9ca3af;
            padding: 2rem;
        }

        footer {
            text-align: center;
            padding: 2rem;
            color: #9ca3af;
            border-top: 1px solid rgba(167, 139, 250, 0.2);
            margin-top: 4rem;
        }

        .status-indicator {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 0.5rem 1rem;
            background: rgba(167, 139, 250, 0.2);
            border: 1px solid #a78bfa;
            border-radius: 8px;
            font-size: 0.9rem;
            z-index: 100;
        }

        .status-online {
            border-color: #10b981;
            color: #10b981;
        }

        .status-offline {
            border-color: #ef4444;
            color: #ef4444;
        }

        @media (max-width: 768px) {
            .welcome-title { font-size: 2.5rem; }
            h1 { font-size: 2rem; }
            .stats-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="stars" id="stars"></div>
    <div class="status-indicator" id="statusIndicator">⚪ Загрузка...</div>

    <div class="welcome-screen" id="welcomeScreen">
        <h1 class="welcome-title">Timelyx</h1>
        <div class="welcome-subtitle" onclick="enterSite()">Привет! 👋</div>
    </div>

    <div class="container" id="mainContent">
        <header>
            <img src="https://i.pinimg.com/736x/15/16/25/151625c23e69e4f9ef351a4c749e0dff.jpg" alt="Timelyx Avatar" class="avatar">
            <h1>Timelyx</h1>
            <p class="subtitle">Python Developer</p>
        </header>

        <section class="bio">
            <h2>Обо мне</h2>
            <p style="text-align: center; line-height: 1.8;">
                Привет! Я Timelyx - Разрабатываю Telegram-ботов на Python, постоянно изучаю новые технологии и совершенствую свои навыки программирования.
            </p>
        </section>

        <section class="section">
            <h2>Моя Статистика</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-number">3</span>
                    <span class="stat-label">Лет программирования</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">12</span>
                    <span class="stat-label">Проектов</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">2500+</span>
                    <span class="stat-label">Часов кодинга</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">25</span>
                    <span class="stat-label">Успешных работ</span>
                </div>
            </div>
        </section>

        <section class="section">
            <h2>Мои Проекты</h2>
            <div class="projects-grid">
                <div class="project-card">
                    <div class="project-title">💻 My business card</div>
                    <p class="project-desc">Мой сайт визитка для ознакомления с моей деятельностью.</p>
                </div>
                <div class="project-card">
                    <div class="project-title">📊 Telegram bot reviews</div>
                    <p class="project-desc">Бот предназначенный для ваших отзывов о моей работе.</p>
                </div>
                <div class="project-card">
                    <div class="project-title">🌐 Bot Editor mp3</div>
                    <p class="project-desc">Упрощает редактирование mp3 файлов для вас</p>
                </div>
            </div>
        </section>

        <section class="section">
            <h2>Связаться со мной</h2>
            <div class="contact-section">
                <a href="https://t.me/timelyx" class="contact-btn" target="_blank">📱 Telegram</a>
                <a href="https://github.com/timelyx" class="contact-btn" target="_blank">💻 GitHub</a>
                <a href="mailto:timelyx@example.com" class="contact-btn">✉️ Email</a>
            </div>
        </section>

        <section class="section">
            <h2>Отзывы</h2>
            <div class="reviews-container" id="reviewsContainer">
                <div class="loading">⏳ Загрузка отзывов...</div>
            </div>
        </section>

        <footer>
            <p>&copy; 2025 Timelyx. Все права защищены.</p>
        </footer>
    </div>

    <script>
        // ВАЖНО: Замените на URL вашего хостинга
        const API_URL = window.location.origin + '/api/reviews';
        
        let serverOnline = false;

        function createStars() {
            const starsContainer = document.getElementById('stars');
            for (let i = 0; i < 100; i++) {
                const star = document.createElement('div');
                star.className = 'star';
                star.style.left = Math.random() * 100 + '%';
                star.style.top = Math.random() * 100 + '%';
                star.style.animationDelay = Math.random() * 3 + 's';
                starsContainer.appendChild(star);
            }
        }

        function enterSite() {
            document.getElementById('welcomeScreen').classList.add('hidden');
            document.getElementById('mainContent').classList.add('visible');
        }

        function updateStatus(online) {
            const indicator = document.getElementById('statusIndicator');
            serverOnline = online;
            if (online) {
                indicator.textContent = '🟢 Сервер онлайн';
                indicator.className = 'status-indicator status-online';
            } else {
                indicator.textContent = '🔴 Оффлайн режим';
                indicator.className = 'status-indicator status-offline';
            }
        }

        function displayReviews(reviews) {
            const container = document.getElementById('reviewsContainer');
            container.innerHTML = '';
            
            if (!reviews || reviews.length === 0) {
                container.innerHTML = '<p style="text-align: center; color: #9ca3af;">Отзывов пока нет. Станьте первым!</p>';
                return;
            }
            
            reviews.forEach((review, index) => {
                const stars = '⭐'.repeat(review.rating || 5);
                const reviewCard = document.createElement('div');
                reviewCard.className = 'review-card';
                reviewCard.style.animationDelay = (index * 0.1) + 's';
                
                const date = review.date ? new Date(review.date).toLocaleDateString('ru-RU', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                }) : 'Недавно';
                
                reviewCard.innerHTML = `
                    <div class="review-header">
                        <span class="review-author">${review.author || 'Аноним'}</span>
                        <span class="review-rating">${stars}</span>
                    </div>
                    <p class="review-text">${review.text || ''}</p>
                    <p class="review-date">${date}</p>
                `;
                container.appendChild(reviewCard);
            });
        }

        async function loadReviews() {
            try {
                const response = await fetch(API_URL, {
                    method: 'GET',
                    headers: {'Content-Type': 'application/json'},
                    signal: AbortSignal.timeout(5000)
                });
                
                if (response.ok) {
                    const reviews = await response.json();
                    displayReviews(reviews);
                    updateStatus(true);
                    console.log('✅ Отзывы загружены с сервера');
                    return;
                }
            } catch (error) {
                console.log('ℹ️ Сервер недоступен');
                updateStatus(false);
            }
            
            displayReviews([]);
        }

        // Инициализация
        createStars();
        loadReviews();
        
        // Автообновление каждые 30 секунд
        setInterval(loadReviews, 30000);

        // Автовход через 3 секунды
        setTimeout(() => {
            if (!document.getElementById('mainContent').classList.contains('visible')) {
                enterSite();
            }
        }, 3000);
    </script>
</body>
</html>'''

# ==================== README для деплоя ====================
README = '''# Timelyx Portfolio System - Инструкция по развертыванию на хостинге

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
'''

# ==================== ИНИЦИАЛИЗАЦИЯ ====================
INITIAL_REVIEWS = [
    {
        "id": time.time(),
        "author": "timelyx",
        "rating": 5,
        "text": "Система работает отлично! Все настроено и готово к использованию.",
        "date": "2025-11-01T12:00:00.000000",
        "telegram_id": 6508828318
    },
    {
        "id": time.time() - 86400,
        "author": "Тестовый пользователь",
        "rating": 5,
        "text": "Красивый дизайн и удобный интерфейс!",
        "date": "2025-10-31T10:30:00.000000",
        "telegram_id": None
    }
]


def create_file(filename, content, description):
    """Создание файла"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {description}")
        return True
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


def create_json_file(filename, data, description):
    """Создание JSON файла"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ {description}")
        return True
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


def main():
    print("\n" + "="*70)
    print("🌐 TIMELYX PORTFOLIO - ГЕНЕРАТОР ДЛЯ ХОСТИНГА")
    print("="*70 + "\n")
    
    print("📦 Создание файлов для размещения на хостинге...\n")
    
    files = {
        'app.py': (FLASK_APP_CODE, "Создан app.py (Flask приложение)"),
        'passenger_wsgi.py': (PASSENGER_WSGI, "Создан passenger_wsgi.py (для Passenger)"),
        'wsgi.py': (WSGI_PY, "Создан wsgi.py (для Gunicorn)"),
        'requirements.txt': (REQUIREMENTS, "Создан requirements.txt (зависимости)"),
        '.htaccess': (HTACCESS, "Создан .htaccess (конфигурация Apache)"),
        'index.html': (INDEX_HTML, "Создан index.html (веб-интерфейс)"),
        'README.txt': (README, "Создан README.txt (инструкция)")
    }
    
    created = 0
    for filename, (content, description) in files.items():
        if create_file(filename, content, description):
            created += 1
    
    if create_json_file('reviews.json', INITIAL_REVIEWS, "Создан reviews.json (данные отзывов)"):
        created += 1
    
    print(f"\n✅ Создано файлов: {created}/{len(files) + 1}\n")
    
    print("="*70)
    print("🎉 ВСЁ ГОТОВО К ЗАГРУЗКЕ НА ХОСТИНГ!")
    print("="*70)
    print("\n📋 ЧТО НУЖНО СДЕЛАТЬ ДАЛЬШЕ:\n")
    print("1️⃣  Загрузите все файлы на хостинг через FTP/панель управления")
    print("2️⃣  Создайте виртуальное окружение (если требуется)")
    print("3️⃣  Установите зависимости: pip install -r requirements.txt")
    print("4️⃣  Настройте файлы (см. README.txt):")
    print("    • passenger_wsgi.py - путь к venv")
    print("    • .htaccess - USERNAME и DOMAIN.COM")
    print("    • app.py - ваш домен в ALLOWED_ORIGINS")
    print("5️⃣  Установите права на файлы")
    print("6️⃣  Откройте ваш сайт в браузере!\n")
    
    print("📚 Подробная инструкция в файле: README.txt\n")
    
    print("="*70)
    print("🌟 РЕКОМЕНДУЕМЫЕ ХОСТИНГИ:")
    print("="*70)
    print("• PythonAnywhere.com - БЕСПЛАТНО (100k запросов/день)")
    print("• Beget.com - от 150₽/мес (популярный в РФ)")
    print("• Timeweb.com - от 190₽/мес (хорошая поддержка)")
    print("• Reg.ru - от 200₽/мес")
    print("• Heroku.com - БЕСПЛАТНО (с ограничениями)")
    print("="*70 + "\n")
    
    print("💡 СОВЕТ: Начните с PythonAnywhere (бесплатно и просто!)\n")
    print("📞 Поддержка: @timelyx в Telegram\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Прервано пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")