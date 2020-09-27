import sqlite3
from classes.class_user import search_byAuth
from classes.class_user import User

class Mails:
    def __init__(self, database):
        self.db = database
        
        
    def get_mails_all(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM mailList""")
        self.raw_mails = cursor.fetchall()
        conn.close()

    
    def get_mails_allAllowed(self, user_day):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM mailList WHERE practice_day<=?""", (int(user_day), ))
        self.raw_mails = cursor.fetchall()
        conn.close()
    
    
    def get_mails_currDay(self, user_day):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM mailList WHERE practice_day=?""", (int(user_day), ))
        self.raw_mails = cursor.fetchall()
        conn.close()
            

    def get_mails_currDayTime(self, user_day, curr_time):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM mailList WHERE practice_day=? AND letter_time=?""", (int(user_day), int(curr_time))) 
        self.raw_mails = cursor.fetchall()
        conn.close()
    
    
    def compose_mails(self, user = 'NULL', get_all = False, get_allAllowed = False, get_currDay = False, get_currDayTime = False):
        self.maildata_list = []
        if get_all:
            self.get_mails_all()
        elif get_allAllowed:
            self.get_mails_allAllowed(user.userdata['user_day'])
        elif get_currDay:
            self.get_mails_currDay(user.userdata['user_day'])
        elif get_currDayTime:
            self.get_mails_currDayTime(user.userdata['user_day'], user.userdata['curr_time'])
        else:
            return 0
        
        if self.raw_mails:
            for element in self.raw_mails:
                self.maildata = {}
                self.maildata['letter_id'] = int(element[0])
                self.maildata['practice_day'] = element[1]
                self.maildata['letter_time'] = int(element[2])
                self.maildata['tag'] = element[3]
                self.maildata['letter_text'] = element[4]
                self.maildata_list.append(self.maildata)
                
    

def user_hourlyMail(curr_datetime, database):
    users = []
    users.append(search_byAuth(1, database))
    users.append(search_byAuth(2, database))
    mails = Mails(database)
    mails.compose_mails(get_all=True)
    mails_pack = []
    
    for user in users:
        user.get_userMailState()
        usermail_pack = []
        for mail in mails.maildata_list:
            if (mail['letter_id'] not in user.userSentLetterIDList):
                if (user.userdata['user_day'] >= mail['practice_day']) and (user.userdata['user_hour'] == mail['letter_time']):
                    mail['tg_uid'] = user.userdata['tg_uid']
                    user.register_sentMail(mail)
                    usermail_pack.append(mail)
        mails_pack.append(usermail_pack)
    return mails_pack


def user_dailyMail(curr_datetime, tg_uid, database):
    user = User(database)
    user.define(tg_uid, by_tg_uid = True)
    user.get_sber_info()
    mails = Mails(database)
    mails.compose_mails(user = user, get_currDay = True)
    return mails.maildata_list


    
    
                
            