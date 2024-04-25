import json

from aiogram import Dispatcher
from aiogram.types import Message

from aiogram.filters.command import Command

from tgbot.keyboards import get_start_inline_keyboard, start_reply_button, basket_control_inline_keyboard


async def user_start(message: Message):
    await message.reply('Бот парсер\nПарсит с Wikkeo и 1688', reply_markup=(await start_reply_button()))


async def choice_action(message: Message):
    await message.reply('Выберите действие', reply_markup=(await get_start_inline_keyboard()).as_markup())


async def get_basket(message: Message):
    basket = await message.bot.redis.get(f'basket-{message.from_user.id}')
    if not basket:
        await message.reply('Ваша корзинка пуста',
                            reply_markup=(await basket_control_inline_keyboard(delete_button=False)).as_markup())
        return
    basket = json.loads(basket)

    overcrowded = len(basket) >= 10
    await message.reply(f'Ваша корзинка\n{[f"{item}" for item in basket]}',
                        reply_markup=(await basket_control_inline_keyboard(add_button=(not overcrowded))).as_markup())


def register_user(dp: Dispatcher):
    dp.message.register(user_start, Command('start'))
    dp.message.register(choice_action, lambda message: message.text.lower() == 'начать')
    dp.message.register(get_basket, lambda message: message.text.lower() == 'корзинка')
