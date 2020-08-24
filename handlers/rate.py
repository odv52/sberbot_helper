
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
    await message.answer('Отлично. Отметь кнопками ниже по шкале от 1 до 5, как бы ты ответил на вопрос?', reply_markup = markup_rate_menu)
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