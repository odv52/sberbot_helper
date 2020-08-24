# from aiogram import Bot, Dispatcher, types
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.dispatcher.filters import Text
# from aiogram.types import ParseMode
# from aiogram.utils import executor
# from aiogram.utils.emoji import emojize
# from aiogram.dispatcher import FSMContext
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# import asyncio
# import time
# import datetime
# import bot_messages
# import logging
# import bot_db_loadFromBot as db
# import re
# from bot_userStates import registerUser, rateMentor
# from bot_mailList import user_mailToSend, user_getAllMails
# from bot_requests import get_user_info, get_user_status, get_user_rate_state
# from bot_db_loadFromFile import shedule_list_reader

from prefs import dp
from aiogram.utils import executor

import interface
import handlers

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


# async def scheduled(wait_for):
#     while True:
#         curr_time = datetime.datetime.now()
#         await asyncio.sleep(wait_for)
#         mail_pack = user_mailToSend(curr_time, by_hour = True)
#         for mail in mail_pack:
#             await bot.send_message(mail['user_id'], 'Message type: {}\nDay: {}\nTime: {}\nText: {}'.format(mail['tag'], mail['practice_day'], mail['letter_time'], mail['letter_text']))                
            
#dp.loop.create_task(scheduled(5))
    
    


