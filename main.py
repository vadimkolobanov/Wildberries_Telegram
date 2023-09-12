import asyncio
import datetime
import json
import os
import pandas as pd
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InputFile, FSInputFile

from retry import retry

# Токен вашего бота в Telegram (замените на свой токен)
BOT_TOKEN = '6499416429:AAFO0fD4Jq48EGUEPiEkPUklMMqSzkuJy2c'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class Form(StatesGroup):
    waiting_for_url = State()  # Ожидание ввода ссылки
    waiting_for_min_price = State()  # Ожидание ввода минимальной цены
    waiting_for_max_price = State()  # Ожидание ввода максимальной цены
    waiting_for_discount = State()  # Ожидание ввода скидки


def get_catalogs_wb() -> dict:
    url = 'https://www.wildberries.ru/webapi/menu/main-menu-ru-ru.json'
    headers = {'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    return requests.get(url, headers=headers).json()


def get_data_category(catalogs_wb: dict) -> list:
    catalog_data = []
    if isinstance(catalogs_wb, dict) and 'childs' not in catalogs_wb:
        catalog_data.append({
            'name': f"{catalogs_wb['name']}",
            'shard': catalogs_wb.get('shard', None),
            'url': catalogs_wb['url'],
            'query': catalogs_wb.get('query', None)
        })
    elif isinstance(catalogs_wb, dict):
        catalog_data.extend(get_data_category(catalogs_wb['childs']))
    else:
        for child in catalogs_wb:
            catalog_data.extend(get_data_category(child))
    return catalog_data


def search_category_in_catalog(url: str, catalog_list: list) -> dict:
    for catalog in catalog_list:
        if catalog['url'] == url.split('https://www.wildberries.ru')[-1]:
            print(f'найдено совпадение: {catalog["name"]}')
            return catalog


def get_data_from_json(json_file: dict) -> list:
    data_list = []
    for data in json_file['data']['products']:
        data_list.append({
            'Наименование': data['name'],
            'id': data['id'],
            'Скидка': data['sale'],
            'Цена': int(data["priceU"] / 100),
            'Цена со скидкой': int(data["salePriceU"] / 100),
            'Бренд': data['brand'],
            'feedbacks': data['feedbacks'],
            'rating': data['rating'],
            'Ссылка': f'https://www.wildberries.ru/catalog/{data["id"]}/detail.aspx?targetUrl=BP'
        })
    return data_list


@retry(Exception, tries=-1, delay=0)
def scrap_page(page: int, shard: str, query: str, low_price: int, top_price: int, discount: int = None) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
        "Accept": "*/*",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Origin": "https://www.wildberries.ru",
        'Content-Type': 'application/json; charset=utf-8',
        'Transfer-Encoding': 'chunked',
        "Connection": "keep-alive",
        'Vary': 'Accept-Encoding',
        'Content-Encoding': 'gzip',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site"
    }
    url = f'https://catalog.wb.ru/catalog/{shard}/catalog?appType=1&curr=rub' \
          f'&dest=-1257786' \
          f'&locale=ru' \
          f'&page={page}' \
          f'&priceU={low_price * 100};{top_price * 100}' \
          f'&sort=popular&spp=0' \
          f'&{query}' \
          f'&discount={discount}'
    r = requests.get(url, headers=headers)
    print(f'Статус: {r.status_code} Страница {page} Идет сбор...')
    return r.json()


def save_excel(data: list, filename: str):
    df = pd.DataFrame(data)
    writer = pd.ExcelWriter(f'{filename}.xlsx')
    df.to_excel(writer, 'data')
    writer.close()
    print(f'Все сохранено в {filename}.xlsx\n')


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
    try:
        args = message.text.split()
        if len(args) != 5:
            await message.reply(
                "Неверный формат команды. Используйте: /parse ссылка минимальная_цена максимальная_цена скидка")
            return

        url = args[1]
        low_price = int(args[2])
        top_price = int(args[3])
        discount = int(args[4])
        print(url, low_price, top_price, discount)
        catalog_data = get_data_category(get_catalogs_wb())
        category = search_category_in_catalog(url=url, catalog_list=catalog_data)
        data_list = []

        for page in range(1, 51):
            data = scrap_page(
                page=page,
                shard=category['shard'],
                query=category['query'],
                low_price=low_price,
                top_price=top_price,
                discount=discount)
            print(f'Добавлено позиций: {len(get_data_from_json(data))}')
            if len(get_data_from_json(data)) > 0:
                data_list.extend(get_data_from_json(data))
            else:
                break
        print(f'Сбор данных завершен. Собрано: {len(data_list)} товаров.')
        filename = f'{category["name"]}_from_{low_price}_to_{top_price}'
        save_excel(data_list, filename)

        await send_data_to_telegram(data_list, filename, message.chat.id)
        await message.reply(
            f'Ссылка для проверки: {url}?priceU={low_price * 100};{top_price * 100}&discount={discount}')
    except TypeError as e:
        await message.reply(str(e))
    except PermissionError:
        await message.reply('Ошибка! Вы забыли закрыть созданный ранее excel файл. Закройте и повторите попытку')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
