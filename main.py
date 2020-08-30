from aiogram import Bot, Dispatcher, types
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.dispatcher.filters import Text
# from aiogram.types import ParseMode
# from aiogram.utils import executor
# from aiogram.utils.emoji import emojize
# from aiogram.dispatcher import FSMContext
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
# import time
import datetime
from classes.class_mails import user_hourlyMail 
#import bot_messages
# import logging
# import bot_db_loadFromBot as db
# import re
# from bot_userStates import registerUser, rateMentor
# from bot_mailList import user_mailToSend, user_getAllMails
# from bot_requests import get_user_info, get_user_status, get_user_rate_state
# from bot_db_loadFromFile import shedule_list_reader

from prefs import dp
from prefs import sber_db
from prefs import bot
from aiogram.utils import executor

import interface
import handlers

async def scheduled(wait_for):
    while True:
        curr_time = datetime.datetime.now()
        await asyncio.sleep(wait_for) 
        mail_pack = user_hourlyMail(curr_time, sber_db)
        for userpack in mail_pack:
            for mail in userpack:
                await bot.send_message(mail['tg_uid'], text='Message type: {}\nDay: {}\nTime: {}\nText: {}'.format(mail['tag'], mail['practice_day'], mail['letter_time'], mail['letter_text']))                

if __name__ == '__main__':
    dp.loop.create_task(scheduled(3))
    executor.start_polling(dp, skip_updates=True)

    
    


