import sqlite3 as sql
from create_bot import bot


def connect_db():
    """Create or connect to db"""
    global db, cur
    db = sql.connect('sushi_profi.db')
    cur = db.cursor()
    if db:
        print('Data base connected OK!')
    db.execute('''CREATE TABLE IF NOT EXISTS
    menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)''')


async def db_add_command(state):
    """Add sushi to db"""
    async with state.proxy() as data:
        cur.execute('''SELECT count(*) FROM menu WHERE name=?''', (data['name'],))
        res = cur.fetchone()[0]
        values = tuple(data.values())
        if res == 1:
            cur.execute('''UPDATE menu SET img=?, name=?, description=?, price=?
            WHERE name=?''', (values[0], values[1], values[2], values[3], data['name']))
        else:
            cur.execute('''INSERT INTO menu VALUES (?, ?, ?, ?)''', tuple(data.values()))
        db.commit()


async def db_read(message):
    for row in cur.execute('''SELECT * FROM menu''').fetchall():
        await bot.send_photo(
            message.from_user.id,
            row[0],
            f'{row[1]}\n'
            f'Описание: {row[2]}\n'
            f'Цена: {row[-1]}'
        )


async def db_delete_command(data):
    """Delete item from db"""
    cur.execute('''DELETE FROM menu WHERE name=?''', (data,))
    db.commit()


async def db_read_all():
    """Read all from db"""
    return cur.execute('''SELECT * FROM menu''').fetchall()
