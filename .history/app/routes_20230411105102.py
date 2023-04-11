from app import app
from flask import render_template,redirect,session,request,url_for
from app import database as db_helper


session = {}
cache = {}

@app.route('/')
def homepage():
    return render_template("index.html")



@app.route('/illpage')
def illpage():
    return render_template("search_treatments.html")

@app.route('/accounthome')
def accpage():
    return render_template("accountHome.html")


@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/login/identify',methods = ["GET"])
def identify():
    user = request.form['username']
    cache['user'] = user
    password = request.form['password']
    print(password)
    if db_helper.find_user(user,password) == 1:
        
        return redirect(url_for('homepage'))
    else :
        "user does not exist or wrong password",400

@app.route('/login/register')
def register():
    return render_template("createAccount.html")

@app.route('/login/register/createAccount',methods = ['POST'])
def newaccount():
    username = request.form['username']
    print(username)
    password = request.form['password']
    age = request.form['age']
    sex = request.form['sex']
    if db_helper.find_user(username,password) == -1:
        db_helper.create_user(username,password,age,sex)
        return "successfully create an account",200
    else:
        return "user already exist",400

@app.route('/deleteAccount',methods = ['GET'])
def delete():
    username = request.form['username']
    password = request.form['password']
    age = request.form['age']
    sex = request.form['sex']
    if db_helper.find_user(username,password) == -1:
        db_helper.create_user(username,password,age,sex)
        return "successfully create an account",200
    else:
        return "user already exist",400


@app.route('/searchSym',methods = ['GET','POST'])
def search():
    content = request.form['symptom-input']
    severity = request.form['sev-option']
    if content == None:
        return render_template("index.html")
    search_Sym = db_helper.find_sym(content,severity)
    return render_template("index.html",results = search_Sym)


@app.route('/illpage/findIll',methods = ['GET','POST'])
def illsta():
    ill_content = request.form['ill-input']
    print(ill_content)
    if ill_content == None:
        return render_template("search_treatments.html")
    search_Tre = db_helper.ill_sta(ill_content)
    return render_template("search_treatments.html",results= search_Tre)
