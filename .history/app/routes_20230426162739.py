from app import app
from flask import render_template,redirect,session,request,url_for
from app import database as db_helper



cache = {'user':'100000000','age':'21','sex':'male'}
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
    print(results)
    return render_template("accountHome.html",data = results)

@app.route('/login/accounthome/updateacc',methods = ['GET','POST'])
def update():
    user = cache['user']
    new_pwd = request.form['password']
    db_helper.update_user(user,new_pwd)
    return "successfully change password",200
    
@app.route('/searchSym',methods = ['GET','POST'])
def search():
    content = request.form['symptom-input']
    severity = int(request.form['sev-option'])
    user = cache['user']
    if content == None:
        return render_template("index.html")
    search_Sym = db_helper.find_sym(content,severity)
    top_illness = search_Sym['illness'][0]
    top_treatment = search_Sym['Treatment'][0]
    db_helper.update_record(user,content,top_illness,top_treatment,severity)
    return render_template("index.html",results = search_Sym)


@app.route('/illpage/findIll',methods = ['GET','POST'])
def illsta():
    global search_Sex
    ill_content = request.form['ill-input']

    print(ill_content)
    if ill_content == None:
        return render_template("search_treatments.html")
    if (request.form['action'] == "search for treatments"):
        search_Tre = db_helper.ill_sta(ill_content)
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
    

@app.route('/direct')
def direct():
    global cache
    if cache['user'] == '100000000':
        return redirect('/login')
    else :
        return redirect('/login/accounthome')