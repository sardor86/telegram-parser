import json

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.filters import StateFilter

from tgbot.keyboards import choice_product_inline_keyboard
from tgbot.misc import DeleteProductBasket


async def choice_product(callback: CallbackQuery, state: FSMContext):
    basket = json.loads(await callback.bot.redis.get(f'basket-{callback.from_user.id}'))
    product_list = []
    for item in basket:
        product_data = (await callback.bot.parser[item['parser']].get_product_details(item['url']))
        product_data['url'] = item['url']
        product_data['parser'] = item['parser']
        product_list.append(product_data)
    await callback.message.edit_text('Выберите продукт',
                                     reply_markup=(await choice_product_inline_keyboard(product_list)).as_markup())
    await state.set_state(DeleteProductBasket.choice_product)
    await state.update_data(product_list=product_list, basket=basket)


async def delete_product(callback: CallbackQuery, state: FSMContext):
    product_id = callback.data.split('_')[1]

    state_data = (await state.get_data())
    product_list = state_data['product_list']
    basket = state_data['basket']

    for product in product_list:
        if product['url'].split('-')[-1] == product_id:
            basket.remove({'parser': product['parser'], 'url': product['url']})

    await callback.bot.redis.set(f'basket-{callback.from_user.id}', json.dumps(basket))

    await callback.message.edit_text('Товар был удален')
    await state.clear()


def register_delete_basket_handler(dp: Dispatcher):
    dp.callback_query.register(choice_product, lambda callback: callback.data == 'basket_delete')
    dp.callback_query.register(delete_product, StateFilter(DeleteProductBasket.choice_product))
