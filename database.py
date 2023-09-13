import os

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy import create_engine
from datetime import datetime
load_dotenv()
# Создаем соединение с базой данных MySQL
engine = create_engine(f"mysql+mysqlconnector://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_NAME')}")


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
