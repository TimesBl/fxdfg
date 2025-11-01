"""
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
