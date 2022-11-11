import sqlite3 as sql
from create_bot import bot


def connect_db():
    """Create or connect to db"""
    global db, cur
    db = sql.connect('sushi_profi.db')
    cur = db.cursor()
    if db:
        print('Data base connected OK!')
    db.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY,'
               'description TEXT, price TEXT)')


async def db_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
        db.commit()


async def db_read(message):
    for row in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(
            message.from_user.id,
            row[0],
            f'{row[1]}\n'
            f'Описание: {row[2]}\n'
            f'Цена: {row[-1]}'
        )
