from aiogram.filters.state import State, StatesGroup


class MainSG(StatesGroup):
    main = State()
    docs = State()


class ProductSG(StatesGroup):
    add = State()
    product = State()
    not_found = State()
    bad_response = State()
    wrong_articul = State()


class BookmarksSG(StatesGroup):
    bookmarks_list = State()
    change_bookmarks_list = State()
