from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import keyboard_client
from aiogram.types import ReplyKeyboardRemove


async def start_command(message: types.Message):
    """Send welcome message or link to register bot and install keyboard"""
    try:
        await bot.send_message(message.from_user.id, 'Приятного аппетита!', reply_markup=keyboard_client)
        await message.delete()
    except:
        await message.reply('Общаться с ботом можно через ЛС, напишите ему:\n'
                            'https://t.me/Sushi_ProfiBot')


async def sushi_open_command(message: types.Message):
    """Send message with schedule"""
    await bot.send_message(message.from_user.id, 'Пн-Чт с 10:00 до 21:00, Пт-Вс с 9:00 до 23:00')


async def sushi_address_command(message: types.Message):
    """Send message with sushi-bar address"""
    await bot.send_message(message.from_user.id, 'г. Ростов-на-Дону, ул. Комарова, 28', reply_markup=ReplyKeyboardRemove())


# @dp.message_handler(commands=['Меню'])
# async def sushi_menu_command(message: types.Message):
#     for ret in cur.execute('SELECT * FROM menu').fetchall():
#         await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена: {ret[-1]}')

def register_handlers_client(dp: Dispatcher):
    """Register all client handlers"""
    dp.register_message_handler(start_command, commands=['start', 'help'])
    dp.register_message_handler(sushi_open_command, commands=['Режим_работы'])
    dp.register_message_handler(sushi_address_command,  commands=['Адрес'])
