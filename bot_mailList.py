import datetime
import sqlite3
from bot_requests import get_user_day, get_user_status

def get_users(auth_state = 1):
    conn = sqlite3.connect("db\sberbot.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT * FROM userList 
                       WHERE is_authorised=?""", (auth_state, ))
        result = cursor.fetchall()
        user_list = []
        for element in result:
            user = {}
            user['personal_number'] = element[0]
            user['user_lastname'] = element[1]
            user['user_firstname'] = element[2]
            user['user_middlename'] = element[3]
            user['is_authorised'] = element[4]
            user['phone_number'] = element[5]
            user['username'] = element[6]
            user['user_id'] = element[7]
            user['date_start'] = element[8]
            user['date_end'] = element[9]
            user['mentor'] = element[10]
            user_list.append(user)
        conn.close()
        return user_list
    except:
        conn.close()
        return 0


def get_daily_mail(user_id, day, conn, cursor):
    cursor.execute("""SELECT * FROM mailList 
                WHERE practice_day=?""", (int(day), ))
    result = cursor.fetchall()
    mail_list = []
    for element in result:
        letter = {}
        letter['user_id'] = user_id
        letter['letter_id'] = int(element[0])
        letter['practice_day'] = element[1]
        letter['letter_time'] = element[2]
        letter['tag'] = element[3]
        letter['letter_text'] = element[4]
        mail_list.append(letter)
    return mail_list
    
    
def user_mailToSend(curr_datetime):
    conn = sqlite3.connect("db\sberbot.db")
    cursor = conn.cursor()
    user_list = get_users()
    mail_pack = []
    lines_to_add = []
    receive_status = 1
    for element in user_list:
        user_start_date = datetime.datetime.strptime(element['date_start'], '%d.%m.%Y')
        user_day = get_user_day(user_start_date, curr_datetime)
        user_status = get_user_status(element['user_id'], user_day)
        if user_status and user_status['is_received_letters'] == 1:
            pass
        else:
            cursor.execute("""INSERT INTO userStateList(
                                user_id, user_day, is_received_letters
                                ) VALUES (?, ?, ?)
                                """, (element['user_id'], user_day, receive_status))
            
            user_mail = get_daily_mail(element['user_id'], user_day, conn, cursor)
            mail_pack.append(user_mail)

        
#Добавить UPDATE
    conn.commit()
    conn.close()
    return mail_pack
