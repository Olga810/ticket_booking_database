import os

import psycopg
from dotenv import load_dotenv


def main():
    load_dotenv()
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print('Укажите адрес базы данных')

    try:
        with psycopg.connect(db_url, connect_timeout=10) as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT current_database(), current_user')
                database_name, database_user = cursor.fetchone()

        print(f'Успешное подключение к БД {database_name} (пользователь: {database_user})')

    except psycopg.Error as e:
        print('Не удалось подключиться к БД. Подробности: ', e)
        
if __name__ == '__main__':
    main()