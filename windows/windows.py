from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Row, Start, Next, Url, Back, Button, SwitchTo, ListGroup
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from handlers.other_handlers import nonint_articul_error, handle_articul, get_product_data, buy_scam, \
    handle_bookmark_add, start_bookmarks, get_bookmars_data, handle_delete
from states.states import MainSG, ProductSG, BookmarksSG


def get_success_window():
    success_window = Window(
                StaticMedia(
                    url=Format('{img}'),
                ),
                Format('Название: {name}\nБренд: {brand}\nПоставщик: {supplier}\nАртикул: {articul}\nЦена: {price}'),
                Row(
                    Start(
                        Const("Добавить в закладки"),
                        id="saved",
                        state=ProductSG.add,
                        data={'name': Format('{name}'),
                              'articul': Format('{articul}'),
                              'price': Format('{price}')},
                        on_click=handle_bookmark_add
                    ),
                ),
                Row(
                    Start(Const("Отмена"), id='main', state=MainSG.main),
                ),
                state=ProductSG.product,
                getter=get_product_data
            )
    return success_window


def get_error_window(code):
    msg = {
        -1: ["Неверный артикул", ProductSG.wrong_articul],
        0: ["Товар не найден", ProductSG.not_found],
        1: ["Некорректный запрос серверу! Обратитесь к администратору", ProductSG.bad_response]
    }
    error_window = Window(
        Format(f'Ошибка!\n{msg[code][0]}!'),
        Row(
            Back(Const("Попробовать ещё раз"), id="try_again"),
        ),
        Row(
            Start(Const("Отмена"), id='main', state=MainSG.main),
        ),
        state=msg[code][1]
    )
    return error_window


def get_main_dialog():
    main_dialog = Dialog(
        Window(
            Const("Добро пожаловать в бота для мониторинга цен в Wildberries! Выберите нужную опцию из представленных ниже кнопок."),
            Row(
                Start(Const("Добавить товар"), id="add_product", state=ProductSG.add, ),
                Button(Const("В свои закладки"), id="bookmarks", on_click=start_bookmarks),
                Next(text=Const('Документация')),
            ),
            Row(
                Button(
                    Const("Поддержать разработчика"),
                    id="buy_premium",
                    on_click=buy_scam
                )
            ),
            state=MainSG.main,
        ),
        Window(
            Const("Аiogram-dialog 3.13.1"),
            Url(
                Const("Docs"),
                Const('https://aiogram-dialog.readthedocs.io/en/stable/index.html')
            ),
            Back(text=Const("Назад")),
            state=MainSG.docs,
        ),
    )
    return main_dialog


def get_product_dialog():
    product_dialog = Dialog(
        Window(
            Const("Введите артикул товара:"),
            Row(
                Start(Const("В меню"), id="menu", state=MainSG.main,)
            ),
            TextInput(id="articul", on_success=handle_articul, on_error=nonint_articul_error, type_factory=int,),
            state=ProductSG.add,

        ),
        get_error_window(-1),
        get_error_window(0),
        get_error_window(1),
        get_success_window(),
    )
    return product_dialog


def get_bookmarks_dialog():
    bookmarks_dialog = Dialog(
        Window(
            Const("Ваши закладки"),
            ListGroup(
                Url(Format(
                    "{item[name]} {item[new_price]} {item[price_changed]} {item[old_price]}"),
                    id='bookmark_button',
                    url=Format('https://www.wildberries.ru/catalog/{item[articul]}/detail.aspx')),
                id="bookmarks",
                items="bookmarks",
                item_id_getter=lambda item: item['articul']
            ),
            Row(
                Start(Const("В меню"), id="menu", state=MainSG.main,),
                SwitchTo(Const("Редактировать"), id='change', state=BookmarksSG.change_bookmarks_list,)
            ),
            state=BookmarksSG.bookmarks_list,
            getter=get_bookmars_data,
        ),
        Window(
            Const("Выберите закладку для удаления"),
            ListGroup(
                Button(Format(
                    "{item[name]} {item[new_price]} {item[price_changed]} {item[old_price]}"),
                    id='delete_bookmark',
                    on_click=handle_delete,

                ),
                id="bookmarks",
                items="bookmarks",
                item_id_getter=lambda item: item['articul']
            ),
            Row(
                Back(Const("Назад"), id="menu",),
            ),
            state=BookmarksSG.change_bookmarks_list,
            getter=get_bookmars_data,
        )
    )
    return bookmarks_dialog

