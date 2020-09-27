import sqlite3
import datetime
import logging


class User:   
    def __init__(self, database):
        self.db = database
    
    
    def define(self, value, by_personnel_num = False, by_tg_uid = False, by_phone_num = False, count = False):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        if by_personnel_num:
            cursor.execute("""SELECT personnel_num,auth_status,tg_uid FROM userListSber WHERE personnel_num=?""", (value, ))
        if by_tg_uid:
            cursor.execute("""SELECT personnel_num,auth_status,tg_uid FROM userListSber WHERE tg_uid=?""", (value, ))
        if by_phone_num:
            cursor.execute("""SELECT personnel_num,auth_status,tg_uid FROM userListSber WHERE phone_num=?""", (value, ))
        else:
            return 0
        result = cursor.fetchall()
        #print ('RESULT ================= ', result)
        self.def_userdata = {}
        self.def_usercount = len(result)
        for element in result:
            self.def_userdata['personnel_num'] = element[0]
            self.def_userdata['auth_status'] = element[1]
            self.def_userdata['tg_uid'] = element[2]
        conn.close()
        
        
    def get_day(self):
        current_datetime = datetime.datetime.now()
        user_start_date = datetime.datetime.strptime(self.userdata['date_start'], '%d.%m.%Y')
        return (int((current_datetime - user_start_date).days) + 1)
    
    
    def get_time(self):
        current_datetime = datetime.datetime.now()
        return (current_datetime.hour)   
                
                
    def get_sber_info(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM userListSber WHERE personnel_num=?""", (self.def_userdata['personnel_num'], ))
        result = cursor.fetchall()
        conn.close()
        self.compose_user(result[0])


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
    
    
    def compose_user(self, element):
        self.userdata = {}
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
        self.userdata['user_day'] = self.get_day()
        self.userdata['user_hour'] = self.get_time()
        
        
    def register_new(self, full_name, phone_num, email, tg_name, tg_uid):
        self.define(phone_num, by_phone_num = True)
        if self.def_usercount != 1:
            if self.def_usercount == 0:
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
                                WHERE phone_num=?""", (tg_name, tg_uid, phone_num))
            
            cursor.execute("""INSERT INTO userListCustom(
                                        full_name, phone_num, email
                                        ) VALUES
                                        (?, ?, ?)
                                        """, (full_name, phone_num, email))
            conn.commit()
            conn.close()
            return 1
        return 0
    
    def fill_userInfo(self, full_name, ):
        pass
    
    def register_sentMail(self, mail):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO userSentMailList(
                            tg_uid, personnel_num, user_day, letter_id, letter_time, tag
                            ) VALUES (?, ?, ?, ?, ?, ?)
                            """, (self.userdata['tg_uid'], self.userdata['personnel_num'], self.userdata['user_day'], 
                                  mail['letter_id'], mail['letter_time'], mail['tag']))
        if mail['tag'] == 'rate':
            cursor.execute("""INSERT INTO userRateList(
                    operation_datetime, tg_uid, personnel_num, user_day, letter_id, rate_header
                    ) VALUES (?, ?, ?, ?)
                    """, (datetime.datetime.now(), self.userdata['tg_uid'], self.userdata['personnel_num'], self.userdata['user_day'], mail['letter_id'], mail['letter_text']))
                            
        conn.commit()
        conn.close()
        
        
    def register_ratedMail(self, rate_mark, rate_text):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO userRateList(
                            is_rated, rate_date, rate_mark, rate_text
                            ) VALUES (?, ?, ?, ?)
                            """, (1, datetime.datetime.now(), rate_mark, rate_text))
        conn.commit()
        conn.close()

    
    def get_userMailState(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM userSentMailList WHERE personnel_num=?""", (self.userdata['personnel_num'], ))
        result = cursor.fetchall()
        conn.close()        
        self.userMailList = []
        self.userSentLetterIDList = []
        for element in result:
            self.userMailData = {}
            self.userMailData['operation_id'] = element[0]
            self.userMailData['operation_datetime'] = element[1]
            self.userMailData['tg_uid'] = element[2]
            self.userMailData['personnel_num'] = element[3]
            self.userMailData['user_day'] = element[4]
            self.userMailData['letter_id'] = element[5]
            self.userMailData['letter_time'] = element[6]
            self.userMailData['tag'] = element[7]
            self.userMailList.append(self.userMailData)
            self.userSentLetterIDList.append(self.userMailData['letter_id'])
            
    
    def get_userRateState(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM userRateList WHERE personnel_num=?""", (self.userdata['personnel_num'], ))
        result = cursor.fetchall()
        conn.close()        
        self.userRateList = []
        for element in result:
            self.userRateData = {}
            self.userRateData['operation_id'] = element[0]
            self.userRateData['operation_datetime'] = element[1]
            self.userRateData['tg_uid'] = element[2]
            self.userRateData['personnel_num'] = element[3]
            self.userRateData['user_day'] = element[4]
            self.userRateData['letter_id'] = element[5]
            self.userRateData['is_rated'] = element[6]
            self.userRateData['rate_date'] = element[7]
            self.userRateData['rate_header'] = element[8]
            self.userRateData['rate_mark'] = element[9] 
            self.userRateData['rate_text'] = element[10]
            self.userRateList.append(self.userRateData)

            
            
def search_byAuth(status, database):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM userListSber WHERE auth_status=?""", (status, ))
    result = cursor.fetchall()
    conn.close()
    user_list = []
    for element in result:
        user = User(database)
        user.compose_user(element)
        user_list.append(user)
    return user_list
