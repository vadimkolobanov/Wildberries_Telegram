from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile

from config import dp, bot
from parser_wb import *


class Form(StatesGroup):
    waiting_for_url = State()  # Ожидание ввода ссылки
    waiting_for_min_price = State()  # Ожидание ввода минимальной цены
    waiting_for_max_price = State()  # Ожидание ввода максимальной цены
    waiting_for_discount = State()  # Ожидание ввода скидки

@dp.message(Form.waiting_for_url)
async def get_url_message(message: Message, state: FSMContext):
    """
    Обрабатывает ввод пользователя для получения ссылки.

    Args:
        message (Message): Объект сообщения пользователя.
        state (FSMContext): Контекст Finite State Machine.

    Returns:
        None

    Пример использования:
        Пользователь отправляет боту ссылку, и эта функция обрабатывает введенную ссылку и переключает состояние.
    """
    await state.update_data(waiting_for_url=message.text)
    await message.answer(
        text="Спасибо. Теперь укажите минимальную сумму товара."
    )
    await state.set_state(Form.waiting_for_min_price)

@dp.message(Form.waiting_for_min_price)
async def get_minimal_price(message: Message, state: FSMContext):
    """
    Обрабатывает ввод пользователя для получения минимальной суммы товара.

    Args:
        message (Message): Объект сообщения пользователя.
        state (FSMContext): Контекст Finite State Machine.

    Returns:
        None

    Пример использования:
        Пользователь отправляет боту минимальную сумму товара, и эта функция обрабатывает введенные данные и переключает состояние.
    """
    await state.update_data(waiting_for_min_price=message.text)
    await message.answer(
        text="Спасибо. Теперь укажите максимальную сумму товара."
    )
    await state.set_state(Form.waiting_for_max_price)

@dp.message(Form.waiting_for_max_price)
async def get_maximal_price(message: Message, state: FSMContext):
    """
    Обрабатывает ввод пользователя для получения максимальной суммы товара.

    Args:
        message (Message): Объект сообщения пользователя.
        state (FSMContext): Контекст Finite State Machine.

    Returns:
        None

    Пример использования:
        Пользователь отправляет боту максимальную сумму товара, и эта функция обрабатывает введенные данные и переключает состояние.
    """
    await state.update_data(waiting_for_max_price=message.text)
    await message.answer(
        text="Отлично! Укажите размер скидки без символа процента или отправьте 0."
    )
    await state.set_state(Form.waiting_for_discount)

@dp.message(Form.waiting_for_discount)
async def get_discount(message: Message, state: FSMContext):
    """
    Обрабатывает ввод пользователя для получения размера скидки.

    Args:
        message (Message): Объект сообщения пользователя.
        state (FSMContext): Контекст Finite State Machine.

    Returns:
        None

    Пример использования:
        Пользователь отправляет боту размер скидки, и эта функция обрабатывает введенные данные, переключает состояние и передает данные для обработки парсеру.
    """
    await state.update_data(waiting_for_discount=message.text)
    await message.answer(
        text="Все верно, данные передаются парсеру. Ожидайте ответ."
    )
    user_data = await state.get_data()
    filename = parse(user_data)

    await bot.send_document(message.from_user.id, FSInputFile(f'{filename}.xlsx'))