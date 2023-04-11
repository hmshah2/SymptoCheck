"""Defines all the functions related to the database"""
from app import db
import random
from datetime import date
from sqlalchemy.util.langhelpers import NoneType
from sqlalchemy import text




# search in db for possible diseases with symptoms
def find_sym(sym,sev) -> list:
    #Returns : list
    conn = db.connect()
    indicator = 0
    if type(sev) == NoneType:
        sev = 1
    if type(sym) != NoneType:
        indicator = 1
        query = conn.execute(text("SELECT IllnessName FROM Has_Symptom WHERE SymptomName LIKE '{}' AND Severity = {} GROUP BY IllnessName ORDER BY COUNT(IllnessName) DESC LIMIT 5;".format(sym,sev)))
        results = query.fetchall()
    conn.close()
    ill_list = []
    if indicator == 1:
        ill_list = results
    print(ill_list)
    return ill_list

# search in db for possible treaments with illness
def ill_sta(ill) -> dict:
    ill_sta = {}
    conn = db.connect()
    query_1 = text("SELECT Medicine FROM Has_Treatment WHERE IllnessName LIKE '{}' GROUP BY Medicine ORDER BY COUNT(Medicine) DESC LIMIT 10;".format(ill))
    cur_1 = conn.execute(query_1)
    results_1 = cur_1.fetchall()
    ill_sta['treatment'] = results_1
    query_2 = text("SELECT SymptomName FROM Has_Symptom WHERE IllnessName LIKE '{}' GROUP BY SymptomName ORDER BY COUNT(SymptomName) DESC LIMIT 10;".format(ill))
    cur_2 = conn.execute(query_2)
    results_2 = cur_2.fetchall()
    conn.close()
    excuse = ["No data"]
    if results_1:
        ill_sta["treatment"] = results_1
    else:
        ill_sta["treatment"] = excuse
    if results_2:
        ill_sta['symptom'] = results_2
    else:
        ill_sta['symptom'] = excuse
    return ill_sta



# register
def create_user(user:str,pwd:str,age:int,sex:str) -> None:
    conn = db.connect()
    if type(user) != NoneType:
        
        query = 'INSERT INTO User(user_name,password,age,sex) VALUES({},{},{},{})'.format(user,pwd,age,sex)
        conn.execute(query)
        conn.commit()
    conn.close()

# update
def update_user(user:str,pwd:str) -> None:
    conn = db.connect()
    if type(user) != NoneType:
        
        query = 'UPDATE User SET password = {} WHERE user_name = {}'.format(pwd,user)
        conn.execute(query)
        conn.commit()
    conn.close()

# match user
def find_user(user:str,pwd:str) -> int:
    conn = db.connect()
    if type(user) != NoneType:
        
        query = text('SELECT password FROM User WHERE user_name = {}'.format(user)
        results = conn.execute(query).fetchall()
    conn.close()
    if len(results) == 0:
        return -1
    for result in results:
        if result == pwd:
            return 1
    return 0

# delete
#def delete_user(user:str) -> str:
#    conn = db.connect()
#    if type(user) != NoneType:
#        query = 'DELETE FROM User WHERE user_name = {}'.format(user)
#        conn.execute(query)
#        conn.commit()
#    conn.close()
#    return "successfully delete your account"

# find_record
def find_record(user:str) -> list:
    conn = db.connect()
    query = text("SELECT * FROM Records WHERE user_id = '{}' ORDER BY checkin_date DESC LIMIT 10;".format(user))
    cur = conn.execute(query)
    results = cur.fetchall()
    if results:
        return results
    else:
        return []

    
# update_record
def update_record(user:str,sym:str,age:int,sex:str,sev:int) -> None:
    conn = db.connect()
    query_check = text('SELECT * FROM Records WHERE user_id = '{}' AND age = {} AND sex = '{}' AND trackable_type = "Symptom" AND trackable_name = '{}' and trackable_value = '{}' LIMIT 1;'.format(user,age,sex,sym,sev))
    list_check = conn.execute(query_check).fetchall()
    if list_check:
        conn.close()
        return
    else:
        today = date.today()
        id = random.randint(10000000, 99999999)
        query_insert = text('INSERT INTO Records(user_id,age,sex,country,checkin_date,trackable_id,trackable_type,trackable_name,trackable_value) VALUES ('{}',{},'{}','','{}','{}','Symptom','{}',{});'.format(user,age,sex,today,id,sym,sev))
        conn.execute(query_insert)
        conn.commit()
    conn.close()


