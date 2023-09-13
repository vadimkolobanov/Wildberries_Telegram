import asyncio
import os
import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InputFile, FSInputFile
import os
from dotenv import load_dotenv

load_dotenv()

MY_ENV_VAR = os.getenv('MY_ENV_VAR')
from keyboards import keyboard_start
from parser import get_data_category, get_catalogs_wb, search_category_in_catalog, scrap_page, get_data_from_json, \
    save_excel

BOT_TOKEN = '6499416429:AAFO0fD4Jq48EGUEPiEkPUklMMqSzkuJy2c'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def send_inline_keyboard(message, text, keyboard):
    await message.answer(text, reply_markup=keyboard)


class Form(StatesGroup):
    waiting_for_url = State()  # Ожидание ввода ссылки
    waiting_for_min_price = State()  # Ожидание ввода минимальной цены
    waiting_for_max_price = State()  # Ожидание ввода максимальной цены
    waiting_for_discount = State()  # Ожидание ввода скидки


@dp.message(Command('start'))
async def start(message: types.Message):
    await message.reply("Привет! Я бот для сбора данных с Wildberries. "
                        "Для начала сбора данных, отправь мне ссылку на категорию, например:\n"
                        "https://www.wildberries.ru/catalog/sport/vidy-sпорта/velosport/velosipedy\n"
                        "и указания минимальной цены, максимальной цены и скидки (если нужно).\n"
                        "Пример: /parse https://www.wildberries.ru/catalog/sport/vidy-sporta/velosport/velosipedy 1000 100000 10")


async def send_data_to_telegram(data: list, filename, chat_id: int):
    df = pd.DataFrame(data)
    file_path = f'{filename}.xlsx'
    df.to_excel(file_path, index=False)

    await bot.send_document(chat_id, FSInputFile(file_path))

    os.remove(file_path)


@dp.message(Command('parse'))
async def parse(message: types.Message):
    await send_inline_keyboard(message, "Добро пожаловать! Для начала парсинга нажмите кнопку ниже.", keyboard_start)
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


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
