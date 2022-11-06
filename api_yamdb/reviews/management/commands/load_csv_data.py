import datetime
from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User


def import_csv_data():
    start_time = datetime.datetime.now()

    csv_files = (
        (User, 'reviews/management/data/users.csv'),
        (Category, 'reviews/management/data/category.csv'),
        (Genre, 'reviews/management/data/genre.csv'),
        (Title, 'reviews/management/data/titles.csv'),
        (GenreTitle, 'reviews/management/data/genre_title.csv'),
        (Review, 'reviews/management/data/review.csv'),
        (Comment, 'reviews/management/data/comments.csv')
    )

    for model, file in csv_files:
        print(f"Загрузка данных таблицы {file} началась.")
        for row in DictReader(open(file, encoding='utf-8')):
            if file == 'reviews/management/data/users.csv':
                data = model(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )
                data.save()
            elif (file == 'reviews/management/data/category.csv'
                  or file == 'reviews/management/data/genre.csv'):
                data = model(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                data.save()
            elif file == 'reviews/management/data/titles.csv':
                data = model(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category_id']
                )
                data.save()
            elif file == 'reviews/management/data/genre_title.csv':
                data = model(
                    id=row['id'],
                    title_id=row['title_id'],
                    genre_id=row['genre_id']
                )
                data.save()
            elif file == 'reviews/management/data/review.csv':
                data = model(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author_id=row['author'],
                    score=row['score'],
                    pub_date=row['pub_date']
                )
                data.save()
            elif file == 'reviews/management/data/comments.csv':
                data = model(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author_id=row['author'],
                    pub_date=row['pub_date']
                )
                data.save()
        print(
            f"Загрузка данных таблицы {file} завершена успешно.")

    print(f"Загрузка данных завершена за"
          f" {(datetime.datetime.now() - start_time).total_seconds()} "
          f"сек.")


class Command(BaseCommand):
    help = ("Загрузка data из reviews/management/data/*.csv."
            "Запуск: python manage.py load_csv_data."
            "Подробнее об импорте в README.md.")

    def handle(self, *args, **options):
        print("Старт импорта")

        try:
            import_csv_data()

        except Exception as error:
            print(f"Сбой в работе импорта: {error}.")

        finally:
            print("Завершена работа импорта.")
