"""
Альтернативный файл для запуска (для Gunicorn и др.)
"""
import sys
import os

# Добавляем путь к приложению
sys.path.insert(0, os.path.dirname(__file__))

from app import application

if __name__ == "__main__":
    application.run()
