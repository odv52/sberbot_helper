import sqlite3
import csv

def practice_list_reader(file):
    conn = sqlite3.connect("db\sberbot.db")
    cursor = conn.cursor()
    
    reader = csv.DictReader(file, delimiter=';')
    lines_to_add = []
    
    for line in reader:
        personnel_num = int(line['ТН'])
        full_name = line['ФИО стажера']
        phone_number = int(line['Телефон'])
        email = line['Почта']
        date_start = line['Дата выхода на стажировку']
        date_end = line['Окончание стажировки']
        area = line['Направление стажировки']
        unit = line['Блок стажера']
        department = line['Департамент']
        mentor = line['ФИО наставника']
        
        lines_to_add.append((personnel_num, full_name, phone_number, 
                             email, date_start, date_end, area, unit, department, mentor))
        
    if lines_to_add:    
        cursor.executemany("""INSERT INTO userListSber(
                            personnel_num, full_name, phone_number, email,
                            date_start, date_end, area, unit, department, mentor
                            ) VALUES
                            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, lines_to_add)
    else:
        print('CSV file is empty')
        
    conn.commit()
    conn.close()
    

    
    
    
    
    
    
    
    
    
# def shedule_list_reader(overwrite = False):
#     conn = sqlite3.connect("db\sberbot.db")
#     cursor = conn.cursor()
    
#     with open("data\mail_test.csv", encoding='utf-8-sig') as file:
    
#         reader = csv.DictReader(file, delimiter=';')
#         lines_to_add = []
        
#         for line in reader:
#             practice_day = int(line['day'])
#             letter_time = int(line['time'])
#             tag = line['tag']
#             letter_text = line['text']

#             lines_to_add.append((practice_day, letter_time, tag, letter_text))
            
#         if lines_to_add:    
#             if overwrite:
#                 cursor.execute("""DELETE FROM mailList""")
#                 conn.commit()
                
#             cursor.executemany("""INSERT INTO mailList(
#                                 practice_day, letter_time, tag, letter_text
#                                 ) VALUES
#                                 (?, ?, ?, ?)
#                                 """, lines_to_add)
#         else:
#             print('CSV file is empty')
            
#         conn.commit()
#         conn.close()
 
if __name__ == "__main__":
    with open("data\system_data\practice_db.csv", encoding='utf-8-sig') as file:
        practice_list_reader(file)
        
    # with open("data\mail_test.csv", encoding='utf-8-sig') as file:
    #     shedule_list_reader(file)
        