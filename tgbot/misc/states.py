from aiogram.fsm.state import State, StatesGroup


class ProductParser(StatesGroup):
    choice_parser = State()
    get_product_link = State()


class ProductListParser(StatesGroup):
    choice_parser = State()
    min_price = State()
    max_price = State()


class AddProductBasket(StatesGroup):
    choice_parser = State()
    get_product_link = State()


class DeleteProductBasket(StatesGroup):
    choice_product = State()
