import os
from pathlib import Path

from dotenv import load_dotenv
import psycopg


def execute_sql_code(database_url: str, sql_file_name: str) -> None:
    schema_path = Path(__file__).resolve().parent / 'sql' / sql_file_name
    schema_sql = schema_path.read_text(encoding='utf-8')

    with psycopg.connect(database_url, connect_timeout=10) as connection:
        with connection.cursor() as cursor:
            cursor.execute(schema_sql)


if __name__ == '__main__':
    load_dotenv()
    db_url = os.getenv('DATABASE_URL')

    execute_sql_code(db_url, 'seed.sql')