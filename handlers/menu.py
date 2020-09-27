from prefs import dp
from prefs import sber_db
from aiogram import types
from interface import messages
from interface import menu_buttons
from classes import class_mails
import datetime


#Кнопки главного меню
@dp.message_handler(regexp='^(FAQ)\S*')
async def process_faq_button(message: types.Message):
    await message.answer(messages.process_faq_button, reply_markup = menu_buttons.markup_faq_menu)

# @dp.message_handler(regexp='^(Информация)\S*')
# async def process_info_button(message: types.Message):
#     #document = config['SBER_INFO_ID']
#     await message.answer_document(document, messages.process_info_button, reply_markup = markup_main_menu)

@dp.message_handler(regexp='^(Задачи)\S*')
async def process_task_button(message: types.Message):
    curr_time = datetime.datetime.now()
    tg_uid = message.chat['id']
    mail_pack = class_mails.user_dailyMail(curr_time, tg_uid, sber_db)
    await message.answer(messages.process_task_button, reply_markup = markup_main_menu)
    print(mail_pack)
    for mail in mail_pack:
        if mail['tag'] == 'task':
            await bot.send_message(mail['tg_uid'], text='Message type: {}\nDay: {}\nTime: {}\nText: {}'.format(mail['tag'], mail['practice_day'], mail['letter_time'], mail['letter_text']))


#Кнопки FAQ
@dp.message_handler(regexp='^(Зарплата)\S*')
async def process_faq_salary1_button(message: types.Message):
    await message.answer(messages.process_faq_salary1_button, reply_markup = menu_buttons.markup_faq_menu)
    
@dp.message_handler(regexp='^(Зарплата - как и когда?)\S*')
async def process_faq_salary2_button(message: types.Message):
    await message.answer(messages.process_faq_salary2_button, reply_markup = menu_buttons.markup_faq_menu)
    
@dp.message_handler(regexp='^(Отпуск)\S*')
async def process_faq_vacation_button(message: types.Message):
    await message.answer(messages.process_faq_vacation_button, reply_markup = menu_buttons.markup_faq_menu)
    
@dp.message_handler(regexp='^(Практика)\S*')
async def process_faq_practice_button(message: types.Message):
    await message.answer(messages.process_faq_practice_button, reply_markup = menu_buttons.markup_faq_menu)
    
@dp.message_handler(regexp='^(Бронирование ТКС-ВКС)\S*')
async def process_faq_tks_button(message: types.Message):
    await message.answer(messages.process_faq_tks_button, reply_markup = menu_buttons.markup_faq_menu)
    
@dp.message_handler(regexp='^(Поменять часы работы)\S*')
async def process_faq_hours_button(message: types.Message):
    await message.answer(messages.process_faq_hours_button, reply_markup = menu_buttons.markup_faq_menu)
    
@dp.message_handler(regexp='^(Наши контакты для поддержки)\S*')
async def process_faq_contacts_button(message: types.Message):
    phone_num = '+79779999090'
    first_name = 'Иван'
    last_name = 'Иванов'
    await message.answer(messages.process_faq_contacts_button, reply_markup = menu_buttons.markup_faq_menu)
    await message.answer_contact(phone_num, first_name, last_name, reply_markup = menu_buttons.markup_faq_menu)

@dp.message_handler(regexp='^(В главное меню)\S*')
async def process_faq_back_button(message: types.Message):
    await message.answer(messages.process_faq_back_button, reply_markup = menu_buttons.markup_main_menu)
    

    