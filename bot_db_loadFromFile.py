import sqlite3
import csv

def practice_list_reader(file):
    conn = sqlite3.connect("db\sberbot.db")
    cursor = conn.cursor()
    
    reader = csv.DictReader(file, delimiter=';')
    lines_to_add = []
    
    for line in reader:
        name_list = line['ФИО стажера'].split()
        last_name, first_name, middle_name = name_list
        personal_number = int(line['ТН'])
        phone = int(line['Телефон'])
        email = line['Почта']
        date_start = line['Дата выхода на стажировку']
        date_end = line['Окончание стажировки']
        mentor = line['ФИО наставника']
        is_authorised = 0

        lines_to_add.append((personal_number, last_name, first_name, 
                             middle_name, phone, date_start, date_end, mentor, is_authorised))
        
    if lines_to_add:    
        cursor.executemany("""INSERT INTO userList(
                            personal_number, user_lastname, user_firstname, user_middlename,
                            phone_number, date_start, date_end, mentor, is_authorised
                            ) VALUES
                            (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, lines_to_add)
    else:
        print('CSV file is empty')
        
    conn.commit()
    conn.close()
 
if __name__ == "__main__":
    with open("data\practice_db.csv", encoding='utf-8-sig') as file:
        practice_list_reader(file)