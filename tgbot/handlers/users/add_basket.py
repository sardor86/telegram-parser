import json
import logging

from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from tgbot.keyboards import choice_parser_inline_keyboard
from tgbot.misc import AddProductBasket

logger = logging.getLogger(__name__)


async def choice_parser(callback: CallbackQuery, state: FSMContext):
    """
    this function sends message with inline buttons of parser name
    and set AddProductBasket.choice_parser
    """
    logger.info('choice parser')
    await callback.message.edit_text('Выберите маркетплейс',
                                     reply_markup=(await choice_parser_inline_keyboard()).as_markup())
    await state.set_state(AddProductBasket.choice_parser)


async def get_parser(callback: CallbackQuery, state: FSMContext):
    """
    this function save parser name to memory and set AddProductBasket.get_product_link
    """
    logger.info('save parser name')
    await state.update_data(parser=callback.data)

    await callback.message.edit_text('Отправте ссылку')
    await state.set_state(AddProductBasket.get_product_link)


async def save_product(message: Message, state: FSMContext):
    """
    this method with parser name and url check product and save it to redis
    """

    # checking that the product exists or not
    logger.info('checking that the product exists or not')
    data = await state.get_data()
    if not (await message.bot.parser[data['parser']].get_product_details(message.text)):
        logger.warning('product not exists')
        await message.reply('Такого товара не существует, попробуйте заново')
        return

    # prepare datas
    logger.info('prepare datas')
    await state.clear()
    basket = await message.bot.redis.get(f'basket-{message.from_user.id}')
    basket_data = {
            'url': message.text.split('?')[0],
            'parser': data['parser']
        }

    # check this product exists in basket and save the product
    logger.info('save product url to basket')
    if not basket:
        basket = [basket_data]
    else:
        basket = json.loads(basket)
        if basket_data in basket:
            logger.warning('this product already exists in basket')
            await message.reply('Такого товар уже существует в вашем корзинке')
            return
        basket.append(basket_data)
    await message.bot.redis.set(f'basket-{message.from_user.id}', json.dumps(basket))
    await message.reply('Сохранено в корзинку')


def register_add_basket_handlers(dp: Dispatcher):
    logger.info('register add basket handlers')
    dp.callback_query.register(choice_parser, lambda callback: callback.data == 'basket_add')
    dp.callback_query.register(get_parser, StateFilter(AddProductBasket.choice_parser))
    dp.message.register(save_product, StateFilter(AddProductBasket.get_product_link))
