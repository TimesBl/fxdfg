"""
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
