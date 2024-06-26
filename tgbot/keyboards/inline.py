from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


async def get_start_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='Парсинг отдельного товара', callback_data='pars_product'))
    keyboard.row(InlineKeyboardButton(text='Получить список товаров', callback_data='get_products'))

    return keyboard


async def choice_parser_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='1688', callback_data='1688'))
    keyboard.row(InlineKeyboardButton(text='wikkeo', callback_data='wikkeo'))

    return keyboard


async def filters_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='Цена', callback_data='filters_price'))
    keyboard.row(InlineKeyboardButton(text='Категории', callback_data='filters_category'))
    keyboard.row(InlineKeyboardButton(text='Начать парсинг', callback_data='start_pars_product'))

    return keyboard


async def choice_category_inline_keyboard(categories_list: list) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    for category in categories_list:
        keyboard.row(InlineKeyboardButton(text=category, callback_data=f'category_{category}'))

    return keyboard


async def basket_control_inline_keyboard(add_button: bool = True, delete_button: bool = True) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    if add_button:
        keyboard.row(InlineKeyboardButton(text='Добавить', callback_data='basket_add'))

    if delete_button:
        keyboard.row(InlineKeyboardButton(text='Удалить', callback_data='basket_delete'))

    return keyboard


async def choice_product_inline_keyboard(products_list: list) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    for product in products_list:
        keyboard.row(InlineKeyboardButton(text=product['name'],
                                          callback_data=f'product_{product["url"].split("/")[-1][:-64]}'))

    return keyboard
