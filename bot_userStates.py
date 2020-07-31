from aiogram.dispatcher.filters.state import StatesGroup, State

class registerUser(StatesGroup):
    S1_personal_number = State()
    S2_names = State()
    S3_phone = State()
    S4_finish = State()