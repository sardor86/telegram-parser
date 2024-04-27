import json
import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.filters import StateFilter

from tgbot.keyboards import choice_product_inline_keyboard
from tgbot.misc import DeleteProductBasket

logger = logging.getLogger(__name__)


async def choice_product(callback: CallbackQuery, state: FSMContext):
    """
    this function sends message with inline button of products name
    then set DeleteProductBasket.choice_product state
    after that save product list and basket to memory
    """
    logger.info('get basket')
    basket = json.loads(await callback.bot.redis.get(f'basket-{callback.from_user.id}'))

    logger.info('prepare product list')
    product_list = []
    for item in basket:
        product_data = (await callback.bot.parser[item['parser']].get_product_details(item['url']))
        product_data['url'] = item['url']
        product_data['parser'] = item['parser']
        product_list.append(product_data)

    logger.info('send message with inline buttons of products')
    await callback.message.edit_text('Выберите продукт',
                                     reply_markup=(await choice_product_inline_keyboard(product_list)).as_markup())

    logger.info('set state and save product list and basket')
    await state.set_state(DeleteProductBasket.choice_product)
    await state.update_data(product_list=product_list, basket=basket)


async def delete_product(callback: CallbackQuery, state: FSMContext):
    """
    this function find product by id and delete it in basket
    after that save it to redis
    """

    logger.info('prepare data for delete product from basket')
    product_id = callback.data.split('_')[1]

    state_data = (await state.get_data())
    product_list = state_data['product_list']
    basket = state_data['basket']

    logger.info('delete product from basket')
    for product in product_list:
        if product['url'].split('-')[-1] == product_id:
            basket.remove({'parser': product['parser'], 'url': product['url']})
            break

    logger.info('save basket to redis')
    await callback.bot.redis.set(f'basket-{callback.from_user.id}', json.dumps(basket))

    await callback.message.edit_text('Товар был удален')
    await state.clear()


def register_delete_basket_handler(dp: Dispatcher):
    logger.info('register delete basket handlers')
    dp.callback_query.register(choice_product, lambda callback: callback.data == 'basket_delete')
    dp.callback_query.register(delete_product, StateFilter(DeleteProductBasket.choice_product))
