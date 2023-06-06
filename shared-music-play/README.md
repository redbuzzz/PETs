# shared-music-play

Для работы с проектом нужно установить [python](http://python.org) и
[poetry](https://python-poetry.org/)

- poetry shell - вход в виртуальное окружение
- poetry install - установка 
- pip install -r requirements.txt - установка зависимостей
- python manage.py migrate - выполнить миграции
- python manage.py runserver - запуск сервера на http://127.0.0.1:8000/
- black . - ручной запуск линтера
- pre-commit install - установить pre commit hook
- pre-commit run -a - запуск линтеров вручную