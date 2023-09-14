from aiogram import types
from aiogram.fsm.context import FSMContext

from database import session, User, PromoCode
from keyboards import *
from main import dp, Form, bot


@dp.callback_query(lambda c: c.data == 'start_parsing')
async def process_start_parsing(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id,
                           f'Пришлите ссылку на категорию товаров ',
                          )
    await state.set_state(Form.waiting_for_url)


@dp.callback_query(lambda c: c.data == 'products')
async def buy_products_menu(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,
                           'Здравствуйте! Мы рады предложить вам подписку на полную версию нашего бота.'
                           ' Полная версия включает в себя разнообразный дополнительный функционал и неограниченное количество запросов.'
                           ' Это отличная возможность получить максимум от работы с нашим ботом.'
                           ' Чтобы узнать больше и приобрести подписку, пожалуйста, нажмите на соответствующую кнопку ниже.',
                           reply_markup=keyboard_products())


@dp.callback_query(lambda c: c.data == 'profile')
async def profile_menu(callback_query: types.CallbackQuery):
    """
      Обрабатывает запрос на отображение профиля пользователя.

      Args:
          callback_query (types.CallbackQuery): CallbackQuery объект, содержащий информацию о запросе.

      Returns:
          None

      Пример использования:
          Пользователь нажимает на кнопку "Профиль", и функция отображает профиль пользователя с его данными.

      """
    session.rollback()
    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()

    if user:
        registration_date = user.registration_date
        is_vip = user.is_vip
        vip_end_date = user.vip_end_date
        free_requests = user.free_requests
        if not is_vip:
            vip = '❌'
        else:
            vip = '✅'
        if not vip_end_date:
            vip_end_date = '❌'

        await bot.send_message(callback_query.from_user.id,
                               f'{callback_query.from_user.first_name} {callback_query.from_user.last_name} @{callback_query.from_user.username}\n\n'
                               f'Дата регистрации 📅: {registration_date}\n\n'
                               f'Доступно бесплатных запросов 🆓: {free_requests}\n\n'
                               f'🌟 PRO-аккаунт: {vip} до {vip_end_date}' ,
                               reply_markup=keyboard_main())
    else:
        print("Пользователь не найден")
    session.close()

@dp.callback_query(lambda c: c.data == 'promo')
async def promo_menu(callback_query: types.CallbackQuery):
    """
        Обрабатывает запрос на отображение меню для работы с промокодами.

        Args:
            callback_query (types.CallbackQuery): CallbackQuery объект, содержащий информацию о запросе.

        Returns:
            None

        Пример использования:
            Пользователь нажимает на кнопку "Промокоды", и функция отображает меню для работы с промокодами.

        """
    await bot.send_message(callback_query.from_user.id,
                           'примените промокод или создайте',
                           reply_markup=keyboard_promo())


@dp.callback_query(lambda c: c.data == 'create_ref')
async def generate_promo(callback_query: types.CallbackQuery):
    """
       Генерирует и привязывает промокод к пользователю.

       Args:
           callback_query (types.CallbackQuery): CallbackQuery объект, содержащий информацию о запросе.

       Returns:
           None

       Пример использования:
           Пользователь нажимает кнопку "Создать промокод" в меню, и функция генерирует и привязывает промокод к пользователю.

       """
    import random
    import string

    def generate_promocode(length=6):
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    promocode = generate_promocode()
    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()

    if user:

        # Проверьте, не использовал ли пользователь этот промокод уже
        if not any(promo in user.used_promocodes for promo in user.promocodes):
            # Создайте промокод и свяжите его с пользователем
            promo_code = PromoCode(code=promocode, creator=user)
            session.add(promo_code)
            session.commit()
            await bot.send_message(callback_query.from_user.id,
                                   f'Ваш промокод {promocode} ',
                                   reply_markup=keyboard_main())
            return promocode
        else:
            await callback_query.answer("Ваш промокод уже создан")
    else:
        print('Нет юзера')

# Функция для использования промокода
# def use_promocode(user_telegram_id, promocode):
#     # Найдите пользователя по его telegram_id
#     user = session.query(User).filter_by(telegram_id=user_telegram_id).first()
#
#     if user:
#         # Проверьте, не использовал ли пользователь этот промокод уже
#         if not any(promo in user.used_promocodes for promo in user.promocodes):
#             # Обновите информацию в базе данных, например, установите флаг "использовано"
#             # Ваш код для обработки использования промокода здесь
#
#             # Добавьте этот промокод в список использованных для пользователя
#             user.used_promocodes.append(promocode)
#             session.commit()
#             return True
#         else:
#             return False  # Пользователь уже использовал этот промокод
#     else:
#         return False  # Пользователь не найден в базе данных

