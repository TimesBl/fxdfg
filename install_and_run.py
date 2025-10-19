"""
=============================================================================
TIMELYX PORTFOLIO - САЙТ-ВИЗИТКА
=============================================================================
Просто запустите: python portfolio_site.py

Автоматически:
✅ Установит Flask
✅ Создаст красивый темный сайт с фиолетовым дизайном
✅ Запустит локальный сервер
=============================================================================
"""

import os
import sys
import subprocess
import json
from datetime import datetime

print("=" * 70)
print("🚀 TIMELYX PORTFOLIO - АВТОЗАПУСК")
print("=" * 70)
print()

# =============================================================================
# УСТАНОВКА FLASK
# =============================================================================

def install_flask():
    """Установка Flask если нет"""
    try:
        import flask
        print("✅ Flask уже установлен")
        return True
    except ImportError:
        print("📦 Установка Flask...")
        try:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', 'flask', '-q'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("✅ Flask успешно установлен")
            return True
        except Exception as e:
            print(f"❌ Ошибка установки: {e}")
            print("   Установите вручную: pip install flask")
            return False

if not install_flask():
    input("\nНажмите Enter для выхода...")
    sys.exit(1)

from flask import Flask, jsonify, request

print()

# =============================================================================
# БАЗА ДАННЫХ (JSON)
# =============================================================================

class Database:
    """Простая база данных в JSON"""
    
    def __init__(self):
        os.makedirs('data', exist_ok=True)
        self.file = 'data/portfolio.json'
        self.data = self.load()
    
    def load(self):
        """Загрузка данных"""
        if os.path.exists(self.file):
            try:
                with open(self.file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # Данные по умолчанию
        return {
            'profile': {
                'name': 'timelyx',
                'title': 'Python Developer',
                'bio': 'азрабатываю Telegram-ботов на Python, постоянно изучаю новые технологии и совершенствую свои навыки.'
            },
            'projects': [
                {
                    'id': 1,
                    'name': 'Portfolio Website',
                    'description': 'Современный сайт-портфолио с темным дизайном',
                    'tech': ['Python', 'Flask', 'HTML/CSS', 'JavaScript'],
                    'link': ''
                },
                {
                    'id': 2,
                    'name': 'Telegram Bot',
                    'description': 'Бот для автоматизации бизнес-процессов',
                    'tech': ['Python', 'python-telegram-bot', 'SQLite'],
                    'link': ''
                }
            ],
            'stats': {
                'years': 2,
                'hours': 1500,
                'total_projects': 2,
                'successful_works': 2
            },
            'contacts': {
                'telegram': '@timelyx_help',
                'email': 'timesblake007@gmail.com',
                'blog': 'https://t.me/timelyx_blog'
            }
        }
    
    def save(self):
        """Сохранение данных"""
        with open(self.file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def add_project(self, name, description, tech, link=''):
        """Добавить проект"""
        project = {
            'id': len(self.data['projects']) + 1,
            'name': name,
            'description': description,
            'tech': tech,
            'link': link
        }
        self.data['projects'].append(project)
        self.data['stats']['total_projects'] = len(self.data['projects'])
        self.save()
        return project
    
    def update_profile(self, **kwargs):
        """Обновить профиль"""
        self.data['profile'].update(kwargs)
        self.save()
    
    def update_stats(self, **kwargs):
        """Обновить статистику"""
        self.data['stats'].update(kwargs)
        self.save()
    
    def get_all(self):
        """Получить все данные"""
        return self.data

db = Database()
print("✅ База данных готова")

# =============================================================================
# ВЕБ-ПРИЛОЖЕНИЕ
# =============================================================================

app = Flask(__name__)

# HTML Страница
HTML_PAGE = '''<!DOCTYPE html>
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
            background: #0a0a0f;
            color: #e0e0e0;
            overflow-x: hidden;
            position: relative;
        }

        /* Анимированный фон */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(ellipse at 20% 30%, rgba(138, 43, 226, 0.15) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 70%, rgba(75, 0, 130, 0.15) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(147, 51, 234, 0.1) 0%, transparent 50%);
            animation: backgroundMove 20s ease infinite;
            pointer-events: none;
            z-index: 0;
        }

        @keyframes backgroundMove {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.8; transform: scale(1.1); }
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 1;
        }

        /* Hero Section */
        .hero {
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            z-index: 1;
        }

        .hero:hover {
            transform: scale(1.02);
        }

        .hero h1 {
            font-size: 6rem;
            margin-bottom: 1rem;
            animation: fadeInDown 1s ease;
            background: linear-gradient(135deg, #9333ea, #a855f7, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 900;
            text-shadow: 0 0 80px rgba(147, 51, 234, 0.5);
        }

        .hero p {
            font-size: 2rem;
            animation: fadeInUp 1s ease 0.3s both;
            color: #c084fc;
            text-shadow: 0 0 20px rgba(192, 132, 252, 0.3);
        }

        .scroll-hint {
            position: absolute;
            bottom: 30px;
            animation: bounce 2s infinite;
            font-size: 2rem;
            color: #a855f7;
        }

        /* Main Content */
        .main-content {
            display: none;
            animation: fadeIn 0.5s ease;
            position: relative;
            z-index: 1;
        }

        .main-content.active {
            display: block;
        }

        .section {
            background: rgba(20, 20, 30, 0.7);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.5),
                inset 0 1px 0 rgba(147, 51, 234, 0.1),
                0 0 0 1px rgba(147, 51, 234, 0.1);
            border: 1px solid rgba(147, 51, 234, 0.2);
            transition: all 0.3s ease;
        }

        .section:hover {
            box-shadow: 
                0 12px 48px rgba(147, 51, 234, 0.2),
                inset 0 1px 0 rgba(147, 51, 234, 0.2),
                0 0 0 1px rgba(147, 51, 234, 0.2);
        }

        /* Profile Section */
        .profile {
            display: flex;
            align-items: center;
            gap: 30px;
            flex-wrap: wrap;
        }

        .avatar {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background: linear-gradient(135deg, #9333ea, #a855f7);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 4rem;
            font-weight: bold;
            box-shadow: 
                0 10px 40px rgba(147, 51, 234, 0.5),
                0 0 60px rgba(147, 51, 234, 0.3);
            position: relative;
            animation: glow 3s ease infinite;
        }

        @keyframes glow {
            0%, 100% { box-shadow: 0 10px 40px rgba(147, 51, 234, 0.5), 0 0 60px rgba(147, 51, 234, 0.3); }
            50% { box-shadow: 0 10px 50px rgba(147, 51, 234, 0.7), 0 0 80px rgba(147, 51, 234, 0.5); }
        }

        .profile-info h2 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            color: #c084fc;
        }

        .profile-info p {
            font-size: 1.2rem;
            color: #a0a0b0;
            line-height: 1.6;
        }

        /* Projects Section */
        .projects-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .project-card {
            background: rgba(30, 30, 45, 0.6);
            padding: 25px;
            border-radius: 15px;
            transition: all 0.3s ease;
            border: 2px solid rgba(147, 51, 234, 0.3);
            position: relative;
            overflow: hidden;
        }

        .project-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(147, 51, 234, 0.1), transparent);
            transition: left 0.5s ease;
        }

        .project-card:hover::before {
            left: 100%;
        }

        .project-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 40px rgba(147, 51, 234, 0.3);
            border-color: #9333ea;
        }

        .project-card h3 {
            margin-bottom: 10px;
            font-size: 1.5rem;
            color: #c084fc;
        }

        .project-card p {
            color: #a0a0b0;
            margin-bottom: 15px;
        }

        .tech-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 15px;
        }

        .tech-tag {
            background: rgba(147, 51, 234, 0.2);
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            color: #c084fc;
            border: 1px solid rgba(147, 51, 234, 0.3);
        }

        /* Stats Section */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .stat-card {
            background: rgba(30, 30, 45, 0.6);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            border: 1px solid rgba(147, 51, 234, 0.2);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .stat-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, #9333ea, #a855f7, #c084fc);
            transform: translateX(-100%);
            transition: transform 0.5s ease;
        }

        .stat-card:hover::after {
            transform: translateX(0);
        }

        .stat-card:hover {
            border-color: #9333ea;
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(147, 51, 234, 0.3);
        }

        .stat-number {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #9333ea, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .stat-label {
            font-size: 1rem;
            color: #a0a0b0;
        }

        /* Contact Section */
        .contact-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }

        .contact-btn {
            padding: 20px;
            background: rgba(147, 51, 234, 0.2);
            border: 2px solid rgba(147, 51, 234, 0.3);
            border-radius: 15px;
            color: #c084fc;
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            font-weight: 600;
        }

        .contact-btn:hover {
            background: rgba(147, 51, 234, 0.4);
            border-color: #9333ea;
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(147, 51, 234, 0.4);
            color: #e0e0e0;
        }

        /* Back Button */
        .back-btn {
            position: fixed;
            top: 20px;
            left: 20px;
            padding: 10px 20px;
            background: rgba(147, 51, 234, 0.2);
            border: 2px solid rgba(147, 51, 234, 0.3);
            border-radius: 10px;
            color: #c084fc;
            cursor: pointer;
            font-size: 1.1rem;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            z-index: 1000;
            font-weight: 600;
        }

        .back-btn:hover {
            background: rgba(147, 51, 234, 0.4);
            transform: translateX(-5px);
            border-color: #9333ea;
        }

        /* Animations */
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
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

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {
                transform: translateY(0);
            }
            40% {
                transform: translateY(-20px);
            }
            60% {
                transform: translateY(-10px);
            }
        }

        h2 {
            font-size: 2rem;
            margin-bottom: 20px;
            color: #c084fc;
            text-shadow: 0 0 20px rgba(192, 132, 252, 0.2);
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
        }

        ::-webkit-scrollbar-track {
            background: #0a0a0f;
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #9333ea, #a855f7);
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #a855f7, #c084fc);
        }

        /* Responsive */
        @media (max-width: 768px) {
            .hero h1 {
                font-size: 3rem;
            }
            .hero p {
                font-size: 1.5rem;
            }
            .avatar {
                width: 100px;
                height: 100px;
                font-size: 3rem;
            }
            .profile-info h2 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <!-- Hero Section -->
    <div class="hero" id="hero">
        <h1>Timelyx</h1>
        <p>Привет! 👋</p>
        <div class="scroll-hint">↓</div>
    </div>

    <!-- Main Content -->
    <div class="main-content" id="mainContent">
        <button class="back-btn" onclick="goBack()">← Назад</button>
        
        <div class="container">
            <!-- Profile Section -->
            <div class="section profile">
                <div class="avatar" id="avatar">T</div>
                <div class="profile-info">
                    <h2 id="profileName">timelyx</h2>
                    <p id="profileBio">Загрузка...</p>
                </div>
            </div>

            <!-- Projects Section -->
            <div class="section">
                <h2>💼 Мои проекты</h2>
                <div class="projects-grid" id="projectsGrid">
                    <p style="color: #666;">Загрузка проектов...</p>
                </div>
            </div>

            <!-- Stats Section -->
            <div class="section">
                <h2>📊 Моя статистика</h2>
                <div class="stats-grid" id="statsGrid">
                    <p style="color: #666;">Загрузка статистики...</p>
                </div>
            </div>

            <!-- Contact Section -->
            <div class="section">
                <h2>📞 Связаться со мной</h2>
                <div class="contact-grid" id="contactGrid">
                    <p style="color: #666;">Загрузка контактов...</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        let data = null;

        // Hero click handler
        document.getElementById('hero').addEventListener('click', function() {
            document.getElementById('hero').style.display = 'none';
            document.getElementById('mainContent').classList.add('active');
            loadData();
        });

        function goBack() {
            document.getElementById('mainContent').classList.remove('active');
            document.getElementById('hero').style.display = 'flex';
        }

        async function loadData() {
            try {
                const response = await fetch('/api/data');
                data = await response.json();
                renderPage();
            } catch (error) {
                console.error('Ошибка загрузки данных:', error);
            }
        }

        function renderPage() {
            if (!data) return;

            // Profile
            document.getElementById('profileName').textContent = data.profile.name;
            document.getElementById('profileBio').textContent = data.profile.bio;
            document.getElementById('avatar').textContent = data.profile.name[0].toUpperCase();

            // Projects
            const projectsHTML = data.projects.map(project => `
                <div class="project-card">
                    <h3>${project.name}</h3>
                    <p>${project.description}</p>
                    <div class="tech-tags">
                        ${project.tech.map(tech => `<span class="tech-tag">${tech}</span>`).join('')}
                    </div>
                    ${project.link ? `<p style="margin-top: 15px; color: #9333ea;">🔗 <a href="${project.link}" style="color: #a855f7;" target="_blank">Перейти</a></p>` : ''}
                </div>
            `).join('');
            document.getElementById('projectsGrid').innerHTML = projectsHTML;

            // Stats
            const statsHTML = `
                <div class="stat-card">
                    <div class="stat-number">${data.stats.years}</div>
                    <div class="stat-label">Лет программирования</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${data.stats.hours}+</div>
                    <div class="stat-label">Часов кодинга</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${data.stats.total_projects}</div>
                    <div class="stat-label">Проектов</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${data.stats.successful_works}</div>
                    <div class="stat-label">Успешных работ</div>
                </div>
            `;
            document.getElementById('statsGrid').innerHTML = statsHTML;

            // Contacts
            const contactsHTML = `
                <a href="https://t.me/${data.contacts.telegram.replace('@', '')}" class="contact-btn" target="_blank">
                    <span>📱</span>
                    <span>Telegram</span>
                </a>
                <a href="mailto:${data.contacts.email}" class="contact-btn">
                    <span>📧</span>
                    <span>Email</span>
                </a>
                <a href="https://${data.contacts.github}" class="contact-btn" target="_blank">
                    <span>💻</span>
                    <span>Blog</span>
                </a>
            `;
            document.getElementById('contactGrid').innerHTML = contactsHTML;
        }
    </script>
</body>
</html>'''

@app.route('/')
def index():
    """Главная страница"""
    return HTML_PAGE

@app.route('/api/data')
def get_data():
    """API: получить все данные"""
    return jsonify(db.get_all())

@app.route('/api/project/add', methods=['POST'])
def add_project():
    """API: добавить проект"""
    data = request.json
    project = db.add_project(
        name=data.get('name'),
        description=data.get('description'),
        tech=data.get('tech', []),
        link=data.get('link', '')
    )
    return jsonify(project)

# =============================================================================
# ЗАПУСК
# =============================================================================

if __name__ == '__main__':
    print()
    print("=" * 70)
    print("✅ ВСЁ ГОТОВО!")
    print("=" * 70)
    print()
    print("🌐 Сайт запускается на: http://localhost:5000")
    print()
    print("💡 Редактирование:")
    print("   • Откройте data/portfolio.json для изменения содержимого")
    print("   • Перезагрузите страницу в браузере для просмотра изменений")
    print()
    print("⌨️  Нажмите Ctrl+C для остановки сервера")
    print("=" * 70)
    print()
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("👋 СЕРВЕР ОСТАНОВЛЕН")
        print("=" * 70)
        print()