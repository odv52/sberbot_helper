








# import schedule
# import time
# import bot_db_loadFromBot as db 
# import threading
# import asyncio
# from main import send_sheduled_msg

# def job1():
#     user_list = db.list_users(1)
#     text = 'Привет! Сработал Job_1'
#     for user in user_list:
#         user_id = user[7]
#         print('JOB', user_id, text)
#         send_sheduled_msg(user_id, text)

# def job2():
#     user_list = db.list_users(1)
#     text = 'Привет! Сработал Job_2'
#     for user in user_list:
#         chat_id = user[7]
#         send_sheduled_msg(chat_id, text)

# def job3():
#     user_list = db.list_users(1)
#     text = 'Привет! Сработал Job_3'
#     for user in user_list:
#         chat_id = user[7]
#         send_sheduled_msg(chat_id, text)
        
# def run_scheduled():
#     schedule.every(0.5).minutes.do(job1)
#     schedule.every(3).to(5).minutes.do(job2)
#     schedule.every().day.at("00:45").do(job3)

#     while True: 
#         schedule.run_pending() 
#         asyncio.sleep(.05)
       
# sch_func = threading.Thread(target=run_scheduled)
# sch_func.start()



# # await bot.send_message(message.chat.id, msg.document.file_id, reply_to_message_id=msg.message_id)