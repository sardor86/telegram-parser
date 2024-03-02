from aiogram import Dispatcher

from .user import register_user
from .product_parser import register_product_parser
from .product_list import register_product_list


def register_all_user_handlers(dp: Dispatcher):
    register_user(dp)
    register_product_parser(dp)
    register_product_list(dp)
