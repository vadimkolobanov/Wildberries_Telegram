from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from config import dp
from parser import parse


class Form(StatesGroup):
    waiting_for_url = State()  # Ожидание ввода ссылки
    waiting_for_min_price = State()  # Ожидание ввода минимальной цены
    waiting_for_max_price = State()  # Ожидание ввода максимальной цены
    waiting_for_discount = State()  # Ожидание ввода скидки


@dp.message(Form.waiting_for_url)
async def get_url_message(message: Message, state: FSMContext):
    await state.update_data(waiting_for_url=message.text)
    await message.answer(
        text="Спасибо. Теперь укажите минимальную сумму товара"
    )
    await state.set_state(Form.waiting_for_min_price)


@dp.message(Form.waiting_for_min_price)
async def get_minimal_price(message: Message, state: FSMContext):
    await state.update_data(waiting_for_min_price=message.text)
    await message.answer(
        text="Спасибо. Теперь укажите максимальную сумму товара"
    )
    await state.set_state(Form.waiting_for_max_price)


@dp.message(Form.waiting_for_max_price)
async def get_minimal_price(message: Message, state: FSMContext):
    await state.update_data(waiting_for_max_price=message.text)
    await message.answer(
        text="Отлично! Укажите размер скидки без символа процента или отправьте 0"
    )
    await state.set_state(Form.waiting_for_discount)


@dp.message(Form.waiting_for_discount)
async def get_minimal_price(message: Message, state: FSMContext):
    await state.update_data(waiting_for_discount=message.text)
    await message.answer(
        text="Все верно, данные передаются парсеру. Ожидайте ответ."
    )
    user_data = await state.get_data()
    parse(user_data, message.from_user.id)
    print(user_data)
