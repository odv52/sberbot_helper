import sqlite3
import datetime

def get_user_day(start_date, curr_date):
    return (int((curr_date - start_date).days) + 1)


def get_user_status(user_id, user_day):
    conn = sqlite3.connect("db\sberbot.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT * FROM userStateList 
                        WHERE user_id=? AND user_day=?""", (user_id, user_day))
        result = cursor.fetchall()
        conn.close()
        user_status = {}
        for element in result:
            user_status['operation_id'] = element[0]
            user_status['operation_date'] = element[1]
            user_status['user_id'] = element[2]
            user_status['user_day'] = element[3]
            user_status['is_received_letters'] = element[4]
            user_status['is_rated'] = element[5]
            user_status['rate_message'] = element[6]
        return user_status
    except:
        conn.close()
        return 0
    

def get_user_info(personal_number):
    conn = sqlite3.connect("db\sberbot.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT * FROM userList 
                        WHERE personal_number=?""", (personal_number, ))
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
        user_date = get_user_day(user_start_date, curr_datetime)
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
                    user['date_start'], user['date_end'],user_date, user['mentor'])
        return answer_message
    except:
        conn.close()
        return 0
