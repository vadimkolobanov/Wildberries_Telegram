import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error
from sqlalchemy import Column, Integer, String, Boolean, DateTime, text, BigInteger, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import create_engine
from datetime import datetime

# Загрузка переменных окружения из файла .env
load_dotenv()

# Создаем соединение с базой данных MySQL
engine = create_engine(f"mysql+mysqlconnector://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_NAME')}")

# Создаем сессию для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Создаем базовый класс для описания моделей
Base = declarative_base()

class User(Base):
    """
    Модель данных для пользователей.

    Attributes:
        id (int): Уникальный идентификатор пользователя.
        telegram_id (BigInteger): Уникальный идентификатор Telegram пользователя.
        registration_date (DateTime): Дата и время регистрации пользователя.
        is_vip (int): Флаг VIP-статуса пользователя (0 - не VIP, 1 - VIP).
        vip_end_date (DateTime): Дата окончания VIP-статуса.
        free_requests (int): Количество бесплатных запросов пользователя.
        promocodes (relationship): Связь с таблицей промокодов, созданных пользователем.
        used_promocodes (relationship): Связь с таблицей промокодов, использованных пользователем.
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    registration_date = Column(DateTime, default=datetime.utcnow)
    is_vip = Column(Integer, default=0)
    vip_end_date = Column(DateTime, nullable=True)
    free_requests = Column(Integer, default=0)
    promocodes = relationship('PromoCode', back_populates='creator')
    used_promocodes = relationship('PromoCode', secondary='promocode_user', back_populates='used_by')

class PromoCode(Base):
    """
    Модель данных для промокодов.

    Attributes:
        id (int): Уникальный идентификатор промокода.
        code (str): Уникальный код промокода.
        creator_id (int): Идентификатор создателя промокода.
        creator (relationship): Связь с таблицей пользователей, создавших промокод.
        used_by (relationship): Связь с таблицей пользователей, использующих промокод.
    """

    __tablename__ = 'promocodes'

    id = Column(Integer, primary_key=True)
    code = Column(String(255), unique=True, nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    creator = relationship('User', back_populates='promocodes')
    used_by = relationship('User', secondary='promocode_user', back_populates='used_promocodes')

# Определите ассоциационную таблицу для связи пользователей и промокодов
promocode_user = Table('promocode_user', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('promocode_id', Integer, ForeignKey('promocodes.id'))
)

# Создаем таблицу в базе данных
Base.metadata.create_all(engine)
