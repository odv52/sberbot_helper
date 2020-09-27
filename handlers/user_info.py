from prefs import dp
from aiogram import types
from interface import messages
from interface import menu_buttons
from prefs import sber_db
from classes.class_userStates import userInfo
from classes.class_user import User
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

#Введем ФИО
@dp.message_handler(commands=['fill_info'], state=None)
async def process_uinfo_st0_command(message: types.Message):
    await message.answer(messages.process_uinfo_st0_command, reply_markup = types.ReplyKeyboardRemove())
    await userInfo.S1_name.set()

#Введем почту
@dp.message_handler(state=userInfo.S1_name)
async def process_uinfo_st1_command(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"name": answer})
    await message.answer(messages.process_uinfo_st1_command)
    await userInfo.S2_email.set()
   
#Введем направление
@dp.message_handler(state=userInfo.S2_email)
async def process_uinfo_st2_command(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"email": answer})
    await message.answer(messages.process_uinfo_st2_command)
    await userInfo.S3_area.set()

#Введем блок    
@dp.message_handler(state=userInfo.S3_area)
async def process_uinfo_st3_command(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"area": answer})
    await message.answer(messages.process_uinfo_st3_command)
    await userInfo.S4_unit.set()

#Введем департамент
@dp.message_handler(state=userInfo.S4_unit)
async def process_uinfo_st4_command(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"unit": answer})
    await message.answer(messages.process_uinfo_st4_command)
    await userInfo.S5_department.set()

#Введем ФИО ментора   
@dp.message_handler(state=userInfo.S5_department)
async def process_uinfo_st5_command(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"department": answer})
    await message.answer(messages.process_uinfo_st5_command)
    await userInfo.S6_mentor.set()
       
#Проверка введенных данных 
@dp.message_handler(state=userInfo.S6_mentor)
async def process_register_st3_command(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"mentor": answer})
    data = await state.get_data()
    await message.answer('Спасибо за уделенное время!')
    await message.answer(
    '''
    Проверь свои ответы!\n
    ФИО: {};\n
    Почта: {};\n
    Направление: {};\n
    Блок: {};\n
    Департамент: {};\n  
    ФИО ментора: {};\n 
    '''.format(data.get('name'), data.get('email'), data.get('napravl'), data.get('block'), data.get('department'), data.get('mentor')))
    await message.answer('Введи /ok, если всё верно или /repeat, если хочешь исправить')
    await userInfo.S7_finish.set()
    
@dp.message_handler(commands=['ok'], state=userInfo.S7_finish)
async def process_register_ok_command(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user = User(sber_db)
    if user.register_new(data.get('name'), data.get('phone_num'), data.get('personnel_num'), data.get('email'), message.chat['username'], message.chat['id']):
        await message.answer('Регистрация окончена!', reply_markup = menu_buttons.markup_main_menu)
    else:
        await message.answer(messages.process_register_failed_command)
    await state.finish()
    
@dp.message_handler(commands=['repeat'], state=userInfo.S7_finish)
async def process_register_repeat_command(message: types.Message, state: FSMContext):
    await message.answer('Повторим еще раз, введи ФИО')
    await userInfo.S1_name.set()