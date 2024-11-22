from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def Login():
    return render_template('Login.html')

@app.route('/Dashboard', methods = ["GET", "POST"])
def Dashboard():
    if request.method == "POST":
        user =  request.form['user']
        return render_template('Dashboard.html', name=user)