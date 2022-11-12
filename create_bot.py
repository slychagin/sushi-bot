import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
load_dotenv(override=True)

bot = Bot(token=os.environ.get('TOKEN'))
dp = Dispatcher(bot, storage=storage)
