import os

from dotenv import load_dotenv
from psycopg.rows import dict_row
import psycopg


def list_events(database_url: str) -> list[dict]:
    with psycopg.connect(database_url, row_factory=dict_row) as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT id, title, venue, starts_at FROM events ORDER BY id')
            return cursor.fetchall()


def search_events(database_url: str, title_part: str = "", venue_part: str = "") -> list[dict]:
    with psycopg.connect(database_url, row_factory=dict_row) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT id, title, venue, starts_at FROM events '
                'WHERE title ILIKE %s AND venue ILIKE %s ORDER BY starts_at, id',
                (f'%{title_part}%', f'%{venue_part}%'),
            )
            return cursor.fetchall()


if __name__ == '__main__':
    load_dotenv()
    db_url = os.getenv('DATABASE_URL')

    print(search_events(db_url, title_part='Джазовый', venue_part='мал'))