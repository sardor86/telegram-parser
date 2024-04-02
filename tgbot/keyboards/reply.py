from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton


async def start_reply_button():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Начать')]], resize_keyboard=True)
