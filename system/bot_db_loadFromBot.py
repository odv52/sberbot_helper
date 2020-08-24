import sqlite3

def save_msg_to_db(username, msg_date, msg_text, msg_id, user_id):
    conn = sqlite3.connect("db\sberbot.db")
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO allMessages VALUES
                    (?, ?, ?, ?, ?) """, (msg_id, username, user_id, msg_date, msg_text))
    conn.commit()
    conn.close()
    print('Message ID:{} saved successfully!'.format(msg_id))
    
    
def save_rate_to_db(user_id, rate, rate_text, curr_datetime, code):
    conn = sqlite3.connect("db\sberbot.db")
    cursor = conn.cursor()
    operation_id = (int(code) - int(user_id))/7
    try:
        cursor.execute("""UPDATE userRateStateList SET
                        rate_date=?, is_rated=?, rate=?, rate_text=? WHERE
                        user_id=? AND operation_id=?
                        """, (curr_datetime, 1, rate, rate_text, user_id, operation_id))
        conn.commit()
        conn.close()
        return 1
    except:
        conn.close()
        return 0

    
def register_user(personal_number, names, phone, mentor, user_id, username):
    conn = sqlite3.connect("db\sberbot.db")
    cursor = conn.cursor()
    last_name, first_name, middle_name = names.split()
    try:
        cursor.execute("""SELECT COUNT(personal_number) FROM userList 
                        WHERE personal_number=? AND user_firstname=? AND is_authorised='0'""", (personal_number, first_name))
        counts = cursor.fetchone()
        if counts[0] == 1:
            cursor.execute("""UPDATE userList
                            SET is_authorised='1',
                                username=?,
                                user_id=?,
                                mentor=?
                            WHERE personal_number=? AND user_firstname=?""", (username, user_id, mentor, personal_number, first_name))
            conn.commit()
            conn.close()
            return 1
        else:
            conn.close()
            return 0
    except:
        conn.close()
        return 0
