from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton


async def start_reply_button():
    keyboard = [
        [KeyboardButton(text='Начать')],
        [KeyboardButton(text='Корзинка')]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
