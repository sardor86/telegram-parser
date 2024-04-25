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
    await state.update_data(parser=callback.data)
    await callback.message.edit_text('Отправте ссылку')
    await state.set_state(ProductParser.get_product_link)


async def pars_product(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()

    product_detail = ''
    parser = message.bot.parser[user_data['parser']]
    product_detail_info = await parser.get_product_details(message.text)
    if product_detail_info:
        for product_info in product_detail_info:
            product_detail += f'{product_info}: {product_detail_info[product_info]}\n'
    else:
        product_detail = 'Не нашли'

    await message.reply(product_detail)

    await state.clear()


def register_product_parser(dp: Dispatcher):
    dp.callback_query.register(choice_parser, lambda callback: callback.data == 'pars_product')
    dp.callback_query.register(get_product_link, StateFilter('ProductParser:choice_parser'))
    dp.message.register(pars_product, StateFilter('ProductParser:get_product_link'))
