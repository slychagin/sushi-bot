from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button1 = KeyboardButton('/Режим_работы')
button2 = KeyboardButton('/Адрес')
button3 = KeyboardButton('/Меню')
# button4 = KeyboardButton('Поделиться контактом', request_contact=True)
# button5 = KeyboardButton('Отправить где я', request_location=True)

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)

keyboard_client.add(button3).row(button1, button2)  # .row(button4, button5)
