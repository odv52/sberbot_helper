from aiogram import types
from interface import messages
from interface import menu_buttons
from prefs import sber_db
from classes.class_userStates import userRating
from classes.class_user import User
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage



"""
Процесс оценивания:
1) Пользователь проверяется на статус авторизации (2)
2) Если всё ок, то переходит к этапу просмотра возможных голосований
3) Голосует
4) Подтверждает или меняет свое мнение


P.S. Если в статусе авторизации ошибка - предложение пройти опросник
"""


    # S1_check_state = State()
    # S2_check_rates_ammount = State()
    # S3_rate = State()
    # S4_ratetext = State()
    # S5_finish = State()

#Оценка ментора
@dp.message_handler(regexp='^(Оценка)\S*', state=None)
async def process_rate_st0_command(message: types.Message):
    await message.answer('Отлично, приступим!', reply_markup = types.ReplyKeyboardRemove())
    tg_uid = message.chat['id']
    user = User(sber_db)
    user.define(value = tg_uid, by_tg_uid = True)
    if user.def_userdata['auth_status'] == 2:
        await message.answer(messages.process_rate_st0_command, reply_markup = types.ReplyKeyboardRemove())
        await userRating.S1_check_state.set()
    else:
        await message.answer(messages.process_rate_st0_error, reply_markup = menu_buttons.markup_main_menu)


@dp.message_handler(state=userRating.S1_check_state)
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
            await message.answer('Доступных голосований нет', reply_markup = menu_buttons.markup_main_menu)
        await rateMentor.S2_check_rates_ammount.set()
    else:
        await message.answer(bot_messages.raise_error_rate_mentor_check)
        await message.answer('Ты ввёл ФИО ментора: {}\nВ базе данных указано, что твой ментор: {}'.format(data.get('user_mentor'), data.get('db_mentor')), reply_markup = menu_buttons.markup_main_menu)
        await state.finish()
    
@dp.message_handler(state=rateMentor.S2_check_rates_ammount)
async def process_rate_amount(message: types.Message, state: FSMContext):
    answer = message.text
    answer = re.findall(r'.(\d+)', answer)
    await state.update_data({"code": answer[0]})
    data = await state.get_data()
    await message.answer('Отлично. Отметь кнопками ниже по шкале от 1 до 5, как бы ты ответил на вопрос?', reply_markup = menu_buttons.markup_rate_menu)
    await rateMentor.S3_rate.set()    
    
@dp.message_handler(state=rateMentor.S3_rate)
async def process_rate_mark(message: types.Message, state: FSMContext):
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
        await message.answer('Результат успешно записан, спасибо!', reply_markup = menu_buttons.markup_main_menu)
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