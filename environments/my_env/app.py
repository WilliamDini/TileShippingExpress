from flask import Flask, render_template, request, redirect, url_for
import sys

app = Flask(__name__)

class DataStore():
    selectOption = "not set"

@app.route('/', methods = ["GET", "POST"])
def Login():
    return render_template('Login.html')

@app.route('/Dashboard', methods = ["GET", "POST"])
def Dashboard():
    if request.method == "POST":
        user =  request.form['user']
        return render_template('Dashboard.html', name=user)
    
@app.route('/Error', methods = ["GET", "POST"])
def Error():
    return render_template('Error.html')

@app.route('/Balance', methods = ["GET", "POST"])
def Balance():
    return render_template('Balance.html')

@app.route('/Transfer', methods = ["GET", "POST"])
def Transfer():
    return render_template('Transfer.html')

@app.route('/FileSelect', methods = ['GET', 'POST'])
def checkAction():
    print("In check action", file = sys.stderr)
    if request.method == "POST":
        print("", file = sys.stderr)
        DataStore.selectOption = request.form['TypeAction']
        print("The action selected is: " + DataStore.selectOption, file=sys.stderr)
        return render_template('FileSelect.html', select = DataStore.selectOption)
    return redirect(url_for('Error'))

@app.route('/typeFile', methods = ['GET', 'POST'])
def fileUpload():
    print("In fileUpload", file = sys.stderr)
    if request.method == "POST":
        print(DataStore.selectOption, file = sys.stderr)
        file = request.files['file']
        file.save(file.filename)
        if(DataStore.selectOption == "Balance"):
            return render_template('Balance.html', fileUploaded = file.filename)
        elif(DataStore.selectOption == "Transfer"):
            return render_template('Transfer.html', fileUploaded = file.filename)
    return redirect(url_for('Error'))

