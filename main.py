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
    await message.answer(text, reply_markup=keyboard)


@dp.message(Command('start'))
async def start(message: types.Message):
    try:
        new_user = User(telegram_id=message.from_user.id, is_vip=False, free_requests=10)
        session.add(new_user)
        session.commit()
    except Exception:
        pass
    await _send_inline_keyboard(message, "Добро пожаловать! Для начала парсинга нажмите кнопку ниже.", keyboard_main())







async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
