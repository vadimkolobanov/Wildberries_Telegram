import asyncio
import os
import pandas as pd
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message
from config import dp, bot
from database import Base, User, session
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
        new_user = User(telegram_id=int(message.from_user.id), is_vip=False, free_requests=10)
        session.add(new_user)
        session.commit()
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
