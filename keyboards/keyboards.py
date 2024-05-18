from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Клавиатура Главного меню
request = KeyboardButton(text='Проверить сейчас')

main_menu = ReplyKeyboardMarkup(
    keyboard=[[request]],
    resize_keyboard=True
)
