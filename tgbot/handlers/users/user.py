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

    changed = False

    message_result = 'Ваша корзинка\n'
    for basket_item in basket:
        item_data = (await message.bot.parser[basket_item['parser']].get_product_details(basket_item['url']))
        if not item_data:
            basket.remove(basket_item)
            changed = True
        message_result += (f'⭕ url: {basket_item["url"]}\n'
                           f'name: {item_data["name"]}\n'
                           f'price: {item_data["price"]}\n')

    if changed:
        await message.bot.redis.set(f'basket-{message.from_user.id}', json.dumps(basket))
    await message.reply(message_result,
                        reply_markup=(await basket_control_inline_keyboard(add_button=(len(basket) <= 10))).as_markup())


def register_user(dp: Dispatcher):
    dp.message.register(user_start, Command('start'))
    dp.message.register(choice_action, lambda message: message.text.lower() == 'начать')
    dp.message.register(get_basket, lambda message: message.text.lower() == 'корзинка')
