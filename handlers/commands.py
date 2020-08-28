import logging
import re
from aiogram import types, bot
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from prefs import dp
from interface import messages
from interface import menu_buttons
from classes.class_user import User


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer(messages.process_start_command, reply_markup = menu_buttons.markup_main_menu)

@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    
    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await message.reply('Процесс завершен, вы в главном меню', reply_markup = menu_buttons.markup_main_menu)
    
@dp.message_handler(regexp='^(user_info)\S*')
async def process_user_info_command(message: types.Message):
    command = message.text
    personnel_num = re.findall(r'^user_info (\d+)', command)
    user = User()
    user.define(personnel_num[0], 'db\sberbot.db')
    user.get_sber_info()
    answer = messages.msg_full_user_info(user.userdata)
    await message.answer(answer, reply_markup = menu_buttons.markup_main_menu)
    
# @dp.message_handler(commands=['dev_msgs'])
# async def process_devmsgs_command(message: types.Message):
#     mail_pack = user_getAllMails(message.chat['id'], write_to_db = True)
#     for mail in mail_pack:
#         await bot.send_message(mail['user_id'], 'Message type: {}\nDay: {}\nTime: {}\nText: {}'.format(mail['tag'], mail['practice_day'], mail['letter_time'], mail['letter_text']))  

# @dp.message_handler(commands=['dev_updateList'])
# async def process_devupdateList_command(message: types.Message):
#     shedule_list_reader(overwrite=True)
#     await message.answer('БД обновлена', reply_markup = menu_buttons.markup_register_menu)
    