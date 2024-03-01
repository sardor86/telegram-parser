from aiogram import Dispatcher
from aiogram.types import Message

from aiogram.filters.command import Command

from tgbot.keyboards import get_start_inline_keyboard


async def user_start(message: Message):
    await message.reply('Выберите действие', reply_markup=(await get_start_inline_keyboard()).as_markup())


def register_user(dp: Dispatcher):
    dp.message.register(user_start, Command('start'))
