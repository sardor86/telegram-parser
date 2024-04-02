from aiogram import Dispatcher
from aiogram.types import Message

from aiogram.filters.command import Command

from tgbot.keyboards import get_start_inline_keyboard, start_reply_button


async def user_start(message: Message):
    await message.reply('Бот парсер\nПарсит с Wikkeo и 1688', reply_markup=(await start_reply_button()))

async def choice_action(message: Message):
    await message.reply('Выберите действие', reply_markup=(await get_start_inline_keyboard()).as_markup())


def register_user(dp: Dispatcher):
    dp.message.register(user_start, Command('start'))
    dp.message.register(choice_action, lambda message: message.text.lower() == 'начать')
