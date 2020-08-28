import sqlite3
import datetime
import logging


class User:   
    def define(self, value, database, by_personnel_num = True, count = False):
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
        self.def_usercount = len(result)
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
            self.userdata['phone_num'] = element[3]
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
            self.custom_userdata['phone_num'] = element[2]
            self.custom_userdata['email'] = element[3]
            self.custom_userdata['area'] = element[4]
            self.custom_userdata['unit'] = element[5]
            self.custom_userdata['department'] = element[6]
            self.custom_userdata['mentor'] = element[7]
    
    
    def register_new(self, full_name, phone_num, personnel_num, email, tg_name, tg_uid, database):
        self.define(personnel_num, database)
        if self.def_usercount!=1:
            if self.def_usercount==0:
                print('User not found')
                return 0
            else:
                print('Incorrect amount of users')
                return 0
        
        self.get_sber_info()

        if self.def_userdata['auth_status']==0 and self.userdata['full_name']==full_name and self.def_usercount==1:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute("""UPDATE userListSber
                                SET auth_status='1',
                                    tg_name=?,
                                    tg_uid=?
                                WHERE personnel_num=? AND full_name=?""", (tg_name, tg_uid, personnel_num, full_name))
            
            cursor.execute("""INSERT INTO userListCustom(
                                        personnel_num, full_name, phone_num, email
                                        ) VALUES
                                        (?, ?, ?, ?)
                                        """, (personnel_num, full_name, phone_num, email))
            conn.commit()
            conn.close()
            return 1
        return 0
            
            
