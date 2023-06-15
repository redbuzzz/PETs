# shared-music-play
> Привет! <br>
> Этот сервис позволит тебе смотреть видеоролики с платформы YoutTube синхронно с твоими друзьями, родственниками, или любыми людьми!
> <br><hr>
> Помимо публичных комнат, ты можешь создать приватную комнату где будут только твои друзья!<hr>Фишки:<br>• Админ / Модератор комнаты может менять порядок видео в плейлисте (всё синхронизируется!)<br>• Вы можете писать сообщения в общий чат<br>• Будучи админом или модератором вы можете банить пользователей!

Для работы с проектом нужно установить [python](http://python.org) и
[poetry](https://python-poetry.org/)
<br>
* Чтобы запустить бэкенд нужно войти в директорию shared-music-play
- docker-compose up - для поднятие БД в контейнере
- poetry shell - вход в виртуальное окружение
- poetry install - установка зависимостей
- python manage.py migrate - выполнить миграции
- python manage.py runserver - запуск сервера на http://127.0.0.1:8000/
- black . - ручной запуск линтера
- pre-commit install - установить pre commit hook
- pre-commit run -a - запуск линтеров вручную
<hr>

- Чтобы запустить фронт нужно перейти в папку frontend и выполнить соответствующие команды прописанные в readme
