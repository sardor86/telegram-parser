from aiogram import Dispatcher

from .user import register_user
from .product_parser import register_product_parser


def register_all_user_handlers(dp: Dispatcher):
    register_user(dp)
    register_product_parser(dp)
