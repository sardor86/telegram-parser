from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.types import CallbackQuery, Message
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from tgbot.keyboards import choice_parser_inline_keyboard, filters_inline_keyboard, choice_category_inline_keyboard
from tgbot.misc import ProductListParser


async def choice_parser(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Выберите маркетплейс',
                                     reply_markup=(await choice_parser_inline_keyboard()).as_markup())
    await state.set_state(ProductListParser.choice_parser)
    await state.update_data(min_price=0, max_price=9999999)


async def set_filters(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Фильтры', reply_markup=(await filters_inline_keyboard()).as_markup())

    await state.update_data(parser=callback.data)


async def set_price(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Выберите минимальную цену')
    await state.set_state(ProductListParser.min_price)


async def set_min_price(message: Message, state: FSMContext):
    if message.text.isdigit():
        await message.reply('Выберите максимальную цену')
        await state.update_data(min_price=int(message.text))

        await state.set_state(ProductListParser.max_price)
    else:
        await message.reply('Это не число повторите заново')


async def set_max_price(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text.isdigit():
        if int(message.text) > int(data['start_price']):
            await message.reply('Фильтры', reply_markup=(await filters_inline_keyboard()).as_markup())
            await state.update_data(max_price=int(message.text))

            await state.set_state(ProductListParser.choice_parser)
        else:
            await message.reply('Минимальная цена не может быть больше или равной максимальной')
    else:
        await message.reply('Это не число повторите заново')


async def choice_category(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    keyboard = await choice_category_inline_keyboard(list(callback.bot.parser[data['parser']].category))

    await callback.message.edit_text('Выберите категорию', reply_markup=keyboard.as_markup())


async def get_category(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data.split('_')[-1])
    await callback.message.edit_text('Фильтры', reply_markup=(await filters_inline_keyboard()).as_markup())

    await state.set_state(ProductListParser.choice_parser)


async def start_pars_product(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if 'category' in data:
        parser = callback.bot.parser[data['parser']]
        product_list = await parser.get_products_list(data['category'],
                                                      min_price=data['min_price'],
                                                      max_price=data['max_price'])
        message = ''
        for product in product_list:
            for product_detail in product:
                message += f'{product_detail}: {product[product_detail]}\n'
            message += '=================\n'
        await callback.message.edit_text('Товары')
        if len(message) > 4096:
            for x in range(0, len(message), 4096):
                await callback.bot.send_message(callback.message.chat.id, message[x:x + 4096])
        else:
            await callback.bot.send_message(callback.message.chat.id, message)
        await state.clear()
    else:
        keyboard = await choice_category_inline_keyboard(list(callback.bot.parser[data['parser']].category))
        await callback.message.edit_text('Пожалуйста выберите категорию', reply_markup=keyboard.as_markup())
        await state.set_state(ProductListParser.choice_parser)


def register_product_list(dp: Dispatcher):
    dp.callback_query.register(start_pars_product, lambda callback: callback.data == 'start_pars_product')
    dp.callback_query.register(choice_parser, lambda callback: callback.data == 'get_products')
    dp.callback_query.register(set_price, lambda callback: callback.data == 'filters_price')
    dp.callback_query.register(choice_category, lambda callback: callback.data == 'filters_category')
    dp.callback_query.register(get_category, lambda callback: callback.data.split('_')[0] == 'category')
    dp.callback_query.register(set_filters, StateFilter(ProductListParser.choice_parser))
    dp.message.register(set_min_price, StateFilter(ProductListParser.min_price))
    dp.message.register(set_max_price, StateFilter(ProductListParser.max_price))
