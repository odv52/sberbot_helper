from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import time
import datetime
import bot_messages
import logging
import bot_db_loadFromBot as db
import re
from bot_userStates import registerUser, rateMentor
from bot_mailList import user_mailToSend, user_getAllMails
from bot_requests import get_user_info, get_user_status, get_user_rate_state

#Конфигурация библиотеки
config = dict()
with open('settings.ini') as settings:
    for line in settings:
        curr_line = line.split()
        config[curr_line[0]] = curr_line[2]

API_TOKEN = config['TOKEN']

#Конфигурация логгирования
logging.basicConfig(level=logging.INFO)

#Инициализация бота и диспетчера
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


#Инициализация меню регистрации
register_button_help = types.KeyboardButton(emojize('Помощь :loudspeaker:'))
markup_register_menu = types.ReplyKeyboardMarkup(resize_keyboard=True).row(register_button_help)

#Инициализация главного меню
main_button_info = types.KeyboardButton(emojize('Информация :clipboard:'))
main_button_faq = types.KeyboardButton(emojize('FAQ :question:'))
main_button_task = types.KeyboardButton(emojize('Задачи :pushpin:'))
main_button_mark = types.KeyboardButton(emojize('Оценка :100:'))
markup_main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True).row(main_button_info, main_button_faq).row(main_button_task, main_button_mark)

#Инициализация меню FAQ
faq_button_salary1 = types.KeyboardButton(emojize('Зарплата :moneybag:'))
faq_button_salary2 = types.KeyboardButton(emojize('Зарплата - как и когда? :date:'))
faq_button_vacation = types.KeyboardButton(emojize('Отпуск :sunny:'))
faq_button_practice = types.KeyboardButton(emojize('Практика :computer:'))
faq_button_tks = types.KeyboardButton(emojize('Бронирование ТКС-ВКС :unlock:'))
faq_button_hours = types.KeyboardButton(emojize('Поменять часы работы :clock4:'))
faq_button_contacts = types.KeyboardButton(emojize('Наши контакты для поддержки :phone:'))
faq_button_back = types.KeyboardButton(emojize('В главное меню :arrow_heading_up:'))
markup_faq_menu = types.ReplyKeyboardMarkup(resize_keyboard=True).row(faq_button_salary1, faq_button_salary2).row(faq_button_practice, faq_button_tks).row(faq_button_vacation, faq_button_hours).row(faq_button_contacts, faq_button_back)

#Инициализация меню оценки ментора
star_button_1 = types.KeyboardButton(emojize('1 из 5'))
star_button_2 = types.KeyboardButton(emojize('2 из 5'))
star_button_3 = types.KeyboardButton(emojize('3 из 5'))
star_button_4 = types.KeyboardButton(emojize('4 из 5'))
star_button_5 = types.KeyboardButton(emojize('5 из 5'))
markup_star_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(star_button_1, star_button_2).row(star_button_3, star_button_4).row(star_button_5)


#Переместить сюда хендлер на отлов сообщений, если захочу сохранять
#Запланированные сообщения

async def scheduled(wait_for):
    while True:
        curr_time = datetime.datetime.now()
        await asyncio.sleep(wait_for)
        mail_pack = user_mailToSend(curr_time, by_hour = True)
        for mail in mail_pack:
            await bot.send_message(mail['user_id'], 'Message type: {}\nDay: {}\nTime: {}\nText: {}'.format(mail['tag'], mail['practice_day'], mail['letter_time'], mail['letter_text']))                



#Команды
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer(bot_messages.process_start_command, reply_markup = markup_main_menu)
    
@dp.message_handler(regexp='^(user_info)\S*')
async def process_start_command(message: types.Message):
    info_id = message.text
    info_id = re.findall(r'^user_info (\d+)', info_id)
    answer = get_user_info(personal_number = info_id[0], format_message = True)
    await message.answer(answer, reply_markup = markup_main_menu)
    
@dp.message_handler(commands=['register'])
async def process_register_command(message: types.Message):
    await message.answer(bot_messages.process_register_command, reply_markup = markup_register_menu)
    
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    
    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await message.reply('Cancelled.', reply_markup = markup_main_menu)
    
@dp.message_handler(commands=['dev_msgs'])
async def process_start_command(message: types.Message):
    mail_pack = user_getAllMails(message.chat['id'], write_to_db = True)
    for mail in mail_pack:
        await bot.send_message(mail['user_id'], 'Message type: {}\nDay: {}\nTime: {}\nText: {}'.format(mail['tag'], mail['practice_day'], mail['letter_time'], mail['letter_text']))  
    
    
#Регистрация
@dp.message_handler(regexp='^(Помощь)\S*')
async def process_register_help_button(message: types.Message):
    phone_num = '+79779999090'
    first_name = 'Иван'
    last_name = 'Иванов'
    await message.answer(bot_messages.process_register_help_button)
    await message.answer_contact(phone_num, first_name, last_name, reply_markup = markup_main_menu)

@dp.message_handler(commands=['regproc'], state=None)
async def process_register_enter_command(message: types.Message):
    await message.answer(bot_messages.process_register_persnum_command, reply_markup = types.ReplyKeyboardRemove())
    await registerUser.S1_personal_number.set()
    
@dp.message_handler(state=registerUser.S1_personal_number)
async def process_register_persnum_command(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"personal_number": answer})
    await message.answer(bot_messages.process_register_names_command)
    await registerUser.S2_names.set()

@dp.message_handler(state=registerUser.S2_names)
async def process_register_names_command(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"names": answer})
    await message.answer(bot_messages.process_register_phone_command)
    await registerUser.S3_phone.set()
    
@dp.message_handler(state=registerUser.S3_phone)
async def process_register_phone_command(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"phone": answer})
    data = await state.get_data()
    await message.answer('Спасибо за уделенное время!')
    await message.answer('Проверь свои ответы!\nТабельный номер: {};\nФИО: {};\nНомер телефона: {};\n'.format(data.get('personal_number'), data.get('names'), data.get('phone')))
    await message.answer('Введи /ok, если всё верно и /repeat, если есть ошибка')
    await registerUser.S4_finish.set()

@dp.message_handler(commands=['ok'], state=registerUser.S4_finish)
async def process_register_ok_command(message: types.Message, state: FSMContext):
    data = await state.get_data()
    trigger = db.register_user(data.get('personal_number'), data.get('names'), data.get('phone'), message.chat['id'], message.chat['username'])
    if trigger == 1:
        await message.answer('Регистрация окончена!', reply_markup = markup_main_menu)
    else:
        await message.answer(bot_messages.process_register_failed_command)
    await state.finish()
    
@dp.message_handler(commands=['repeat'], state=registerUser.S4_finish)
async def process_register_repeat_command(message: types.Message, state: FSMContext):
    await message.answer('Повторим еще раз, введите табельный номер')
    await registerUser.S1_personal_number.set()


#Оценка ментора
@dp.message_handler(regexp='^(Оценка)\S*', state=None)
async def process_rate_start(message: types.Message):
    await message.answer('Отлично, приступим!', reply_markup = types.ReplyKeyboardRemove())
    user_id = message.chat['id']
    user_info = get_user_info(user_id = user_id)
    if user_info['is_authorised']:
        await message.answer(bot_messages.process_rate_start, reply_markup = types.ReplyKeyboardRemove())
        await rateMentor.S1_check_mentor.set()
    else:
        await message.answer(bot_messages.raise_error_rate_start, reply_markup = markup_main_menu)
        await state.finish()

@dp.message_handler(state=rateMentor.S1_check_mentor)
async def process_rate_mentor_check(message: types.Message, state: FSMContext):
    answer = message.text
    user_id = message.chat['id']
    user_info = get_user_info(user_id = user_id)
    db_mentor = user_info['mentor']
    await state.update_data({"db_mentor": db_mentor})
    await state.update_data({"user_mentor": answer})
    data = await state.get_data()
    if data.get('user_mentor') == data.get('db_mentor'):
        rate_list = get_user_rate_state(user_id)
        print(rate_list)
        msg = ''
        if rate_list:
            for element in rate_list:
                msg += 'День голосования: {}\nЗадача голосования: {}\nКод голосования для продолжения: {}\n\n'.format(element['user_day'], element['rate_header'], element['message_code'])
        if msg:
            await message.answer(msg)
        else:
            await message.answer('Доступных голосований нет', reply_markup = markup_main_menu)
        await rateMentor.S2_check_rates_ammount.set()
    else:
        await message.answer(bot_messages.raise_error_rate_mentor_check)
        await message.answer('Ты ввёл ФИО ментора: {}\nВ базе данных указано, что твой ментор: {}'.format(data.get('user_mentor'), data.get('db_mentor')), reply_markup = markup_main_menu)
        await state.finish()
    
@dp.message_handler(state=rateMentor.S2_check_rates_ammount)
async def process_rate_amount(message: types.Message, state: FSMContext):
    answer = message.text
    answer = re.findall(r'.(\d+)', answer)
    await state.update_data({"code": answer[0]})
    data = await state.get_data()
    await message.answer('Отлично. Отметь кнопками ниже по шкале от 1 до 5, как бы ты ответил на вопрос?', reply_markup = markup_star_menu)
    await rateMentor.S3_rate.set()    
    
@dp.message_handler(state=rateMentor.S3_rate)
async def process_rate_stars(message: types.Message, state: FSMContext):
    answer = message.text
    answer = re.findall(r'(\d) из \d', answer)
    await state.update_data({"rate": answer[0]})
    data = await state.get_data()
    await message.answer('Спасибо за оценку [{}/5]! Оставь, пожалуйста, пару слов об ощущениях или пожеланиях'.format(data.get('rate')), reply_markup = types.ReplyKeyboardRemove())
    await rateMentor.S4_ratetext.set()
    
@dp.message_handler(state=rateMentor.S4_ratetext)
async def process_rate_finish(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"rate_text": answer})
    data = await state.get_data()
    await message.answer('Спасибо за уделенное время!')
    await message.answer('Проверь свои ответы!\nФИО ментора: {};\nОценка: {};\nТекст к оценке: {};\nКод голосования: {};'.format(data.get('user_mentor'), data.get('rate'), data.get('rate_text'), data.get('code')))
    await message.answer('Введи /ok, если всё верно и /repeat, если есть ошибка')
    await rateMentor.S5_finish.set()

@dp.message_handler(commands=['ok'], state=rateMentor.S5_finish)
async def process_rate_ok_command(message: types.Message, state: FSMContext):
    data = await state.get_data()
    curr_datetime = datetime.datetime.now()
    trigger = db.save_rate_to_db(message.chat['id'], data.get('rate'), data.get('rate_text'), curr_datetime, data.get('code'))
    if trigger == 1:
        await message.answer('Результат успешно записан, спасибо!', reply_markup = markup_main_menu)
    else:
        await message.answer('Ошибка регистрации данных, попробуй еще раз или обратись за помощью')
    await state.finish()
    
@dp.message_handler(commands=['repeat'], state=rateMentor.S5_finish)
async def process_rate_repeat_command(message: types.Message, state: FSMContext):
    await message.answer('Повторим еще раз, введи имя ментора :)')
    await rateMentor.S1_check_mentor.set()

# @dp.message_handler(state=rateMentor.S2_rate)
# async def process_rate_finish(message: types.Message, state: FSMContext):
#     answer = message.text
#     await state.update_data({"rate": answer})
#     await message.answer(bot_messages.process_rate_finish)
#     await rateMentor.S3_finish.set()
    

#Кнопки главного меню
@dp.message_handler(regexp='^(FAQ)\S*')
async def process_faq_button(message: types.Message):
    await message.answer(bot_messages.process_faq_button, reply_markup = markup_faq_menu)

@dp.message_handler(regexp='^(Информация)\S*')
async def process_info_button(message: types.Message):
    document = config['SBER_INFO_ID']
    await message.answer_document(document, bot_messages.process_info_button, reply_markup = markup_main_menu)

@dp.message_handler(regexp='^(Задачи)\S*')
async def process_task_button(message: types.Message):
    curr_time = datetime.datetime.now()
    mail_pack = user_mailToSend(curr_time, by_hour = False)
    await message.answer(bot_messages.process_task_button, reply_markup = markup_main_menu)
    print(mail_pack)
    for mail in mail_pack:
        await bot.send_message(mail['user_id'], 'Message type: {}\nDay: {}\nTime: {}\nText: {}'.format(mail['tag'], mail['practice_day'], mail['letter_time'], mail['letter_text']))

    
#Кнопки FAQ
@dp.message_handler(regexp='^(Зарплата)\S*')
async def process_faq_salary1_button(message: types.Message):
    await message.answer(bot_messages.process_faq_salary1_button, reply_markup = markup_faq_menu)
    
@dp.message_handler(regexp='^(Зарплата - как и когда?)\S*')
async def process_faq_salary2_button(message: types.Message):
    await message.answer(bot_messages.process_faq_salary2_button, reply_markup = markup_faq_menu)
    
@dp.message_handler(regexp='^(Отпуск)\S*')
async def process_faq_vacation_button(message: types.Message):
    await message.answer(bot_messages.process_faq_vacation_button, reply_markup = markup_faq_menu)
    
@dp.message_handler(regexp='^(Практика)\S*')
async def process_faq_practice_button(message: types.Message):
    await message.answer(bot_messages.process_faq_practice_button, reply_markup = markup_faq_menu)
    
@dp.message_handler(regexp='^(Бронирование ТКС-ВКС)\S*')
async def process_faq_tks_button(message: types.Message):
    await message.answer(bot_messages.process_faq_tks_button, reply_markup = markup_faq_menu)
    
@dp.message_handler(regexp='^(Поменять часы работы)\S*')
async def process_faq_hours_button(message: types.Message):
    await message.answer(bot_messages.process_faq_hours_button, reply_markup = markup_faq_menu)
    
@dp.message_handler(regexp='^(Наши контакты для поддержки)\S*')
async def process_faq_contacts_button(message: types.Message):
    phone_num = '+79779999090'
    first_name = 'Иван'
    last_name = 'Иванов'
    await message.answer(bot_messages.process_faq_contacts_button, reply_markup = markup_faq_menu)
    await message.answer_contact(phone_num, first_name, last_name, reply_markup = markup_faq_menu)

@dp.message_handler(regexp='^(В главное меню)\S*')
async def process_faq_back_button(message: types.Message):
    await message.answer(bot_messages.process_faq_back_button, reply_markup = markup_main_menu)
    
    
#Реакции на звезды
@dp.message_handler(lambda message: message.text and emojize(':star::anger::anger::anger::anger:') in message.text)
async def process_star_1_button(message: types.Message):
    await message.answer(bot_messages.process_star_1_button, reply_markup = markup_main_menu)

@dp.message_handler(lambda message: message.text and emojize(':star::star::anger::anger::anger:') in message.text)
async def process_star_2_button(message: types.Message):
    await message.answer(bot_messages.process_star_2_button, reply_markup = markup_main_menu)

@dp.message_handler(lambda message: message.text and emojize(':star::star::star::anger::anger:') in message.text)
async def process_star_3_button(message: types.Message):
    await message.answer(bot_messages.process_star_3_button, reply_markup = markup_main_menu)

@dp.message_handler(lambda message: message.text and emojize(':star::star::star::star::anger:') in message.text)
async def process_star_4_button(message: types.Message):
    await message.answer(bot_messages.process_star_4_button, reply_markup = markup_main_menu)

@dp.message_handler(lambda message: message.text and emojize(':star::star::star::star::star:') in message.text)
async def process_star_5_button(message: types.Message):
    await message.answer(bot_messages.process_star_5_button, reply_markup = markup_main_menu)
    
    
#Хендлер на отлов сообщений, которые не попали выше
@dp.message_handler(state=None)
async def process_start_command(message: types.Message):
    print('\nDate: {};\nText: {};\nMessage ID: {};\nMessage chat: {};\n'.format(message.date, message.text, message.message_id, message.chat))
    await bot.send_message(message.chat['id'], 'Я получил и сохранил твое сообщение, {}!'.format(message.chat['first_name']))
    db.save_msg_to_db(message.chat['username'], message.date, message.text, message.message_id, message.chat['id'])
    
if __name__ == '__main__':
    dp.loop.create_task(scheduled(5))
    executor.start_polling(dp, skip_updates=True)
    
    
    
# Получаем ID файла
# msg = await bot.send_document(message.chat.id, document, None)
# await bot.send_message(message.chat.id, msg.document.file_id, reply_to_message_id=msg.message_id)
