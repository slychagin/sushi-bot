from aiogram import executor
from create_bot import dp
from handlers import client, admin, other
from data_base import sqlite_db
import inline


async def on_startup(_):
    print('Бот вышел онлайн.')
    sqlite_db.connect_db()

inline.register_handlers_inline(dp)
client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
