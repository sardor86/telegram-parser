from aiogram import Dispatcher

from .user import register_user
from .product_parser import register_product_parser
from .product_list import register_product_list
from .add_basket import register_add_basket_handlers


def register_all_user_handlers(dp: Dispatcher):
    register_user(dp)
    register_product_parser(dp)
    register_product_list(dp)
    register_add_basket_handlers(dp)
