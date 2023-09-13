import asyncio
import os

import mysql
import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile
from dotenv import load_dotenv
from sqlalchemy import create_engine
from mysql.connector import Error
from database import Base, User, session
from keyboards import *

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()




# Пример добавления нового пользователя

async def send_inline_keyboard(message, text, keyboard):
    await message.answer(text, reply_markup=keyboard)


class Form(StatesGroup):
    waiting_for_url = State()  # Ожидание ввода ссылки
    waiting_for_min_price = State()  # Ожидание ввода минимальной цены
    waiting_for_max_price = State()  # Ожидание ввода максимальной цены
    waiting_for_discount = State()  # Ожидание ввода скидки


@dp.message(Command('start'))
async def start(message: types.Message):
    try:
        new_user = User(telegram_id=message.from_user.id, is_vip=False, free_requests=10)
        session.add(new_user)
        session.commit()
    except Exception:
        pass
    await send_inline_keyboard(message, "Добро пожаловать! Для начала парсинга нажмите кнопку ниже.", keyboard_main())


async def send_data_to_telegram(data: list, filename, chat_id: int):
    df = pd.DataFrame(data)
    file_path = f'{filename}.xlsx'
    df.to_excel(file_path, index=False)

    await bot.send_document(chat_id, FSInputFile(file_path))

    os.remove(file_path)


@dp.message(Command('parse'))
async def parse(message: types.Message):
    pass
    # try:
    #     args = message.text.split()
    #     if len(args) != 5:
    #         await message.reply(
    #             "Неверный формат команды. Используйте: /parse ссылка минимальная_цена максимальная_цена скидка")
    #         return
    #
    #     url = args[1]
    #     low_price = int(args[2])
    #     top_price = int(args[3])
    #     discount = int(args[4])
    #     catalog_data = get_data_category(get_catalogs_wb())
    #     category = search_category_in_catalog(url=url, catalog_list=catalog_data)
    #     data_list = []
    #
    #     for page in range(1, 51):
    #         data = scrap_page(
    #             page=page,
    #             shard=category['shard'],
    #             query=category['query'],
    #             low_price=low_price,
    #             top_price=top_price,
    #             discount=discount)
    #         if len(get_data_from_json(data)) > 0:
    #             data_list.extend(get_data_from_json(data))
    #         else:
    #             break
    #     filename = f'{category["name"]}_from_{low_price}_to_{top_price}'
    #     save_excel(data_list, filename)
    #
    #     await send_data_to_telegram(data_list, filename, message.chat.id)
    #     await message.reply(
    #         f'Ссылка для проверки: {url}?priceU={low_price * 100};{top_price * 100}&discount={discount}')
    # except TypeError as e:
    #     await message.reply(str(e))
    # except PermissionError:
    #     await message.reply('Ошибка! Вы забыли закрыть созданный ранее excel файл. Закройте и повторите попытку')


@dp.callback_query(lambda c: c.data == 'start_parsing')
async def process_start_parsing(callback_query: types.CallbackQuery):
    await callback_query.answer("Начинаем парсинг!")
    # Добавьте ваш код для начала парсинга здесь

@dp.callback_query(lambda c: c.data == 'products')
async def buy_products_menu(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Здравствуйте! Мы рады предложить вам подписку на полную версию нашего бота.'
                                                        ' Полная версия включает в себя разнообразный дополнительный функционал и неограниченное количество запросов.'
                                                        ' Это отличная возможность получить максимум от работы с нашим ботом.'
                                                        ' Чтобы узнать больше и приобрести подписку, пожалуйста, нажмите на соответствующую кнопку ниже.', reply_markup=keyboard_products())

    # Добавьте ваш код для начала парсинга здесь
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
