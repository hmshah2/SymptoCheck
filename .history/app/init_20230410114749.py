from flask import Flask,render_template
from app import routes


app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html")





