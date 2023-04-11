from app import app
from flask import render_template,redirect,session,request,url_for
from app import database as db_helper




@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('search_treatments.html')
def my_link():
    # Redirect to another route
    return redirect(url_for('ill_route'))

@app.route('/ill-route')
def stapage():
    return render_template("search_treatments.html")



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
    content = request.form['symptom-input']
    severity = request.form['sev-option']
    if content == None:
        return render_template("index.html")
    search_Sym = db_helper.find_sym(content,severity)
    return render_template("index.html",results = search_Sym)


@app.route('/findIll',methods = ['GET','POST'])
def illsta():
    ill_content = request.form['ill-input']
    if ill_content == None:
        return render_template("search_treatments.html")
    search_Tre = db_helper.ill_sta(ill_content)
    return render_template("search_treatments.html",results= search_Tre)
