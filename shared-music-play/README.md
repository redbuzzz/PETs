# shared-music-play
Этот сервис позволяет просматривать совместные клипы на ютубе.
Реализован Чат(веб-сокеты), плейлисты, перемотка/паузка видео. 
Всё работает синхронно.

Для работы с проектом нужно установить [python](http://python.org) и
[poetry](https://python-poetry.org/)

- poetry shell - вход в виртуальное окружение
- poetry install - установка 
- python manage.py migrate - выполнить миграции
- python manage.py runserver - запуск сервера на http://127.0.0.1:8000/
- black . - ручной запуск линтера
- pre-commit install - установить pre commit hook
- pre-commit run -a - запуск линтеров вручную
