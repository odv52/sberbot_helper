import sqlite3

conn = sqlite3.connect("db\sberbot.db")
cursor = conn.cursor()
 
# Создание таблицы с историей сообщений
cursor.execute("""CREATE TABLE IF NOT EXISTS allMessages(
                message_id INTEGER NOT NULL PRIMARY KEY,
                username TEXT,
                user_id INTEGER NOT NULL, 
                message_date DATE, 
                message_text TEXT
                )
                """)
conn.commit()

#Создание списка пользователей, состояния авторизации и табельного номера
cursor.execute("""CREATE TABLE IF NOT EXISTS userList(
                personal_number INTEGER NOT NULL PRIMARY KEY,
                user_lastname TEXT,
                user_firstname TEXT,
                user_middlename TEXT,
                is_authorised BOOLEAN,
                phone_number INTEGER NOT NULL,
                username TEXT,
                user_id INTEGER, 
                date_start DATE,
                date_end DATE,
                mentor TEXT
                )
                """)
conn.commit()

conn.close()
# Создание таблицы соответствия файла и file_id
# Создание таблицы контента (рассылок)
