import mysql.connector
from mysql.connector import Error
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy import create_engine
from datetime import datetime

# Создаем соединение с базой данных MySQL


    if connection.is_connected():
        print('Connected to MySQL database')

except Error as e:
    print(f"Error: {e}")

# Создаем сессию для работы с базой данных

Session = sessionmaker(bind=engine)
session = Session()

# Создаем базовый класс для описания моделей
Base = declarative_base()


# Определяем модель пользователя
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    registration_date = Column(DateTime, default=datetime.utcnow)
    is_vip = Column(Boolean, default=False)
    vip_end_date = Column(DateTime, nullable=True)
    free_requests = Column(Integer, default=0)


# Создаем таблицу в базе данных
Base.metadata.create_all(engine)

# Пример добавления нового пользователя
new_user = User(telegram_id=123456, is_vip=False, free_requests=10)
session.add(new_user)
session.commit()

# Пример извлечения данных о пользователе
user = session.query(User).filter_by(telegram_id=123456).first()
if user:
    print(f"User {user.telegram_id}: VIP - {user.is_vip}, Free Requests - {user.free_requests}")
else:
    print("User not found.")

# Закрываем соединение с MySQL
if connection.is_connected():
    connection.close()
    print('Connection closed')
