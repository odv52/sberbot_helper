from aiogram.dispatcher.filters.state import StatesGroup, State

class registerUser(StatesGroup):
    S1_name = State()
    S2_phone_num = State()
    S3_email = State()
    S4_finish = State()

class userRating(StatesGroup):
    S1_check_state = State()
    S2_check_rates_ammount = State()
    S3_rate = State()
    S4_ratetext = State()
    S5_finish = State()
    
class userInfo(StatesGroup):
    S1_name = State()
    S2_email = State()
    S3_area = State()
    S4_unit = State()
    S5_department = State()
    S6_mentor = State()
    S7_finish = State()
   