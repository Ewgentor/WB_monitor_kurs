from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from database.db import add_user
from states.states import MainSG

router = Router()


@router.message(CommandStart())
async def process_start(message: Message, dialog_manager: DialogManager):

    await add_user(message.chat.id)
    await dialog_manager.start(MainSG.main, mode=StartMode.RESET_STACK)


@router.message(Command("help"))
async def process_help(message: Message, dialog_manager: DialogManager):
    await message.answer("Пользуйтесь главным диалогом по команде /main")


@router.message(Command("main"))
async def process_main(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainSG.main)
