import sqlite3

def save_msg_to_db(username, msg_date, msg_text, msg_id, user_id, user_first_name = 'NULL', user_last_name = 'NULL'):
    conn = sqlite3.connect("db\sberbot.db")
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO allMessages VALUES
                    (?, ?, ?, ?, ?, ?, ?)
                    """, (username, msg_date, msg_text, msg_id, user_id, user_first_name, user_last_name))
    conn.commit()
    conn.close()
    print('Message ID:{} saved successfully!'.format(msg_id))
    
def register_user(personal_number, names, phone, user_id, username):
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
                                user_id=?
                            WHERE personal_number=? AND user_firstname=?""", (username, user_id, personal_number, first_name))
            conn.commit()
            return 1
        else:
            return 0
    except:
        return 0
    
    conn.commit()
    conn.close()
        
#     UPDATE table_name
# SET column1 = value1, column2 = value2...., columnN = valueN
# WHERE [condition];
