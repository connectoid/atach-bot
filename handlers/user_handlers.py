from aiogram.filters import Command, CommandStart, StateFilter
from aiogram import Router, F 
from aiogram.types import Message, CallbackQuery


from keyboards.keyboards import main_menu
from tools.parsing import request_tickets

router = Router()


@router.message(CommandStart())
async def proccess_start_command(message: Message):
    await message.answer('Приветствую. Вы запустили бот, который мониторит наличие в продаже билетов',
                         reply_markup=main_menu)


@router.message(F.text == 'Проверить сейчас')
async def process_help_command(message: Message):
    result_list = request_tickets()
    for result_text in result_list:
        if result_text:
            await message.answer(text=result_text, 
                                reply_markup=main_menu)