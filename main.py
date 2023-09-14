import asyncio
import os
import pandas as pd
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message
from config import dp, bot
from database import Base, User, session, execute_sql_query
from keyboards import *
from FSM_activity import *
from callbacks import *


async def _send_inline_keyboard(message, text, keyboard):
    """
    Отправляет сообщение с встроенной клавиатурой.

    Args:
        message: Объект сообщения, куда будет отправлено сообщение.
        text (str): Текст сообщения.
        keyboard: Встроенная клавиатура.

    Returns:
        None

    Пример использования:
        Отправка сообщения с встроенной клавиатурой.
    """
    await message.answer(text, reply_markup=keyboard)


@dp.message(Command('start'))
async def start(message: types.Message):
    """
    Обрабатывает команду /start и создает нового пользователя.

    Args:
        message (types.Message): Объект сообщения.

    Returns:
        None

    Пример использования:
        Пользователь отправляет команду /start, и эта функция создает нового пользователя и отправляет приветственное сообщение.
    """
    try:
        insert_user_query = "INSERT INTO your_app_name_telegramuser (telegram_id, is_vip, vip_end_date, free_requests) VALUES (%s, %s, %s, %s);"

        # Параметры для SQL-запроса
        user_params = (123456789, False, None, 0)

        # Выполнение SQL-запроса с параметрами
        result = execute_sql_query(insert_user_query, user_params)

        # Проверка результата
        if result is not None:
            print("Пользователь успешно добавлен.")
        else:
            print("Произошла ошибка при добавлении пользователя.")
    except Exception as e:
        pass
    await _send_inline_keyboard(message, "Добро пожаловать! Для начала парсинга нажмите кнопку ниже.", keyboard_main())


async def main():
    """
    Запускает бота.

    Returns:
        None

    Пример использования:
        Запуск бота с помощью asyncio.run(main()).
    """
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
