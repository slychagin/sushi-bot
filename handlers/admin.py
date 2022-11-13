from aiogram import types, Dispatcher
from create_bot import bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import admin_keyboard
from data_base import sqlite_db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ID = None


class FSMAdmin(StatesGroup):
    """Finite state machine. Writing all states."""
    photo = State()
    name = State()
    description = State()
    price = State()


async def make_changes_command(message: types.Message):
    """Check is user admin. If admin then allow changes."""
    global ID
    ID = message.from_user.id
    await bot.send_message(
        message.from_user.id,
        'Что, руководитель, надо?',
        reply_markup=admin_keyboard.admin_kb
    )
    await message.delete()


async def command_start(message: types.Message):
    """Start dialog to load a new menu item"""
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')


async def cancel_handler(message: types.Message, state: FSMContext):
    """Escaping from all states"""
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('ОК')


async def load_photo(message: types.Message, state: FSMContext):
    """Get first answer and save photo to dictionary"""
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Теперь введи название')


async def load_name(message: types.Message, state: FSMContext):
    """Get second answer and save name to dictionary"""
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи описание')


async def load_description(message: types.Message, state: FSMContext):
    """Get third answer and save description to dictionary"""
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь укажи цену')


async def load_price(message: types.Message, state: FSMContext):
    """Get forth answer, save price to dictionary and save all data to database"""
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = message.text

        await sqlite_db.db_add_command(state)
        await state.finish()


async def call_back_run(callback_query: types.CallbackQuery):
    await sqlite_db.db_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(
        text=f'{callback_query.data.replace("del ", "")} удалена.',
        show_alert=True
    )


async def delete_item(message: types.Message):
    """Read all data from db, create Delete button"""
    if message.from_user.id == ID:
        read_data = await sqlite_db.db_read_all()
        for row in read_data:
            await bot.send_photo(
                message.from_user.id,
                row[0],
                f'{row[1]}\n'
                f'Описание: {row[2]}\n'
                f'Цена: {row[-1]}'
            )
            await bot.send_message(
                message.from_user.id,
                text='^^^',
                reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                    f'Удалить {row[1]}',
                    callback_data=f'del {row[1]}'
                ))
            )


def register_handlers_admin(dp: Dispatcher):
    """Register all admin handlers"""
    dp.register_message_handler(command_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(make_changes_command, commands=['admin'], is_chat_admin=True)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(cancel_handler, state='*', commands='отмена')
    dp.register_message_handler(delete_item, commands=['Удалить'])
    dp.register_callback_query_handler(call_back_run, lambda x: x.data and x.data.startswith('del '))
