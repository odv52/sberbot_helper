from aiogram.dispatcher.filters.state import StatesGroup, State

class registerUser(StatesGroup):
    S1_personal_number = State()
    S2_names = State()
    S3_phone = State()
    S4_mentor = State()
    S5_finish = State()

class userRating(StatesGroup):
    S1_check_mentor = State()
    S2_check_rates_ammount = State()
    S3_rate = State()
    S4_ratetext = State()
    S5_finish = State()
