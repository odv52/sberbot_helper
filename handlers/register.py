  
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
    await message.answer(bot_messages.process_register_mentor_command)
    await registerUser.S4_mentor.set()
    
@dp.message_handler(state=registerUser.S4_mentor)
async def process_register_mentor_command(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"mentor": answer})
    data = await state.get_data()
    await message.answer('Спасибо за уделенное время!')
    await message.answer('Проверь свои ответы!\nТабельный номер: {};\nФИО: {};\nНомер телефона: {};\nФИО ментора: {};\n'.format(data.get('personal_number'), data.get('names'), data.get('phone'), data.get('mentor')))
    await message.answer('Введи /ok, если всё верно и /repeat, если есть ошибка')
    await registerUser.S5_finish.set()
    
@dp.message_handler(commands=['ok'], state=registerUser.S5_finish)
async def process_register_ok_command(message: types.Message, state: FSMContext):
    data = await state.get_data()
    trigger = db.register_user(data.get('personal_number'), data.get('names'), data.get('phone'), data.get('mentor'), message.chat['id'], message.chat['username'])
    if trigger == 1:
        await message.answer('Регистрация окончена!', reply_markup = markup_main_menu)
    else:
        await message.answer(bot_messages.process_register_failed_command)
    await state.finish()
    
@dp.message_handler(commands=['repeat'], state=registerUser.S5_finish)
async def process_register_repeat_command(message: types.Message, state: FSMContext):
    await message.answer('Повторим еще раз, введите табельный номер')
    await registerUser.S1_personal_number.set()
