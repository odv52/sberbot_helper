import sqlite3
import datetime
import logging


class User:   
    def define(self, value, database, by_personnel_num = True):
        self.db = database
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        if by_personnel_num:
            cursor.execute("""SELECT personnel_num,auth_status,tg_uid FROM userListSber WHERE personnel_num=?""", (value, ))
        else:
            cursor.execute("""SELECT personnel_num,auth_status,tg_uid FROM userListSber WHERE tg_uid=?""", (value, ))
        result = cursor.fetchall()
        print ('RESULT ================= ', result)
        self.def_userdata = {}
        for element in result:
            self.def_userdata['personnel_num'] = element[0]
            self.def_userdata['auth_status'] = element[1]
            self.def_userdata['tg_uid'] = element[2]
        conn.close()
        
    def get_day(self):
        current_date = datetime.datetime.now()
        user_start_date = datetime.datetime.strptime(self.userdata['date_start'], '%d.%m.%Y')
        return (int((current_date - user_start_date).days) + 1)
                
    def get_sber_info(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM userListSber WHERE personnel_num=?""", (self.def_userdata['personnel_num'], ))
        result = cursor.fetchall()
        conn.close()
        self.userdata = {}
        for element in result:
            self.userdata['personnel_num'] = element[0]
            self.userdata['full_name'] = element[1]
            self.userdata['auth_status'] = element[2]
            self.userdata['phone_number'] = element[3]
            self.userdata['email'] = element[4]
            self.userdata['tg_name'] = element[5]
            self.userdata['tg_uid'] = element[6]
            self.userdata['date_start'] = element[7]
            self.userdata['date_end'] = element[8]
            self.userdata['area'] = element[9]
            self.userdata['unit'] = element[10]
            self.userdata['department'] = element[11]
            self.userdata['mentor'] = element[12]
            self.userdata['day'] = self.get_day()
    
    def get_custom_info(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM userListCustom WHERE personnel_num=?""", (self.def_userdata['personnel_num'], ))
        result = cursor.fetchall()
        conn.close()
        self.custom_userdata = {}
        for element in result:
            self.custom_userdata['personnel_num'] = element[0]
            self.custom_userdata['full_name'] = element[1]
            self.custom_userdata['phone_number'] = element[2]
            self.custom_userdata['email'] = element[3]
            self.custom_userdata['area'] = element[4]
            self.custom_userdata['unit'] = element[5]
            self.custom_userdata['department'] = element[6]
            self.custom_userdata['mentor'] = element[7]