import os

from dotenv import load_dotenv

from sqlite_to_postgres.models import (
    FilmWork,
    Genre,
    GenreFilmWork,
    Person,
    PersonFilmWork,
)

load_dotenv()

SQLITE_DB_PATH = os.getenv('SQLITE_DB_PATH')

POSTGRES_DB_DSN = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT'),
    'options': '-c search_path=content'
}

BATCH_SIZE = int(os.getenv('BATCH_SIZE', 100))


MAPPING_TABLE = {
    'genre': Genre,
    'film_work': FilmWork,
    'person': Person,
    'person_film_work': PersonFilmWork,
    'genre_film_work': GenreFilmWork,
}
