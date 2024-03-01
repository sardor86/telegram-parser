from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from tgbot.keyboards import choice_parser_inline_keyboard
from tgbot.misc import ProductParser


async def choice_parser(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text('Выберите маркетплейс',
                                     reply_markup=(await choice_parser_inline_keyboard()).as_markup())
    await state.set_state(ProductParser.choice_parser)


async def get_product_link(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(parser=callback.data.split('_')[0])
    await callback.message.edit_text('Отправте ссылку')
    await state.set_state(ProductParser.get_product_link)


async def pars_product(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()

    product_detail = ''
    if user_data['parser'] == 'aliexpress':
        product_detail_info = message.bot.aliexpress_parser.get_product_details(message.text)
        if not product_detail_info is None:
            product_detail = (f'name: {product_detail_info["name"]}\n'
                              f'price: {product_detail_info["price"]}\n'
                              f'category: {product_detail_info["category"]}\n')
        else:
            product_detail = 'Не нашли'
    if user_data['parser'] == '1688':
        product_detail_info = message.bot.tm_parser.get_product_details(message.text)
        if not product_detail_info['data'] is None:
            product_detail = (f'name: {message.bot.tm_parser.translate_text(product_detail_info["data"]["title"])}\n'
                              f'price: {product_detail_info["data"]["sku_price_scale"]}\n'
                              f'category_id: {product_detail_info["data"]["category_id"]}')
        else:
            product_detail = 'Не нашли'
    if user_data['parser'] == 'wikkeo':
        product_detail_info = message.bot.wikkeo_parser.get_product_details(message.text)
        if not product_detail_info is None:
            product_detail = (f'name: {product_detail_info["name"]}\n'
                              f'price: {product_detail_info["price"]}\n'
                              f'description: {product_detail_info["description"]}')
        else:
            product_detail = 'Не нашли'

    await message.reply(product_detail)

    await state.clear()


def register_product_parser(dp: Dispatcher):
    dp.callback_query.register(choice_parser, lambda callback: callback.data == 'pars_product')
    dp.callback_query.register(get_product_link,
                               lambda callback: callback.data[-14:] == 'product_parser',
                               StateFilter('ProductParser:choice_parser'))
    dp.message.register(pars_product,
                        StateFilter('ProductParser:get_product_link'))
