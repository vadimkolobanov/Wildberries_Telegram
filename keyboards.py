from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

button = InlineKeyboardButton(text="Начать парсинг", callback_data="start_parsing")

button_start = InlineKeyboardButton(text="Начать парсинг", callback_data="start_parsing")
keyboard_start = InlineKeyboardMarkup(inline_keyboard=[[button_start]])
