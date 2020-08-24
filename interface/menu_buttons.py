from aiogram import types
from aiogram.utils.emoji import emojize

#Инициализация меню регистрации
register_button_help = types.KeyboardButton(emojize('Помощь :loudspeaker:'))
markup_register_menu = types.ReplyKeyboardMarkup(resize_keyboard=True).row(register_button_help)

#Инициализация главного меню
main_button_info = types.KeyboardButton(emojize('Информация :clipboard:'))
main_button_faq = types.KeyboardButton(emojize('FAQ :question:'))
main_button_task = types.KeyboardButton(emojize('Задачи :pushpin:'))
main_button_mark = types.KeyboardButton(emojize('Оценка :100:'))
main_button_settings = types.KeyboardButton(emojize('Настройки :wrench:'))
markup_main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True).row(main_button_faq, main_button_settings).row(main_button_task, main_button_mark, main_button_info)

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
rate_button_1 = types.KeyboardButton(emojize('1 из 5'))
rate_button_2 = types.KeyboardButton(emojize('2 из 5'))
rate_button_3 = types.KeyboardButton(emojize('3 из 5'))
rate_button_4 = types.KeyboardButton(emojize('4 из 5'))
rate_button_5 = types.KeyboardButton(emojize('5 из 5'))
markup_rate_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(rate_button_1, rate_button_2).row(rate_button_3, rate_button_4).row(rate_button_5)
