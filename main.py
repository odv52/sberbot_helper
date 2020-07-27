from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram import Bot, Dispatcher, types
from aiogram.utils.emoji import emojize
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import aiogram.utils.markdown as md
import bot_messages
import logging
import bot_db_loadFromBot as db
from bot_registerUserStates import RegisterUser

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
star_button_1 = types.KeyboardButton(emojize(':star::anger::anger::anger::anger:'))
star_button_2 = types.KeyboardButton(emojize(':star::star::anger::anger::anger:'))
star_button_3 = types.KeyboardButton(emojize(':star::star::star::anger::anger:'))
star_button_4 = types.KeyboardButton(emojize(':star::star::star::star::anger:'))
star_button_5 = types.KeyboardButton(emojize(':star::star::star::star::star:'))
markup_star_menu = types.ReplyKeyboardMarkup(resize_keyboard=True).row(star_button_1, star_button_2).row(star_button_3, star_button_4).row(star_button_5)


#Переместить сюда хендлер на отлов сообщений, если захочу сохранять

#Команды
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer(bot_messages.process_start_command, reply_markup = markup_main_menu)
    
@dp.message_handler(commands=['register'])
async def process_register_command(message: types.Message):
    await message.answer(bot_messages.process_register_command, reply_markup = markup_register_menu)
    
    
#Регистрация
@dp.message_handler(regexp='^(Помощь)\S*')
async def process_register_help_button(message: types.Message):
    phone_num = '+79779999090'
    first_name = 'Иван'
    last_name = 'Иванов'
    await message.answer(bot_messages.process_register_help_button, reply_markup = markup_register_menu)
    await message.answer_contact(phone_num, first_name, last_name, reply_markup = markup_register_menu)

@dp.message_handler(commands=['regproc'], state=None)
async def process_register_enter_command(message: types.Message):
    await message.answer(bot_messages.process_register_persnum_command, reply_markup = types.ReplyKeyboardRemove())
    await RegisterUser.S1_personal_number.set()
    
@dp.message_handler(state=RegisterUser.S1_personal_number)
async def process_register_persnum_command(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"personal_number": answer})
    await message.answer(bot_messages.process_register_names_command)
    await RegisterUser.S2_names.set()

@dp.message_handler(state=RegisterUser.S2_names)
async def process_register_names_command(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"names": answer})
    await message.answer(bot_messages.process_register_phone_command)
    await RegisterUser.S3_phone.set()
    
@dp.message_handler(state=RegisterUser.S3_phone)
async def process_register_phone_command(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"phone": answer})
    data = await state.get_data()
    await message.answer('Спасибо за уделенное время!')
    await message.answer('Проверьте ваши ответы!\nТабельный номер: {};\nФИО: {};\nНомер телефона: {};\n'.format(data.get('personal_number'), data.get('names'), data.get('phone')))
    await message.answer('Введите /ok, если всё верно и /repeat, если ошиблись')
    await RegisterUser.S4_finish.set()

@dp.message_handler(commands=['ok'], state=RegisterUser.S4_finish)
async def process_register_ok_command(message: types.Message, state: FSMContext):
    data = await state.get_data()
    trigger = db.register_user(data.get('personal_number'), data.get('names'), data.get('phone'), message.chat['id'], message.chat['username'])
    if trigger == 1:
        await message.answer('Регистрация окончена!')
    else:
        await message.answer(process_register_failed_command)
    await state.finish()
    
@dp.message_handler(commands=['repeat'], state=RegisterUser.S4_finish)
async def process_register_repeat_command(message: types.Message, state: FSMContext):
    await message.answer('Повторим еще раз, введите табельный номер')
    await RegisterUser.S1_personal_number.set()
    

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
    await message.answer(bot_messages.process_task_button, reply_markup = markup_main_menu)
    
@dp.message_handler(regexp='^(Оценка)\S*')
async def process_star_button(message: types.Message):
    await message.answer(bot_messages.process_star_button, reply_markup = markup_star_menu)
    
    
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
    db.save_msg_to_db(message.chat['username'], message.date, message.text, message.message_id, message.chat['id'], message.chat['first_name'], message.chat['last_name'])
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    
    
    
# Получаем ID файла
# msg = await bot.send_document(message.chat.id, document, None)
# await bot.send_message(message.chat.id, msg.document.file_id, reply_to_message_id=msg.message_id)
