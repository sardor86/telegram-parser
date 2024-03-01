from aiogram.fsm.state import State, StatesGroup


class ProductParser(StatesGroup):
    choice_parser = State()
    get_product_link = State()
