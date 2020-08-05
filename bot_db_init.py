import sqlite3

conn = sqlite3.connect("db\sberbot.db")
cursor = conn.cursor()
 
# Создание таблицы с историей сообщений
cursor.execute("""CREATE TABLE IF NOT EXISTS allMessages(
                message_id INTEGER NOT NULL PRIMARY KEY,
                username TEXT,
                user_id INTEGER NOT NULL, 
                message_date DATETIME, 
                message_text TEXT
                )
                """)
conn.commit()

#Создание списка пользователей, состояния авторизации и табельного номера
cursor.execute("""CREATE TABLE IF NOT EXISTS userList(
                personal_number INTEGER NOT NULL PRIMARY KEY,
                user_lastname TEXT DEFAULT 'NONE',
                user_firstname TEXT DEFAULT 'NONE',
                user_middlename TEXT DEFAULT 'NONE',
                is_authorised BOOLEAN DEFAULT 0,
                phone_number INTEGER NOT NULL,
                username TEXT DEFAULT 'NONE',
                user_id INTEGER DEFAULT 'NONE', 
                date_start DATE,
                date_end DATE,
                mentor TEXT DEFAULT 'NONE'
                )
                """)
conn.commit()

#Создание базы данных для предзагрузки текста и параметров рассылки
cursor.execute("""CREATE TABLE IF NOT EXISTS mailList(
                letter_id INTEGER NOT NULL PRIMARY KEY,
                practice_day INTEGER,
                letter_time INTEGER,
                tag TEXT,
                letter_text TEXT
                )
                """)
conn.commit()

#Создание таблиц состояния получения сообщения
cursor.execute("""CREATE TABLE IF NOT EXISTS userStateList(
                operation_id INTEGER NOT NULL PRIMARY KEY,
                operation_date DATETIME NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
                user_id INTEGER,
                user_day INTEGER,
                letter_id INTEGER,
                letter_time INTEGER,
                tag TEXT,
                is_sent BOOLEAN DEFAULT 0
                )
                """)
conn.commit()

#Создание таблиц состояния голосования
cursor.execute("""CREATE TABLE IF NOT EXISTS userRateStateList(
                operation_id INTEGER NOT NULL PRIMARY KEY,
                operation_date DATETIME,
                rate_date DATETIME,
                rate_header TEXT NOT NULL DEFAULT 'EMPTY',
                user_id INTEGER,
                user_day INTEGER,
                is_rated BOOLEAN DEFAULT 0,
                rate INTEGER DEFAULT 0,
                rate_text TEXT DEFAULT 'EMPTY'
                )
                """)
conn.commit()



conn.close()
# Создание таблицы соответствия файла и file_id