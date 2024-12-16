from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram_dialog import DialogManager, StartMode

from lexicon.lexicon_ru import LEXICON
from database.db import add_user
from states.states import MainSG

router = Router()


@router.message(CommandStart())
async def process_start(message: Message, dialog_manager: DialogManager):
    await message.answer(text=LEXICON['start'], reply_markup=ReplyKeyboardRemove())
    await add_user(message.chat.id)
    await dialog_manager.start(MainSG.main, mode=StartMode.RESET_STACK)


@router.message(Command("help"))
async def process_help(message: Message, dialog_manager: DialogManager):
    await message.answer(LEXICON['help'],
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[[KeyboardButton(text=LEXICON['start_btn'])]]
                         ))


@router.message(Command("main"))
async def process_main(message: Message, dialog_manager: DialogManager):
    await message.answer(LEXICON['return'], reply_markup=ReplyKeyboardRemove())
    await dialog_manager.start(MainSG.main)
