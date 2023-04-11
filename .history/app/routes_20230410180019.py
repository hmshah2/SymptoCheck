from app import app
from flask import render_template,redirect,session,requests
from app import database as db_helper




@app.route('/')
def homepage():
    return render_template("index.html")



@app.route('/login',methods = ["POST"])
def login():
    user = requests.form['username']
    password = requests.form['password']
    if db_helper.find_user(user,password):
        session['username'] = user
        return redirect('/index.html')
    else :
        "check your password and username"


@app.route('/createAccount',methods = ['GET'])
def register():


