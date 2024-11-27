from flask import Flask, render_template, request, redirect, url_for, jsonify
import sys
from grid import *

app = Flask(__name__)

class DataStore():
    selectOption = "not set"
    ship = Ship()
    fileName = "not set"
    shipChanges = []


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

@app.route('/Transfer-comingon', methods = ["GET", "POST"])
def comingon():
    for item in DataStore.shipChanges:
        itemArray = item.split('_')
        itemID = itemArray[0]
        for i in range(len(DataStore.shipChanges)):
            if item == DataStore.shipChanges[i]:
                DataStore.shipChanges[i] = itemID
    for item in DataStore.shipChanges:
        index = 95 - int(item)
        DataStore.ship.containers[index].weight = "00000"
        DataStore.ship.containers[index].name = "UNUSED"
    DataStore.ship.printContainers()
    return render_template('comingon.html', ship = DataStore.ship.containers)

@app.route('/Transfer-process-changes', methods = ["GET", "POST"])
def transferChanges():
    data = request.get_json()
    if data and isinstance(data, list):
        print("Recieved array", file=sys.stderr)
        selectedIDsString = ""
        DataStore.shipChanges = data
        print(DataStore.shipChanges, file=sys.stderr)
        for element in data:
            selectedIDsString += element + " "
        return jsonify({"status": "success", "array" : selectedIDsString})
    else:
        DataStore.shipChanges = []
        print(DataStore.shipChanges, file=sys.stderr)
        return jsonify({"status": "error", "message": "Recieved Empty List"}), 400

def Transfer():
    return render_template('Transfer.html')

@app.route('/Transfer-comingoff', methods = ["GET", "POST"])
def comingoff():
    return render_template('comingoff.html', fileUploaded = DataStore.fileName, ship = DataStore.ship.containers)

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
        DataStore.fileName = file.filename
        print(DataStore.fileName, file = sys.stderr)
        file.save(file.filename)
        DataStore.ship.loadGrid(DataStore.fileName)
        if(DataStore.selectOption == "Balance"):
            return render_template('Balance.html', fileUploaded = file.filename, ship = DataStore.ship.containers)
        elif(DataStore.selectOption == "Transfer"):
            print("in transfer conditional", file = sys.stderr)
            return redirect(url_for('comingoff'))
    return redirect(url_for('Error'))

