"""Defines all the functions related to the database"""
from app import db
import random
from datetime import date
from sqlalchemy.util.langhelpers import NoneType
from sqlalchemy import text




# search in db for possible diseases with symptoms
def find_sym(sym,sev) -> dict:
    #Returns : dict
    conn = db.connect()
    indicator = 0
    if type(sev) == NoneType:
        sev = 1
    if type(sym) != NoneType:
        indicator = 1
        query = conn.execute(text("SELECT IllnessName FROM Has_Symptom WHERE SymptomName LIKE '{}' AND Severity = {} GROUP BY IllnessName ORDER BY COUNT(IllnessName) DESC LIMIT 15;".format(sym,sev)))
        results = query.fetchall()
    
    results = list(results)
    for i in range(len(results)):
        results[i] = str(results[i])[2:-3]
    print(results)
        

    ill_dict = {}
    if len(results) != 0:
        ill_dict['illness'] = results
    else:
        ill_dict['illness'] = ['no data']
        ill_dict['treatment'] = ['no data']
        return ill_dict
    query_2 = text("SELECT t.Medicine  FROM Has_Treatment t JOIN (SELECT IllnessName FROM Has_Symptom WHERE SymptomName LIKE '{}' AND Severity = {} GROUP BY IllnessName ORDER BY COUNT(IllnessName) DESC LIMIT 15) AS s ON t.IllnessName = s.IllnessName GROUP BY t.Medicine ORDER BY COUNT(t.Medicine) DESC LIMIT 15;".format(sym,sev))
    results_2 = conn.execute(query_2).fetchall()
    results_2 = list(results_2)
    for i in range(len(results_2)):
        results_2[i] = str(results_2[i])[2:-3]

        
    ill_dict['treatment'] = results_2
    conn.close()
    return ill_dict

# search in db for possible treaments with illness
def ill_sta(ill) -> dict:
    ill_sta = {}
    conn = db.connect()
    query_1 = text("SELECT Medicine FROM Has_Treatment WHERE IllnessName LIKE '{}' GROUP BY Medicine ORDER BY COUNT(Medicine) DESC LIMIT 8;".format(ill))
    cur_1 = conn.execute(query_1)
    results_1 = cur_1.fetchall()
    results_1 = list(results_1)
    for i in range(len(results_1)):
        results_1[i] = str(results_1[i])[2:-3]
    query_2 = text("SELECT SymptomName FROM Has_Symptom WHERE IllnessName LIKE '{}' GROUP BY SymptomName ORDER BY COUNT(SymptomName) DESC LIMIT 8;".format(ill))
    cur_2 = conn.execute(query_2)
    results_2 = cur_2.fetchall()
    results_2 = list(results_2)
    for i in range(len(results_2)):
        results_2[i] = str(results_2[i])[2:-3]
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

# sex statistics
def sex_sta(ill) -> list:
    conn = db.connect()
    if type(ill) != NoneType:
        query = text("SELECT f.Illness, f.Num_Female, m.Num_Male FROM (SELECT trackable_name AS Illness, COUNT(user_id) as Num_Female FROM Records WHERE trackable_type = 'Condition' AND sex = 'female' GROUP BY Illness) AS f JOIN (SELECT trackable_name AS Illness, COUNT(user_id) as Num_Male FROM Records WHERE trackable_type = 'Condition' AND sex = 'male' GROUP BY Illness) AS m ON f.Illness = m.Illness ORDER BY f.Num_Female DESC, m.Num_Male DESC LIMIT 15;")
        results = conn.execute(query).fetchall()
        results = list(results)
        for i in range(len(results)):
            results[i] = str(results[i])[2:-3]
    conn.close()
    return results




# register
def create_user(user:str,pwd:str,age:int,sex:str) -> None:
    conn = db.connect()
    if type(user) != NoneType:
        
        query = text("INSERT INTO User(user_name,password,age,sex) VALUES('{}','{}',{},'{}')".format(user,pwd,age,sex))
        conn.execute(query)
        conn.commit()
    conn.close()

# update
def update_user(user:str,old_pwd:str,new_pwd:str) -> str:
    conn = db.connect()

    if type(user) != NoneType:
        
       

        

        query = text("""
        CREATE TRIGGER password_update_trigger 
        BEFORE UPDATE ON User 
        FOR EACH ROW 
        BEGIN 
            IF OLD.password != :old_pwd THEN 
                
                SET @message = 'Incorrect old password entered.'; 
            ELSEIF :new_pwd = OLD.password THEN 
                
                SET @message = 'New password cannot be the same as the old password.'; 
            ELSE 
                UPDATE User 
                SET NEW.password = :new_pwd 
                WHERE user_name = :user
                SET @message = 'Password updated successfully.'; 
            END IF; 
            SELECT @message AS message; 
        END;
        """)

        query = query.bindparams(old_pwd=old_pwd, new_pwd=new_pwd,user = user)



        conn.execute(query)
        conn.commit()
        result = conn.execute("SELECT @message").fetchone()
    conn.close()
    return result

# match user
def find_user(user:str,pwd:str) -> dict:
    conn = db.connect()
    if type(user) != NoneType:
        
        query = text("SELECT * FROM User WHERE user_name = '{}'".format(user))
        results = conn.execute(query).fetchall()
    conn.close()
    df = dict()
    if len(results) == 0:
        df['user_name'] = ""
        return df
    user_name,password,age,sex = results[0]
    df['user_name'] =user_name
    df['password'] = password
    df['age'] = age
    df['sex'] = sex
    return df

# delete
def delete_user(user:str) -> str:
    conn = db.connect()
    if type(user) != NoneType:
        query = text("DELETE FROM User WHERE user_name = '{}';".format(user))
        conn.execute(query)
        conn.commit()
    conn.close()
    return "successfully delete your account"

# find_record
def find_record(user:str) -> list:
    conn = db.connect()
    query = text("SELECT * FROM Search_Record WHERE user_id = '{}' ORDER BY checkin_date DESC LIMIT 10;".format(user))
    cur = conn.execute(query)
    results = cur.fetchall()
    if results:
        return results
    else:
        return []

    
# update_record
def update_sym_record(user:str,sym:str,ill:str,tre:str,sev:int) -> None:
    conn = db.connect()
   
    today = date.today()
    query_insert = text("INSERT INTO Search_Record(user_id,symptom,illness,treatment,checkin_date,severity) VALUES ('{}','{}','{}','{}','{}','{}');".format(user,sym,ill,tre,today,sev))
    conn.execute(query_insert)
    conn.commit()
    conn.close()
    print("succeed")


