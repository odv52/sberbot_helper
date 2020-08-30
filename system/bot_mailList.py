import datetime
import sqlite3
from bot_requests import get_user_day, get_user_status

def get_users(auth_state = 1, user_id = 0):
    conn = sqlite3.connect("db\sberbot.db")
    cursor = conn.cursor()
    try:
        if user_id:
            cursor.execute("""SELECT * FROM userList 
                        WHERE is_authorised=? AND user_id=?""", (auth_state, user_id))
        else:
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


# def get_mail(user_id, day, conn, cursor, curr_time = -1, dayTo = False):
#     if curr_time == -1 and dayTo == False:
#         cursor.execute("""SELECT * FROM mailList 
#             WHERE practice_day=?""", (int(day), ))
#     elif dayTo:
#         cursor.execute("""SELECT * FROM mailList 
#             WHERE practice_day<=?""", (int(day), ))
#     else:
#         cursor.execute("""SELECT * FROM mailList 
#             WHERE practice_day=? AND letter_time=?""", (int(day), int(curr_time)))  
    
#     result = cursor.fetchall()
#     mail_list = []
#     for element in result:
#         letter = {}
#         letter['user_id'] = user_id
#         letter['letter_id'] = int(element[0])
#         letter['practice_day'] = element[1]
#         letter['letter_time'] = int(element[2])
#         letter['tag'] = element[3]
#         letter['letter_text'] = element[4]
#         mail_list.append(letter)
#     return mail_list
    
    
def user_mailToSend(curr_datetime, by_hour = True):
    conn = sqlite3.connect("db\sberbot.db")
    cursor = conn.cursor()
    user_list = get_users()
    mail_pack = []
    lines_to_add = []
    for element in user_list:
        user_start_date = datetime.datetime.strptime(element['date_start'], '%d.%m.%Y')
        user_day = get_user_day(user_start_date, curr_datetime)
        user_time = curr_datetime.hour
        if by_hour:
            user_status = get_user_status(element['user_id'], user_day, user_time)
        else:
            user_status = False
        if user_status:
            pass
        else:
            if by_hour:
                user_mail = get_mail(element['user_id'], user_day, conn, cursor, user_time)
            else:
                user_mail = get_mail(element['user_id'], user_day, conn, cursor)
            if user_mail:
                for element in user_mail:
                    mail_pack.append(element)
                    if by_hour:
                        cursor.execute("""INSERT INTO userStateList(
                                        user_id, user_day, letter_id, letter_time, tag, is_sent
                                        ) VALUES (?, ?, ?, ?, ?, ?)
                                        """, (element['user_id'], user_day, element['letter_id'], element['letter_time'], element['tag'], 1))
                        if element['tag'] == 'rate':
                            cursor.execute("""INSERT INTO userRateStateList(
                                        operation_date, rate_header, user_id, user_day
                                        ) VALUES (?, ?, ?, ?)
                                        """, (curr_datetime, element['letter_text'], element['user_id'], user_day))
        
    conn.commit()
    conn.close()
    return mail_pack
                            
                            
def user_getAllMails(user_id, write_to_db = False):
    conn = sqlite3.connect("db\sberbot.db")
    cursor = conn.cursor()
    curr_datetime = datetime.datetime.now()
    user_data = get_users(user_id = user_id)
    mail_pack = []
    lines_to_add = []
    print('User data', user_data)
    for element in user_data:
        user_start_date = datetime.datetime.strptime(element['date_start'], '%d.%m.%Y')
        user_day = get_user_day(user_start_date, curr_datetime)
        user_time = curr_datetime.hour
        user_mail = get_mail(element['user_id'], user_day, conn, cursor, dayTo = True)
        sent_messages = get_user_status(element['user_id'], user_day, dayTo = True)
        print('element', element)
        print('user_mail', user_mail)
        print('sent_messages data', sent_messages)
        if user_mail:
            if write_to_db:
                for element in user_mail:
                    mail_pack.append(element)
                    if element['letter_id'] not in sent_messages:
                        cursor.execute("""INSERT INTO userStateList(
                                        user_id, user_day, letter_id, letter_time, tag, is_sent
                                        ) VALUES (?, ?, ?, ?, ?, ?)
                                        """, (element['user_id'], element['practice_day'], element['letter_id'], element['letter_time'], element['tag'], 1))
                        if element['tag'] == 'rate':
                            cursor.execute("""INSERT INTO userRateStateList(
                                        operation_date, rate_header, user_id, user_day
                                        ) VALUES (?, ?, ?, ?)
                                        """, (curr_datetime, element['letter_text'], element['user_id'], element['practice_day']))
            else:
                for element in user_mail: 
                    mail_pack.append(element)

    conn.commit()
    conn.close()
    return mail_pack