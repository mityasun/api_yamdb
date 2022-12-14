![Test and push to Docker Hub](https://github.com/mityasun/api_yamdb/actions/workflows/yamdb_workflow.yml/badge.svg)
## Проект API Yamdb - api для сайта с отзывами на кино, книги и музыку.

***Здесь вы можете создавать оставлять отзывы и рейтинг на произведения, а также комментировать отзывы.***

Этот репозиторий содержит урезанную версию проекта: в составе готовое API для взаимодействия с проектом.
<br>
### Возможности API:
- Регистрация пользователей и токен авторизации (Simple JWT).
- Получение, создание, обновление, удаление учетных записей.
- Получение, создание, обновление, удаление произведений.
- Получение, создание, удаление категорий произведений и их жанров.
- Получение, создание, обновление, удаление отзывов и комментариев.

Подробней [по ссылке](http://127.0.0.1:8000/api/v1/redoc/)<br>
<sub>Ссылка откроется после развертывания проекта.</sub>
<br>
### Технологии
![Python](https://img.shields.io/badge/Python-3.9.8-%23254F72?style=for-the-badge&logo=python&logoColor=yellow&labelColor=254f72)
![Django](https://img.shields.io/badge/Django-2.2.28-0C4B33?style=for-the-badge&logo=django&logoColor=white&labelColor=0C4B33)
![Django](https://img.shields.io/badge/Django%20REST-3.12.4-802D2D?style=for-the-badge&logo=django&logoColor=white&labelColor=802D2D)


### Как запустить проект:

Клонировать репозиторий и перейти в него в терминале:

```
git clone https://github.com/mityasun/api_yamdb.git
```

Перейдите в директорию с настройками Docker-compose:

```
cd api_yamdb/infra/
```

Создать файл .env в этой директории пропишите в нем:

```
SECRET_KEY=*Секретный ключ Django*
DEBUG=*False для прода и True для тестов*
ALLOWED_HOSTS=*Список разрешенных хостов*
DB_NAME=*Имя БД*
POSTGRES_USER=*Имя пользователя БД*
POSTGRES_PASSWORD=*Пароль пользователя БД*
DB_HOST=db
DB_PORT=5432
```

Запустите Docker-compose:
```
docker-compose up -d --build
```

Примените миграции:

```
docker-compose exec web python manage.py migrate
```

Соберите статику:

```
docker-compose exec web python manage.py collectstatic --no-input
```

Заполнить базу данными из копии::

```
docker-compose exec web python manage.py loaddata fixtures.json
```

Создайте суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

<br>

### Импорт данных из csv для наполнения базы:

В терминале наберите команду:

```
docker exec -it yamdb_web bash
```

Запустите команду импорта:

```
python manage.py load_csv_data
```

В терминале отобразится результат импорта.<br>
Если какой-либо из файлов отсутствует, то он не будет импортирован.

Примеры файлов csv для наполнения базы находятся в папке reviews/management/data/*.csv:
- users.csv - файл для заполнения таблицы пользователей
- titles.csv - файл для заполнения таблицы произведений.
- category.csv - файл для заполнения таблицы категорий произведений.
- genre.csv - файл для заполнения таблицы жанров произведений.
- genre_title.csv - файл для заполнения таблицы Many-to-Many: одно произведение может иметь несколько жанров.
- review.csv - файл для заполнения таблицы отзывов к произведениям.
- comments.csv - файл для заполнения таблицы комментариев к отзывам.
<br>

Авторы проекта:
<br>
Auth/Users: Петухов Артем [Github](https://github.com/mityasun)<br>
Titles/Category/Genre: Клименкова Мария [Github](https://github.com/mawuta-super-hack)<br>
Reviews/Comments: Хужина Лилия [Github](https://github.com/iamliliya)<br>
