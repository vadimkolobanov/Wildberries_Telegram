from aiogram import types
from aiogram.fsm.context import FSMContext

from keyboards import keyboard_products
from main import dp, Form, bot


@dp.callback_query(lambda c: c.data == 'start_parsing')
async def process_start_parsing(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer("Отправьте мне ссылку на категорию, чтобы начать сбор данных.")
    await state.set_state(Form.waiting_for_url)


@dp.callback_query(lambda c: c.data == 'products')
async def buy_products_menu(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,
                           'Здравствуйте! Мы рады предложить вам подписку на полную версию нашего бота.'
                           ' Полная версия включает в себя разнообразный дополнительный функционал и неограниченное количество запросов.'
                           ' Это отличная возможность получить максимум от работы с нашим ботом.'
                           ' Чтобы узнать больше и приобрести подписку, пожалуйста, нажмите на соответствующую кнопку ниже.',
                           reply_markup=keyboard_products())
