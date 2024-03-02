from aiogram.fsm.state import State, StatesGroup


class ProductParser(StatesGroup):
    choice_parser = State()
    get_product_link = State()


class ProductListParser(StatesGroup):
    choice_parser = State()
    start_price = State()
    end_price = State()
