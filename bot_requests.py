import sqlite3
import datetime

def get_user_day(start_date, curr_date):
    return (int((curr_date - start_date).days) + 1)


def get_user_status(user_id, user_day, hour = -1, dayTo = False):
    conn = sqlite3.connect("db\sberbot.db")
    cursor = conn.cursor()
    try:
        if hour == -1 and dayTo == False:
            cursor.execute("""SELECT * FROM userStateList 
                            WHERE user_id=? AND user_day=?""", (user_id, user_day))
        elif dayTo:
            cursor.execute("""SELECT * FROM userStateList 
                WHERE user_id=? AND user_day<=?""", (user_id, user_day))
        else:
            cursor.execute("""SELECT * FROM userStateList 
                WHERE user_id=? AND user_day=? AND letter_time=?""", (user_id, user_day, hour))
            
        result = cursor.fetchall()
        conn.close()
        user_status_list = []
        if dayTo:
            for element in result:
                user_status_list.append(element[4])
        else:
            for element in result:
                user_status = {}
                user_status['operation_id'] = element[0]
                user_status['operation_date'] = element[1]
                user_status['user_id'] = element[2]
                user_status['user_day'] = element[3]
                user_status['letter_id'] = element[4]
                user_status['letter_time'] = element[5]
                user_status['tag'] = element[6]
                user_status['is_sent'] = element[7]
                user_status_list.append(user_status)
        return user_status_list
    except:
        conn.close()
        return 0
    
    
def get_user_rate_state(user_id):
    conn = sqlite3.connect("db\sberbot.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT * FROM userRateStateList 
                        WHERE user_id=? AND is_rated=?""", (user_id, 0))
        result = cursor.fetchall()
        conn.close()
        user_rate_status_list = []
        for element in result:
            user_rate_status = {}
            user_rate_status['operation_id'] = element[0]
            user_rate_status['operation_date'] = element[1]
            user_rate_status['rate_date'] = element[2]
            user_rate_status['rate_header'] = element[3]
            user_rate_status['user_id'] = element[4]
            user_rate_status['user_day'] = element[5]
            user_rate_status['is_rated'] = element[6]
            user_rate_status['rate'] = element[7]
            user_rate_status['rate_text'] = element[8]
            user_rate_status['message_code'] = '/{}'.format((element[0] * 7) + element[4]) #Минимальное шифрование
            user_rate_status_list.append(user_rate_status)
        return user_rate_status_list
    except:
        conn.close()
        return 0

    
def get_user_info(personal_number = 0, user_id = 0, format_message = False):
    conn = sqlite3.connect("db\sberbot.db")
    cursor = conn.cursor()
    try:
        if personal_number:
            cursor.execute("""SELECT * FROM userList 
                            WHERE personal_number=?""", (int(personal_number), ))
        if user_id:
            cursor.execute("""SELECT * FROM userList 
                            WHERE user_id=?""", (user_id, ))
        result = cursor.fetchall()
        conn.close()
        user = {}
        for element in result:
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
        curr_datetime = datetime.datetime.now()
        user_start_date = datetime.datetime.strptime(user['date_start'], '%d.%m.%Y')
        user['day'] = get_user_day(user_start_date, curr_datetime)
        if format_message:
            answer_message = '''
            Информация о пользователе {}:\n
            ФИО пользователя - {};
            Табельный номер - {};
            Уровень авторизации - {};
            Телефонный номер - {};
            ID пользователя - {};
            Начало стажировки - {};
            Конец стажировки - {};
            Количество дней - {};
            ФИО ментора - {};                     
            '''.format(user['username'], user['user_lastname']+' '+user['user_firstname']+' '+user['user_middlename'],
                        user['personal_number'], user['is_authorised'], user['phone_number'], user['user_id'],
                        user['date_start'], user['date_end'], user['day'], user['mentor'])
            return answer_message
        else:
            return user
    except:
        conn.close()
        return 0
