import json

from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from tgbot.keyboards import choice_parser_inline_keyboard
from tgbot.misc import AddProductBasket


async def choice_parser(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Выберите маркетплейс',
                                     reply_markup=(await choice_parser_inline_keyboard()).as_markup())
    await state.set_state(AddProductBasket.choice_parser)


async def get_parser(callback: CallbackQuery, state: FSMContext):
    await state.update_data(parser=callback.data)

    await callback.message.edit_text('Отправте ссылку')
    await state.set_state(AddProductBasket.get_product_link)


async def save_product(message: Message, state: FSMContext):
    data = await state.get_data()
    if not (await message.bot.parser[data['parser']].get_product_details(message.text)):
        await message.reply('Такого товара не существует, попробуйте заново')
        return
    await state.clear()
    basket = await message.bot.redis.get(f'basket-{message.from_user.id}')
    basket_data = {
            'url': message.text,
            'parser': data['parser']
        }
    if not basket:
        basket = [basket_data]
    else:
        basket = json.loads(basket)
        if basket_data in basket:
            await message.reply('Такого товар уже существует в вашем корзинке')
            return
        basket.append(basket_data)
    await message.bot.redis.set(f'basket-{message.from_user.id}', json.dumps(basket))
    await message.reply('Сохранено в корзинку')


def register_add_basket_handlers(dp: Dispatcher):
    dp.callback_query.register(choice_parser, lambda callback: callback.data == 'basket_add')
    dp.callback_query.register(get_parser, StateFilter(AddProductBasket.choice_parser))
    dp.message.register(save_product, StateFilter(AddProductBasket.get_product_link))
