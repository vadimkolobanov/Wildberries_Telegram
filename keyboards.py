from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def keyboard_main():
    """
    Генерирует основную клавиатуру для главного меню.

    Returns:
        InlineKeyboardMarkup: Встроенная клавиатура.
    """
    button_start = InlineKeyboardButton(text="Начать парсинг ✅", callback_data="start_parsing")
    profile = InlineKeyboardButton(text="Мой профиль 👤", callback_data="profile")
    pro_buy = InlineKeyboardButton(text="Товары 💰", callback_data="products")
    free = InlineKeyboardButton(text="Промокоды и акции", callback_data="promo")
    keyboard_start = InlineKeyboardMarkup(inline_keyboard=[[button_start],[profile,pro_buy],[free]])
    return keyboard_start

def keyboard_products():
    """
    Генерирует клавиатуру для меню товаров.

    Returns:
        InlineKeyboardMarkup: Встроенная клавиатура.
    """
    pro_account = InlineKeyboardButton(text="PRO-аккаунт", callback_data="one_mounth_buy")
    free_package = InlineKeyboardButton(text="Пакет бесплатных запросов (100р = 100)", callback_data="six_mounth_buy")

    keyboard_productst = InlineKeyboardMarkup(inline_keyboard=[[free_package], [pro_account]])
    return keyboard_productst

def keyboard_promo():
    """
    Генерирует клавиатуру для меню промокодов.

    Returns:
        InlineKeyboardMarkup: Встроенная клавиатура.
    """
    input_ref_code = InlineKeyboardButton(text="Применить код✅", callback_data="use_ref")
    keyboard_promo = InlineKeyboardMarkup(inline_keyboard=[[input_ref_code],])
    return keyboard_promo
