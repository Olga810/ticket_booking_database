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


def delete_event(conn: psycopg.Connection, event_id: int):
    query = "DELETE FROM events WHERE id = %s;"
    with conn.cursor() as cur:
        cur.execute(query, (event_id,))
        conn.commit()


def add_event(conn: psycopg.Connection, name: str, event_date: str, description: str = None):
    query = """
        INSERT INTO events (name, event_date, description)
        VALUES (%s, %s, %s)
        RETURNING id;
    """
    with conn.cursor() as cur:
        cur.execute(query, (name, event_date, description))
        event_id = cur.fetchone()[0]
        conn.commit()
        return event_id


def find_events_by_seat(conn: psycopg.Connection, row_number: int, seat_number: int):
    query = """
        SELECT e.*
        FROM events e
        JOIN seats s ON t.seat_id = s.event_id
        WHERE s.row_number = %s AND s.seat_number = %s;
    """
    with conn.cursor() as cur:
        cur.execute(query, (row_number, seat_number))
        return cur.fetchall()


if __name__ == '__main__':
    load_dotenv()
    db_url = os.getenv('DATABASE_URL')

    print(search_events(db_url, title_part='Джазовый', venue_part='мал'))
  