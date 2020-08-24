#Хендлер на отлов сообщений, которые не попали выше
@dp.message_handler(state=None)
async def process_start_command(message: types.Message):
    print('\nDate: {};\nText: {};\nMessage ID: {};\nMessage chat: {};\n'.format(message.date, message.text, message.message_id, message.chat))
    await bot.send_message(message.chat['id'], 'Я получил и сохранил твое сообщение, {}!'.format(message.chat['first_name']))
    db.save_msg_to_db(message.chat['username'], message.date, message.text, message.message_id, message.chat['id'])
    
