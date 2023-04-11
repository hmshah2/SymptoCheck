from app import app
from flask import render_template,redirect,session,request
from app import database as db_helper




@app.route('/')
def homepage():
    return render_template("index.html")



@app.route('/login',methods = ["POST"])
def login():
    user = request.form['username']
    password = request.form['password']
    if db_helper.find_user(user,password) == 0:
        session['username'] = user
        return redirect('/index.html')
    else :
        "user does not exist or wrong password"


@app.route('/createAccount',methods = ['GET'])
def register():
    username = request.form['username']
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
    content = request.form.get('symptom_input')
    severity = request.form.get('sev_option')
    print(content)
    print(severity)
    search_Sym = db_helper.find_sym(content,severity)
    return render_template("index.html",results = search_Sym)


