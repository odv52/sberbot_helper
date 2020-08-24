import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

#Конфигурация библиотеки
config = dict()
with open('settings.ini') as settings:
    for line in settings:
        curr_line = line.split()
        config[curr_line[0]] = curr_line[2]

API_TOKEN = config['TOKEN']

#Инициализация бота и диспетчера
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

#Конфигурация логгирования
logging.basicConfig(level=logging.INFO)

#Путь к базе данных
sber_db = 'db\sberbot.db'