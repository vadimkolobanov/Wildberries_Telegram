from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def keyboard_main():
    button_start = InlineKeyboardButton(text="Начать парсинг ✅", callback_data="start_parsing")
    profile = InlineKeyboardButton(text="Мой профиль 👤", callback_data="start_parsing")
    pro_buy = InlineKeyboardButton(text="Продукты 💰", callback_data="products")
    keyboard_start = InlineKeyboardMarkup(inline_keyboard=[[button_start],[profile,pro_buy]])
    return keyboard_start

def keyboard_products():
    mounth_1 = InlineKeyboardButton(text="Приобрести 1 месяц", callback_data="one_mounth_buy")
    mounth_6 = InlineKeyboardButton(text="Приобрести 6 месяцев", callback_data="six_mounth_buy")
    year = InlineKeyboardButton(text="Приобрести на год", callback_data="year_buy")
    keyboard_productst = InlineKeyboardMarkup(inline_keyboard=[[mounth_1], [mounth_6],[year]])
    return keyboard_productst

