from prefs import dp
from aiogram import types
from interface import messages
from interface import menu_buttons
from prefs import sber_db
from classes.class_userStates import registerUser
from classes.class_user import User
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
  
#Введем ФИО
@dp.message_handler(commands=['register'], state=None)
async def process_register_st0_command(message: types.Message):
    await message.answer(messages.process_register_st0_command, reply_markup = types.ReplyKeyboardRemove())
    await registerUser.S1_name.set()

#Введем номер телефона
@dp.message_handler(state=registerUser.S1_name)
async def process_register_st1_command(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"name": answer})
    await message.answer(messages.process_register_st1_command)
    await registerUser.S2_phone_num.set()
    
#Введем почту
@dp.message_handler(state=registerUser.S2_phone_num)
async def process_register_st2_command(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"phone_num": answer})
    await message.answer(messages.process_register_st2_command)
    await registerUser.S3_email.set()
    
#Введем табельный номер
@dp.message_handler(state=registerUser.S3_email)
async def process_register_st3_command(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"email": answer})
    await message.answer(messages.process_register_st3_command)
    await registerUser.S4_personnel_num.set()
    
#Проверка введенных данных 
@dp.message_handler(state=registerUser.S4_personnel_num)
async def process_register_st4_command(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"personnel_num": answer})
    data = await state.get_data()
    await message.answer('Спасибо за уделенное время!')
    await message.answer('Проверь свои ответы!\nФИО: {};\nНомер телефона: {};\nПочта: {}\nТабельный номер: {};'.format(data.get('name'), data.get('phone_num'), data.get('email'), data.get('personnel_num')))
    await message.answer('Введи /ok, если всё верно или /repeat, если хочешь исправить')
    await registerUser.S5_finish.set()
    
@dp.message_handler(commands=['ok'], state=registerUser.S5_finish)
async def process_register_ok_command(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user = User(sber_db)
    if user.register_new(data.get('name'), data.get('phone_num'), data.get('personnel_num'), data.get('email'), message.chat['username'], message.chat['id']):
        await message.answer('Регистрация окончена!', reply_markup = menu_buttons.markup_main_menu)
    else:
        await message.answer(messages.process_register_failed_command)
    await state.finish()
    
@dp.message_handler(commands=['repeat'], state=registerUser.S5_finish)
async def process_register_repeat_command(message: types.Message, state: FSMContext):
    await message.answer('Повторим еще раз, введи ФИО')
    await registerUser.S1_name.set()
