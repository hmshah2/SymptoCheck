from flask import flask,render_template


app = flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html")





