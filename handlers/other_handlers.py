import json

from typing import Any
from aiogram.types import Message, LabeledPrice, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button

from api import api
from database.db import add_bookmark, get_bookmarks, delete_bookmark
from states.states import ProductSG, BookmarksSG
from config.config import load_config
from tools.utility import find_articul, get_price_emoji


async def handle_articul(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        data: Any):

    data = api.get_data(dialog_manager.find("articul").get_value())
    if data["code"] == 2:
        dialog_manager.dialog_data["product"] = data
        await dialog_manager.switch_to(ProductSG.product)
    elif data["code"] == 0:
        await dialog_manager.switch_to(ProductSG.not_found)
    elif data["code"] == -1:
        await dialog_manager.switch_to(ProductSG.wrong_articul)
    else:
        await dialog_manager.switch_to(ProductSG.bad_response)


async def get_product_data(**kwargs):
    return kwargs['dialog_manager'].dialog_data["product"]


async def nonint_articul_error(
        message: Message,
        dialog_: Any,
        manager: DialogManager,
        error_: ValueError
):
    await message.answer("Артикул должен содержать только цифры!")


async def buy_scam(
        callback: CallbackQuery, button: Button,
        manager: DialogManager
):
    invoice_payload = {
        "user_id": callback.from_user.id,
        "product_name": "premium"
    }
    await callback.message.answer_invoice(
        title="Поддержать донатом",
        description="Все базовые услуги бота предоставляются БЕСПЛАТНО и БЕЗ ОГРАНИЧЕНИЙ, если хотите поддержать меня и получить небольшие плюшки, можете символически заплатить 100 рублей.",
        payload=json.dumps(invoice_payload),
        provider_token=load_config().provider_id,
        prices=[LabeledPrice(label="К оплате", amount=10000)],
        currency="RUB",
        start_parameter="test_payment",
    )


async def handle_bookmark_add(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager
):
    await add_bookmark(
        callback.message.chat.id,
        manager.dialog_data['product']['name'],
        manager.dialog_data['product']['articul'],
        manager.dialog_data['product']['price'][:-2]
    )




async def start_bookmarks(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager
):
    db_r = await get_bookmarks(callback.message.chat.id)
    data = {'bookmarks': []}
    for product in db_r:
        new_price = api.get_data(product[-2])['price'],
        data['bookmarks'].append({
            'articul': product[-2],
            'name': product[1][:24] + '...',
            'old_price': "{:.2f}".format(product[2]) + ' ₽',
            'new_price': new_price[0],
            'price_changed': get_price_emoji(product[2], new_price[0])
        })
    await manager.start(BookmarksSG.bookmarks_list, data=data)


async def get_bookmars_data(**kwargs):
    return kwargs['dialog_manager'].start_data


async def handle_delete(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager
):
    articul = manager.event.data.split(sep=':')[1]
    user_id = callback.from_user.id
    manager.start_data['bookmarks'].pop(find_articul(articul, manager.start_data['bookmarks']))
    await delete_bookmark(user_id, articul)

