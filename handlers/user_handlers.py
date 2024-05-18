import random
from datetime import datetime

from aiogram.filters import Command, CommandStart, StateFilter
from aiogram import Router, F 
from aiogram.types import Message, CallbackQuery


from keyboards.keyboards import main_menu
from tools.parsing import request_tickets

router = Router()

answers = [
    'Для вас у нас нет билетов.',
    'Все билеты проданы, даже стоячие.',
    'Билеты закончились, когда прилетели Провиденцы.',
    'Продажа билетов остановлена до следующего года.',
    'Извините, но у нас нет билетов для людей.',
    'Мы продаем билеты только жителям Марса.',
    'Все билеты уже куплены вашими соседями.',
    'У нас есть билеты только на следующий год.',
    'Извините, но мы не можем продавать билеты людям.',
    'Билеты закончились, потому что они были нужны только другим.',
    'Извините, но у нас нет билетов для вас.',
    'Прошу прощения, но наш поставщик билетов сказал, что больше не будет их поставлять.',

]

@router.message(CommandStart())
async def proccess_start_command(message: Message):
    await message.answer('Приветствую. Вы запустили бот, который мониторит наличие в продаже билетов',
                         reply_markup=main_menu)


@router.message(F.text == 'Проверить сейчас')
async def process_help_command(message: Message):
    current_time = datetime.now()
    current_time = current_time.strftime("%d %B %Y, %H:%M:%S")
    print(f'Билеты запрошены вручную в {current_time}')
    result_list = request_tickets()
    if result_list:
        for result_text in result_list:
            if result_text:
                print(result_text)
                await message.answer(text=result_text, 
                                    reply_markup=main_menu)
    else:
        random_text = random.choice(answers)
        print(random_text)
        await message.answer(text=random_text, 
                                    reply_markup=main_menu)