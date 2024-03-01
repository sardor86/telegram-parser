from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


async def get_start_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='Парсинг отдельного товара', callback_data='pars_product'))
    keyboard.row(InlineKeyboardButton(text='Получить список товаров', callback_data='get_products'))

    return keyboard


async def choice_parser_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='Aliexpress', callback_data='aliexpress_product_parser'))
    keyboard.row(InlineKeyboardButton(text='1688', callback_data='1688_product_parser'))
    keyboard.row(InlineKeyboardButton(text='wikkeo', callback_data='wikkeo_product_parser'))

    return keyboard
