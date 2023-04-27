from app import app
from flask import render_template,redirect,session,request,url_for
from app import database as db_helper
import datetime



cache = {'user':'100000000','password':'','age':21,'sex':'male'}
search_Sex = []

@app.route('/')
def homepage():
    return render_template("index.html")



@app.route('/illpage')
def illpage():
    return render_template("search_treatments.html")



@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/login/identify',methods = ["POST"])
def identify():
    #global cache
    user = request.form['username']
    cache['user'] = user
    print(cache['user'])
    password = request.form['password']
    df = db_helper.find_user(user,password)
    if df['user_name'] == "":
        return "user does not exist",400
    if df['password']  == password:
        cache['password'] = password
        cache['age'] = df['age']
        cache['sex'] = df['sex']
        return redirect('/')
    return "wrong password",400

@app.route('/login/register')
def register():
    return render_template("createAccount.html")

@app.route('/login/register/createAccount',methods = ['POST'])
def newaccount():
    username = request.form['username']
    password = request.form['password']
    age = request.form['age']
    sex = request.form['sex']
    if db_helper.find_user(username,password)['user_name'] == "":
        db_helper.create_user(username,password,age,sex)
        return redirect('/login/accounthome')
    else:
        return "user already exist",400

@app.route('/login/accounthome/deleteacc',methods = ['GET'])
def delete():
    global cache
    username = cache['user']
    str = db_helper.delete_user(username)
    cache = {}
    return str,200

@app.route('/login/accounthome',methods = ['GET'])
def accpage():
    results = db_helper.find_record(cache['user'])
    item_result = []

    for line in results:
        split_line = list(line)
        #split_line = line.split(',')
        dt_string = split_line[5].strftime('%Y-%m-%d')
        append_item = [split_line[2].strip(''),split_line[3].strip(''),split_line[4].strip(''),dt_string]
        item_result.append(append_item)
        print(item_result)
    return render_template("accountHome.html",data = item_result)

@app.route('/login/accounthome/admin',methods = ['GET'])
def admin():
    return render_template("popup.html")

@app.route('/login/accounthome/updateacc',methods = ['GET','POST'])
def update():
    user = cache['user']
    
    old_pwd = request.form['old_pwd']
    new_pwd = request.form['new_pwd']
    result = db_helper.update_user(user,old_pwd,new_pwd)
    return result


@app.route('/login/accounthome/updateAdm',methods = ['POST'])
def update_admin():
    sym = request.form['sym']
    ill = request.form['ill']
    sev = request.form['sev']
    result = db_helper.admin_update_record(sym,ill,sev)
    

@app.route('/searchSym',methods = ['GET','POST'])
def search():
    content = request.form['symptom-input']
    severity = int(request.form['sev-option'])
    user = cache['user']
    if content == None:
        return render_template("index.html")
    search_Sym = db_helper.find_sym(content,severity)
    top_illness = search_Sym['illness'][0]
    top_treatment = search_Sym['treatment'][0]
    db_helper.update_sym_record(user,content,top_illness,top_treatment,severity)
    return render_template("index.html",results = search_Sym)


@app.route('/illpage/findIll',methods = ['GET','POST'])
def illsta():
    global search_Sex
    ill_content = request.form['ill-input']
    user_id = cache['user_id']
    print(ill_content)
    if ill_content == None:
        return render_template("search_treatments.html")
    if (request.form['action'] == "search for treatments"):
        search_Tre = db_helper.ill_sta(ill_content)
        top_sym = search_Tre['symptom']
        top_tre = search_Tre['treatment']
        db_helper.update_sym_record(user_id,top_sym,ill_content,top_tre,'/')
        return render_template("search_treatments.html",results_Tre= search_Tre)
    elif request.form['action'] == "know about sex statistics":
        if len(search_Sex) == 0:
            search_Sex = db_helper.sex_sta(ill_content)
        
        return render_template("search_treatments.html",results_Sex= search_Sex)
    else:
        return "Invalid",400

@app.route('/illpage/direct')
def illdirect():
    global cache
    if cache == {}:
        return redirect('/login')
    else :
        return redirect('/login/accounthome')

@app.route('/login/accounthome/direct')
def admindirect():
    global cache
    if cache['user'] == "admin019019":
        return redirect('/login/accounthome/admin')
    

@app.route('/direct')
def direct():
    global cache
    if cache['user'] == '100000000':
        return redirect('/login')
    else :
        return redirect('/login/accounthome')