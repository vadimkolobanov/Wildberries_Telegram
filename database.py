import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()
# Параметры подключения к базе данных
db_params = {
    "database": os.getenv('DATABASE_NAME'),
    "user": os.getenv('DATABASE_USER'),
    "password": os.getenv('DATABASE_PASSWORD'),
    "host": os.getenv('DATABASE_HOST'),
    "port": "5432",
}

# Функция для установления подключения к базе данных
def get_db_connection():
    try:
        connection = psycopg2.connect(**db_params)
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при подключении к PostgreSQL:", error)
        return None

# Функция для закрытия подключения к базе данных
def close_db_connection(connection):
    if connection:
        connection.close()

def execute_sql_query(query, params=None):
    connection = get_db_connection()
    if not connection:
        return None

    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        connection.commit()
        return result
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при выполнении SQL-запроса:", error)
        return None
    finally:
        close_db_connection(connection)