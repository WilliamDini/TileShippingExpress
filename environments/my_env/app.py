from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sys
from grid import *
from Transfer import *
from Transfer import Problem
from datetime import datetime, timezone
import pytz
import os

app = Flask(__name__)
app.secret_key = 'DrKeoghRocks'
class DataStore():
    selectOption = "not set"
    ship = Ship()
    fileName = "not set"
    shipChanges = []
    #problem = Problem(ship.containers)
    #transfer = Transfer(Problem.shipContNested, Problem.shipContainers)
    #shipCntrOn = []

log_file = 'logfile.log' 
pst_timezone = pytz.timezone('US/Pacific')

def log(append_str):
    utc_now = datetime.now(timezone.utc)
    pst_now = utc_now.replace(tzinfo=pytz.utc).astimezone(pst_timezone)

    timestamp = pst_now.strftime('%H:%M')

    with open(log_file, 'a') as f:
        f.write(f'{timestamp} {append_str}\n')

@app.route('/', methods = ["GET", "POST"])
def Login():
    if request.method == "POST":
        user = request.form.get('user', 'Guest') 
        session['user'] = user 
        log(user + "has logged in.")
        return redirect(url_for('Dashboard'))  
    return render_template('Login.html') 

@app.route('/Dashboard', methods = ["GET", "POST"])
def Dashboard():
    if request.method == "POST":
        user = request.form.get('user', 'Guest') 
        session['user'] = user 
    user = session.get('user', 'Guest') 
    return render_template('Dashboard.html', name=user)
    
@app.route('/Error', methods = ["GET", "POST"])
def Error():
    return render_template('Error.html')

@app.route('/Transfer-loading', methods=["GET", "POST"])
def loading():
    if request.method == "POST":
        num_containers = request.form.get("num_containers")

        if not num_containers.isdigit() and not (num_containers.lstrip('-').isdigit()):
            return render_template('loading.html', error="Please enter a valid number.")

        num_containers = int(num_containers)

        if num_containers < 0:
            print(f"Negative number ({num_containers}) entered. Adjusting to 0.", file=sys.stderr)
            num_containers = 0

        num_empty_spaces = sum(1 for container in DataStore.ship.containers if container.name == "UNUSED")
        num_to_unload = len(DataStore.shipChanges)
        max_loadable = num_empty_spaces + num_to_unload

        if num_containers > max_loadable:
            return render_template(
                'loading.html',
                error=f"The number of containers must be less than or equal to {max_loadable}."
            )


        print(f"User wants to load {num_containers} containers", file=sys.stderr)
        DataStore.num_containers_to_load = num_containers

        #changed redirect from "transfer_process"
        return redirect(url_for('transfer_process_off', current=1))

    return render_template('loading.html')


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

@app.route('/Transfer-process', methods=["GET", "POST"])
def transfer_process():
    current_operation = request.args.get("current", 1, type=int)

    num_containers_to_remove = len(DataStore.shipChanges)
    num_containers_to_load = getattr(DataStore, 'num_containers_to_load', 0)
    total_operations = num_containers_to_remove + num_containers_to_load

    ship_data = DataStore.ship.containers

    #figure out how to render a come off path first,
    #with next button, to go to a come on path, keep
    #alternating, til operations is complete

    if request.method == "POST":
        container_name = request.form.get('container_name')
        container_weight = request.form.get('container_weight')

        if not container_name or not container_weight:
            return render_template(
                'TransferProcess.html',
                ship=ship_data,
                current_operation=current_operation,
                total_operations=total_operations,
                error="Name and weight are required."
            )

        try:
            container_weight = float(container_weight)  
        except ValueError:
            return render_template(
                'TransferProcess.html',
                ship=ship_data,
                current_operation=current_operation,
                total_operations=total_operations,
                error="Weight must be a valid number."
            )

        if container_weight < 0:
            print(f"Negative weight ({container_weight}) entered. Adjusting to 0.", file=sys.stderr)
            container_weight = 0  
        elif container_weight > 9999:
            print(f"Weight ({container_weight}) exceeds 9999. Adjusting to 9999.", file=sys.stderr)
            container_weight = 9999 
        else:
            container_weight = round(container_weight) 

        if current_operation <= len(ship_data):
            ship_data[current_operation - 1].name = container_name
            ship_data[current_operation - 1].weight = f"{int(container_weight):05}"  # Format as 5-digit number

        current_operation += 1
        if current_operation > total_operations:
            return redirect(url_for('success'))

    return render_template(
        'TransferProcess.html',
        ship=ship_data,
        current_operation=current_operation,
        total_operations=total_operations
    )

@app.route('/Transfer-process-Off', methods=["GET", "POST"])
def transfer_process_off():
    current_operation = request.args.get("current", 1, type=int)

    num_containers_to_remove = len(DataStore.shipChanges)
    num_containers_to_load = getattr(DataStore, 'num_containers_to_load', 0)
    total_operations = num_containers_to_remove + num_containers_to_load

    ship_data = DataStore.ship.containers

    #figure out how to render a come off path first,
    #with next button, to go to a come on path, keep
    #alternating, til operations is complete
    action = ""
    contOffArr = []
    if len(DataStore.shipChanges) > 0:
        action = "Off"
        for element in DataStore.shipChanges:
            temp = element.split("_")
            contOffArr.append(temp[1])
        print(contOffArr, file = sys.stderr)

    problem = Problem(DataStore.ship.containers)
    print(DataStore.shipChanges, file = sys.stderr)
    problem.loadNestedContainers()
    problem.printShipContNested()
    
    transfer = Transfer(problem.shipContNested, problem.shipContainers)
    if len(contOffArr) > 0:
        for element in problem.shipContainers:
            if(element.name == contOffArr[0]):
                container = element

        pathArray = transfer.moveContainerOff(container, [])
        newPathArray = []
        for element in pathArray:
            if type(element) != list:
                newPathArray.append(element)
    
        print("path is: ", file = sys.stderr)
        if(newPathArray == None):
            print("No path available", file = sys.stderr)
        else:
            for element in newPathArray:
                print(element, file = sys.stderr)

        steps = problem.returnPathArray(newPathArray)
        print(len(steps[0]), file = sys.stderr)
        DataStore.ship.containers = steps[0]
        ship_data = DataStore.ship.containers
        contOffArr.pop(0)
        DataStore.shipChanges.pop(0)
        steps.pop(0)

    if request.method == "POST":
        DataStore.ship.containers = steps[0]
        ship_data = DataStore.ship.containers
        steps.pop(0)
        
        print("in post continue", file = sys.stderr)
        return render_template(
            'TransferProcess.html',
            ship=ship_data,
            current_operation=current_operation,
            total_operations=total_operations,
            action = action
        )

    #if len(steps) > 0
    # if request.method == "POST":
    #     container_name = request.form.get('container_name')
    #     container_weight = request.form.get('container_weight')

    #     if not container_name or not container_weight:
    #         return render_template(
    #             'TransferProcess.html',
    #             ship=ship_data,
    #             current_operation=current_operation,
    #             total_operations=total_operations,
    #             error="Name and weight are required."
    #         )

    #     try:
    #         container_weight = float(container_weight)  
    #     except ValueError:
    #         return render_template(
    #             'TransferProcess.html',
    #             ship=ship_data,
    #             current_operation=current_operation,
    #             total_operations=total_operations,
    #             error="Weight must be a valid number."
    #         )

    #     if container_weight < 0:
    #         print(f"Negative weight ({container_weight}) entered. Adjusting to 0.", file=sys.stderr)
    #         container_weight = 0  
    #     elif container_weight > 9999:
    #         print(f"Weight ({container_weight}) exceeds 9999. Adjusting to 9999.", file=sys.stderr)
    #         container_weight = 9999 
    #     else:
    #         container_weight = round(container_weight) 

    #     if current_operation <= len(ship_data):
    #         ship_data[current_operation - 1].name = container_name
    #         ship_data[current_operation - 1].weight = f"{int(container_weight):05}"  # Format as 5-digit number

    #     current_operation += 1
    #     if current_operation > total_operations:
    #         return redirect(url_for('success'))

    return render_template(
        'TransferProcess.html',
        ship=ship_data,
        current_operation=current_operation,
        total_operations=total_operations,
        action = action
    )

#def transfer_process_on():

#IMPORTANT KEEP THIS TO HANDLE WHICH CONTAINERS SELECTED
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

#@app.route('/Transfer-path', methods = ["GET", "POST"])
#def path():
#    return

@app.route('/Transfer-comingoff', methods = ["GET", "POST"])
def comingoff():
    return render_template('comingoff.html', fileUploaded = DataStore.fileName, ship = DataStore.ship.containers)

@app.route('/FileSelect', methods=['GET', 'POST'])
def checkAction():
    print("In check action", file=sys.stderr)
    if request.method == "POST":
        DataStore.selectOption = request.form['TypeAction']
        print(f"The action selected is: {DataStore.selectOption}", file=sys.stderr)
        log(DataStore.selectOption + 'was selected by operator')
        return redirect(url_for('fileUpload'))
    return render_template('FileSelect.html')

@app.route('/Balance', methods=["GET", "POST"])
def Balance():
    if request.method == "POST":
        print("Balance algorithm triggered", file=sys.stderr)
        return redirect(url_for('success')) 
    return render_template('Balance.html', ship=DataStore.ship.containers)

@app.route('/typeFile', methods=['GET', 'POST'])
def fileUpload():
    print("In fileUpload", file=sys.stderr)
    if request.method == "POST":
        file = request.files.get('file')
        if file:
            DataStore.fileName = file.filename
            file.save(file.filename)
            print(f"File {file.filename} uploaded successfully", file=sys.stderr)
            DataStore.ship.loadGrid(DataStore.fileName)
        if DataStore.selectOption == "Balance":
            return redirect(url_for('Balance'))
        elif DataStore.selectOption == "Transfer":
            return redirect(url_for('comingoff'))

    return redirect(url_for('checkAction'))

@app.route('/Success', methods=["GET"])
def success():
    return render_template('Success.html')