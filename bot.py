import os
import asyncio
import logging
import random
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers import user_handlers, other_handlers
from tools.parsing import request_one_ticket
from settings.settings import data_list

from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
LOG_FILE = 'atach-ebot.log'
REQUEST_INTERVAL = 180

scheduler = AsyncIOScheduler()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

users = [101676827, 225164946]


async def main():
    logging.basicConfig(level=logging.INFO,
                        filename=LOG_FILE,
                        filemode='a',
                        format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
                        '%(lineno)d - %(name)s - %(message)s')
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)
    await schedule_jobs()
    scheduler.start()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def request_dates(dp: Dispatcher):
    current_time = datetime.now()
    print("Дата и время запроса:", current_time.strftime("%d %B %Y, %H:%M:%S"))

    interval = random.randint(3, 5)
    for data in data_list:
        result = request_one_ticket(data)
        if result:
            for user_id in users:
                await bot.send_message(chat_id=user_id, text=result) 
                print(f'Есть билеты: {result}')
        await asyncio.sleep(interval)

async def schedule_jobs():
    scheduler.add_job(request_dates, 'interval', seconds = REQUEST_INTERVAL, args=(dp, ))


if __name__ == '__main__':
    logging.info('Бот запущен')
    asyncio.run(main())