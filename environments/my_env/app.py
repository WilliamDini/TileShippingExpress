from flask import Flask, render_template, request, redirect, url_for, jsonify, session, g
import sys
from grid import *
from Transfer import *
from Transfer import Problem
from datetime import datetime, timezone
from Balance import balance, readFileInput
import os
import pytz
import pickle
import atexit
import time
import threading
import copy

app = Flask(__name__)
app.secret_key = 'DrKeoghRocks'
log_file = 'logfile.log'
state_file = 'program_state.pkl'
STATE_FILE = "test_state.pkl"
class DataStore():
    selectOption = "not set"
    ship = Ship()
    fileName = "not set"
    shipChanges = []
    problem = None
    transfer = None
    manifest_content = None
    contOffArr = []
    action = ""
    masterPathArray = []
    steps = []
    current_operation = 0
    total_operations = 0
    num_containers_to_load = 0
    num_containers_to_remove = 0
    tempContainerArray = []
    iteration = 1
    prevAction = ""
    noLoadLeft = 0
    loadContinue = 0
    prevMove = 0
    moveOffLeft = 0
    currOpAdded = False
    balanceEnd = False
    balanceCost = 0

    def __getstate__(self):
        state = self.__dict__.copy()
        if "problem" in state:
            state["problem"] = None
        if "transfer" in state:
            state["transfer"] = None
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

state_lock = threading.Lock()

def save_state():
    state = {
        "fileName": DataStore.fileName,
        "containers": DataStore.ship.containers, 
        "manifest_content": DataStore.manifest_content,
    }
    with open(state_file, 'wb') as f:
        pickle.dump(state, f)
    print(f"Autosave: {len(DataStore.ship.containers)} containers saved.", file=sys.stderr)

def load_state():
    with state_lock:
        global DataStore
        try:
            with open(state_file, 'rb') as f:
                state = pickle.load(f)
                DataStore.fileName = state.get("fileName", "not set")
                DataStore.manifest_content = state.get("manifest_content", None)
                saved_containers = state.get("containers", [])

                if saved_containers:
                    DataStore.ship.containers = saved_containers
                    print(f"State restored: {len(DataStore.ship.containers)} containers.", file=sys.stderr)
                else:
                    print("No containers found in saved state.", file=sys.stderr)
        except Exception as e:
            print(f"Error loading state: {e}", file=sys.stderr)

def save_periodically():
    save_state()

def autosave():
    while True:
        time.sleep(15)
        with state_lock:
            save_state()

autosave_thread = threading.Thread(target=autosave, daemon=True)
autosave_thread.start()

@app.before_request
def initialize_app():
    global DataStore
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "rb") as f:
                DataStore.ship = pickle.load(f)
            print(f"Ship state restored from {STATE_FILE}", file=sys.stderr)
        else:
            print("No saved ship state found, initializing with default ship.", file=sys.stderr)
    except Exception as e:
        print(f"Error restoring ship state: {e}", file=sys.stderr)

def test_serialization(uploaded_file=None):
    ship = Ship()
    
    if uploaded_file:
        # Load grid from the uploaded file
        print(f"Loading grid from uploaded file: {uploaded_file}", file=sys.stderr)
        ship.loadGrid(uploaded_file)
        
        # Save the state to the file
        with open(STATE_FILE, "wb") as f:
            pickle.dump(ship, f)
        print("Ship state saved after uploading the file.", file=sys.stderr)
    elif os.path.exists(STATE_FILE):
        # Restore the ship's state from the saved file
        with open(STATE_FILE, "rb") as f:
            ship = pickle.load(f)
        print("Restored ship state from saved file.", file=sys.stderr)
    else:
        # If no uploaded file or saved state, raise an error or handle accordingly
        raise FileNotFoundError("No uploaded file or saved state found. Unable to initialize the ship.")
    
    return ship

pacific_tz = pytz.timezone('US/Pacific')

def log(append_str):
    pacific_time = datetime.now(pacific_tz).strftime('%Y-%m-%d %H:%M')
    with open(log_file, 'a') as f:
        f.write(pacific_time + ' ' + append_str + '\n')

@app.route('/', methods = ["GET", "POST"])
def Login():
    if request.method == "POST":
        user = request.form.get('user', 'Guest') 
        session['user'] = user 
        log(f"{user} has logged in.")
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
        if num_containers == 1:
            num_containers = 1
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
        DataStore.num_containers_to_remove = num_to_unload
        DataStore.total_operations = DataStore.num_containers_to_load + DataStore.num_containers_to_remove
        if len(DataStore.shipChanges) == 0 and DataStore.num_containers_to_load > 0:
            DataStore.action = "On"

        #changed redirect from "transfer_process"
        return redirect(url_for('transfer_process_init', current=1, moveTo="none"))

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
            new_manifest_content = DataStore.ship.generate_manifest_content()
            new_manifest_filename = f"{DataStore.fileName.split('.')[0]}OUTBOUND.txt"
            new_manifest_path = os.path.join(app.root_path, new_manifest_filename)
        
        # Save the new manifest to a file
            with open(new_manifest_path, 'w') as f:
                f.write(new_manifest_content)
        
        # Save the new manifest filename in the session for download
        session['new_manifest_filename'] = new_manifest_filename
        return redirect(url_for('success'))

    return render_template(
        'TransferProcess.html',
        ship=ship_data,
        current_operation=current_operation,
        total_operations=total_operations
    )

@app.before_request
def before_request():
    if request.endpoint == "/Transfer-process-Off":
        g.total_operations = 0
        g.ship_data = DataStore.ship.containers
        g.current_operation = 0

@app.route('/Transfer-process-Off', methods=["GET", "POST"])
def transfer_process_init():
    print("in process init", file=sys.stderr)
    print("num cont to Load " + str(DataStore.num_containers_to_load))
    moveTo = request.args.get("moveTo")
    DataStore.current_operation = request.args.get("current", type=int)
    
    if DataStore.current_operation is None:
        DataStore.current_operation = 1

    # Ensure current_operation is set to 1 if it's the first iteration
    if DataStore.iteration == 1 and DataStore.current_operation == 0:
        DataStore.current_operation = 1

    if len(DataStore.steps) > 0:
        print("in beginning action = off")
        DataStore.action = "Off"
    
    if len(DataStore.steps) == 0 and DataStore.action == "Off" and DataStore.prevAction != "On":
        print("change to off")
        DataStore.prevAction = "Off"

    if len(DataStore.steps) == 0 and DataStore.num_containers_to_load == 0 and DataStore.prevAction != "Off":
        DataStore.currOpAdded = False

    print("steps length: " + str(len(DataStore.steps)))
    print(DataStore.currOpAdded)
    if len(DataStore.steps) == 0 and DataStore.currOpAdded == False and DataStore.iteration > 1:
        print("add one to current op when no steps")
        DataStore.currOpAdded = True
        if DataStore.current_operation < DataStore.total_operations:
            DataStore.current_operation += 1

    print("current operation: " + str(DataStore.current_operation) + " out of " + str(DataStore.total_operations))
    if (DataStore.current_operation == DataStore.total_operations and len(DataStore.steps) == 0 and DataStore.num_containers_to_load == 0 and DataStore.num_containers_to_remove == 0) or DataStore.current_operation > DataStore.total_operations:
        DataStore.ship.containers = copy.deepcopy(DataStore.tempContainerArray)
        new_manifest_content = DataStore.ship.generate_manifest_content()
        new_manifest_filename = f"{DataStore.fileName.split('.')[0]}OUTBOUND.txt"
        new_manifest_path = os.path.join(app.root_path, new_manifest_filename)
        
        with open(new_manifest_path, 'w') as f:
            f.write(new_manifest_content)
        
        session['new_manifest_filename'] = new_manifest_filename
        return redirect(url_for('success'))
    elif DataStore.total_operations == 0:
        DataStore.ship.containers = copy.deepcopy(DataStore.tempContainerArray)
        new_manifest_content = DataStore.ship.generate_manifest_content()
        new_manifest_filename = f"{DataStore.fileName.split('.')[0]}OUTBOUND.txt"
        new_manifest_path = os.path.join(app.root_path, new_manifest_filename)
        
        # Save the new manifest to a file
        with open(new_manifest_path, 'w') as f:
            f.write(new_manifest_content)
        
        # Save the new manifest filename in the session for download
        session['new_manifest_filename'] = new_manifest_filename
        return redirect(url_for('success'))

    if DataStore.num_containers_to_load == 0:
        print("in no load left")
        DataStore.noLoadLeft = 1
        moveTo = "Off"

    print("moveTo " + moveTo)
    print("action " + DataStore.action)
    print(DataStore.num_containers_to_load)
    print(DataStore.prevAction)
    print("num steps: " + str(len(DataStore.steps)))
    print("contOffAr: " + str(len(DataStore.contOffArr)))

    if moveTo == "Off" and DataStore.action == "Off" and DataStore.num_containers_to_load > 0 and len(DataStore.contOffArr) == 0 and DataStore.prevAction == "On":
        print("in this")
        moveTo = "On"

    if len(DataStore.steps) == 0 and DataStore.num_containers_to_load > 0 and DataStore.iteration > 1 and DataStore.prevAction == "Off":
        print("there are no steps, changing to coming on")
        moveTo = "On"

    if moveTo == "On" or (DataStore.num_containers_to_remove == 0 and moveTo == "On" and DataStore.num_containers_to_load > 0 ):
        print("in no containers to remove, putting on")
        for i in range(len(DataStore.tempContainerArray)):
            DataStore.tempContainerArray[i].action = "x"
        if DataStore.loadContinue == 1:
            DataStore.num_containers_to_load -= 1
        DataStore.prevMove = 0
        if(DataStore.prevAction == "On"):
            DataStore.prevAction = ""
        return transfer_process_on()

    print(len(DataStore.steps))
    if moveTo == "Off" and len(DataStore.steps) > 0:
        print("continuing steps")
        DataStore.prevMove = 1
        return transfer_process_off_cont()

    if moveTo == "Off":
        if len(DataStore.tempContainerArray) > 0:
            for i in range(len(DataStore.tempContainerArray)):
                if DataStore.tempContainerArray[i].xPos == 1 and DataStore.tempContainerArray[i].yPos == 1 and DataStore.tempContainerArray[i].name != "UNUSED":
                    print("found container: " + DataStore.tempContainerArray[i].name)
                    DataStore.tempContainerArray[i].name = "UNUSED"
                    DataStore.tempContainerArray[i].weight = "00000"
                    DataStore.problem.pathContainers[i].name = "UNUSED"
                    DataStore.problem.pathContainers[i].weight = "00000"
            DataStore.transfer.nestedArray[0][0].name = "UNUSED"
            DataStore.transfer.nestedArray[0][0].weight = "00000"

    for i in range(len(DataStore.tempContainerArray)):
        DataStore.tempContainerArray[i].action = "x"

    print("past moveTo checks")

    if len(DataStore.shipChanges) > 0 and DataStore.iteration == 1:
        print("adding containers to remove")
        DataStore.num_containers_to_remove = len(DataStore.shipChanges)
        DataStore.action = "Off"
        for element in DataStore.shipChanges:
            temp = element.split("_")
            DataStore.contOffArr.append(temp[1])
        print(DataStore.contOffArr, file=sys.stderr)
    
    if DataStore.iteration == 1:
        print("in iteration = 1")
        DataStore.tempContainerArray = copy.deepcopy(DataStore.ship.containers)
        DataStore.problem = Problem(DataStore.tempContainerArray)
        print(DataStore.shipChanges, file=sys.stderr)
        DataStore.problem.loadNestedContainers()
        DataStore.problem.printShipContNested()
        DataStore.transfer = Transfer(DataStore.problem.shipContNested, DataStore.problem.shipContainers)

    if len(DataStore.contOffArr) > 0:
        for element in DataStore.problem.shipContainers:
            if(element.name == DataStore.contOffArr[0]):
                container = element

        pathArray = []
        if DataStore.iteration > 1:
            for i in range(len(DataStore.tempContainerArray)):
                if DataStore.tempContainerArray[i].xPos == 1 and DataStore.tempContainerArray[i].yPos == 1 and DataStore.tempContainerArray[i].name != "UNUSED":
                    print("found container: " + DataStore.tempContainerArray[i].name)
                    DataStore.tempContainerArray[i].name = "UNUSED"
                    DataStore.tempContainerArray[i].weight = "00000"
                    DataStore.problem.pathContainers[i].name = "UNUSED"
                    DataStore.problem.pathContainers[i].weight = "00000"
            DataStore.transfer.nestedArray[0][0].name = "UNUSED"
            DataStore.transfer.nestedArray[0][0].weight = "00000"
        pathArray = DataStore.transfer.moveContainerOff(container, [])

        DataStore.masterPathArray = []
        for element in pathArray:
            if type(element) != list:
                DataStore.masterPathArray.append(element)
    
        print("path is: ", file=sys.stderr)
        if(DataStore.masterPathArray == None):
            print("No path available", file=sys.stderr)
        else:
            for element in DataStore.masterPathArray:
                print(element, file=sys.stderr)

        if len(DataStore.steps) == 0:
            DataStore.steps = DataStore.problem.returnPathArray(DataStore.masterPathArray)
            DataStore.tempContainerArray = copy.deepcopy(DataStore.steps[0])
            print("pop step from init")
            DataStore.steps.pop(0)
        else:
            print(len(DataStore.steps), file=sys.stderr)
            DataStore.tempContainerArray = copy.deepcopy(DataStore.steps[0])
            print("in else pop")
            DataStore.steps.pop(0)
        print("length of steps: " + str(len(DataStore.steps)))
        DataStore.contOffArr.pop(0)
        print("contArray: ")
        print(DataStore.contOffArr)
        DataStore.shipChanges.pop(0)
        DataStore.num_containers_to_remove -= 1
        if DataStore.num_containers_to_remove > 0 and DataStore.num_containers_to_load == 0:
            DataStore.moveOffLeft = 1

    if(DataStore.iteration > 1) or len(DataStore.steps) > 0:
        DataStore.action = "Off"
    print("action: " + DataStore.action)

    if DataStore.iteration == 1 or len(DataStore.steps) > 0:
        DataStore.prevAction = ""
    
    if len(DataStore.steps) == 0:
        print("in datastore steps = 0")
        DataStore.prevAction = "Off"
        DataStore.currOpAdded = True
        # if DataStore.current_operation < DataStore.total_operations:
        #     DataStore.current_operation += 1  # Increment current_operation here
    
    DataStore.iteration += 1

    # Check if only one container is being loaded and terminate correctly
    if DataStore.num_containers_to_load == 1 and DataStore.current_operation == DataStore.total_operations and DataStore.action == "On":
        return transfer_process_on()

    return render_template(
            'TransferProcess.html',
            ship=DataStore.tempContainerArray,
            current_operation=DataStore.current_operation,
            total_operations=DataStore.total_operations,
            action=DataStore.action,
            prevAction=DataStore.prevAction,
            numContRemove=DataStore.num_containers_to_remove,
            numLoad=DataStore.num_containers_to_load
        )

def transfer_process_on():
    print("in transfer process on", file = sys.stderr)
    if request.method == "POST":
        print("in post method", file = sys.stderr)
        container_name = request.form.get('container_name')
        container_weight = request.form.get('container_weight')

        print(container_name + container_weight, file = sys.stderr)

        if not container_name or not container_weight:
            DataStore.prevAction = ""
            return render_template(
                'TransferProcess.html',
                ship=DataStore.tempContainerArray,
                current_operation=DataStore.current_operation,
                total_operations=DataStore.total_operations,
                action = DataStore.action,
                error="Name and weight are required.",
                prevAction = DataStore.prevAction,
                numContRemove = DataStore.num_containers_to_remove,
                numLoad = DataStore.num_containers_to_load
            )

        try:
            container_weight = float(container_weight)  
        except ValueError:
            DataStore.prevAction = ""
            return render_template(
                'TransferProcess.html',
                ship=DataStore.tempContainerArray,
                current_operation=DataStore.current_operation,
                total_operations=DataStore.total_operations,
                action = DataStore.action,
                error="Weight must be a valid number.",
                prevAction = DataStore.prevAction,
                numContRemove = DataStore.num_containers_to_remove,
                numLoad = DataStore.num_containers_to_load
            )

        if container_weight < 0:
            print(f"Negative weight ({container_weight}) entered. Adjusting to 0.", file=sys.stderr)
            container_weight = 0  
        elif container_weight > 99999:
            print(f"Weight ({container_weight}) exceeds 99999. Adjusting to 99999.", file=sys.stderr)
            container_weight = 99999 
        else:
            container_weight = round(container_weight) 

        if len(str(container_weight)) < 5:
            contString = copy.deepcopy(str(container_weight))
            for i in range(5 - len(str(container_weight))):
                contString = "0" + contString

        print(len(DataStore.tempContainerArray))
        if len(DataStore.tempContainerArray) > 0:
            for i in range(len(DataStore.tempContainerArray)):
                if DataStore.tempContainerArray[i].xPos == 1 and DataStore.tempContainerArray[i].yPos == 1:
                    print("found container: " + DataStore.tempContainerArray[i].name)
                    DataStore.tempContainerArray[i].name = "UNUSED"
                    DataStore.tempContainerArray[i].weight = "00000"

        print(contString + " " + container_name)

        DataStore.problem.shipContainers = copy.deepcopy(DataStore.tempContainerArray)
        DataStore.transfer.nestedArray[0][0].name = "UNUSED"
        DataStore.transfer.nestedArray[0][0].weight = "00000"

        newPathArray = DataStore.transfer.moveContainerOn(contString, container_name, [])
        DataStore.masterPathArray = []
        print(type(newPathArray))
        for element in newPathArray:
            if type(element) != list:
                DataStore.masterPathArray.append(element)
        print(DataStore.masterPathArray)
        
        print("path is: ", file = sys.stderr)
        if(DataStore.masterPathArray == None):
            print("No path available", file = sys.stderr)
        else:
            for element in DataStore.masterPathArray:
                print(element, file = sys.stderr)

        print(type(DataStore.problem.pathContainers[0]))
        DataStore.problem.pathContainers[0] = Container(1, 1, contString, container_name, 0, "x", False)
        DataStore.steps = DataStore.problem.returnPathArray(DataStore.masterPathArray)
        print(len(DataStore.steps[0]), file = sys.stderr)
        DataStore.tempContainerArray = copy.deepcopy(DataStore.steps[0])
        
        if len(DataStore.steps)> 0:
            DataStore.steps.pop(0)
        
        DataStore.loadContinue = 1
        DataStore.iteration += 1
        DataStore.action = "Off"
        DataStore.prevAction = "On"
        DataStore.currOpAdded = False
        print("at submit, choice: action-" + DataStore.action + " prev-" + DataStore.prevAction)
        return render_template(
            'TransferProcess.html',
            ship=DataStore.tempContainerArray,
            current_operation=DataStore.current_operation,
            total_operations=DataStore.total_operations,
            action = DataStore.action,
            prevAction = DataStore.prevAction,
            numContRemove = DataStore.num_containers_to_remove,
            numLoad = DataStore.num_containers_to_load
        )
    DataStore.loadContinue = 0
    DataStore.action = "On"
    return render_template(
        'TransferProcess.html',
        ship=DataStore.tempContainerArray,
        current_operation=DataStore.current_operation,
        total_operations=DataStore.total_operations,
        action = DataStore.action,
        prevAction = DataStore.prevAction,
        numContRemove = DataStore.num_containers_to_remove,
        numLoad = DataStore.num_containers_to_load
    )

def transfer_process_off_cont():
    current_operation = request.args.get("current", 1, type=int)
    print("in transfer_process_off_cont", file=sys.stderr)

    if len(DataStore.steps) > 0:
        DataStore.tempContainerArray = copy.deepcopy(DataStore.steps[0])
        print("pop step from off cont")
        DataStore.steps.pop(0)
        print("remaining steps: " + str(len(DataStore.steps)), file=sys.stderr)

        # Update the container being unloaded
        if DataStore.tempContainerArray:
            for container in DataStore.tempContainerArray:
                if container.name != "UNUSED":
                    print(f"Unloading container: {container.name} at ({container.xPos}, {container.yPos})", file=sys.stderr)
                    container.name = "UNUSED"
                    container.weight = "00000"

        if len(DataStore.steps) == 0:
            DataStore.currOpAdded = False
    else:
        print("changing currOp to false in off cont")
        DataStore.currOpAdded = False

    DataStore.prevAction = ""
    return render_template(
        'TransferProcess.html',
        ship=DataStore.tempContainerArray,
        current_operation=DataStore.current_operation,
        total_operations=DataStore.total_operations,
        action=DataStore.action,
        prevAction=DataStore.prevAction,
        numContRemove=DataStore.num_containers_to_remove
    )

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


@app.route('/Transfer-comingoff', methods=["GET", "POST"])
def comingoff():
    if not DataStore.ship.containers:
        print("No containers available in DataStore.ship.containers.", file=sys.stderr)
    else:
        print(f"Containers available: {len(DataStore.ship.containers)}", file=sys.stderr)
        #for container in DataStore.ship.containers:
            #print(f"Container Info: {container.name} at ({container.xPos}, {container.yPos})", file=sys.stderr)
    return render_template('comingoff.html', fileUploaded=DataStore.fileName, ship=DataStore.ship.containers)


@app.route('/FileSelect', methods=['GET', 'POST'])
def checkAction():
    print("In check action", file=sys.stderr)
    if request.method == "POST":
        DataStore.selectOption = request.form['TypeAction']
        print(f"The action selected is: {DataStore.selectOption}", file=sys.stderr)
        log(DataStore.selectOption + ' was selected by operator.')
        return redirect(url_for('fileUpload'))
    return render_template('FileSelect.html')

@app.route('/Balance', methods=["GET", "POST"])
def Balance():
    if len(DataStore.steps) > 0:
        return balance_process_cont()

    if len(DataStore.steps) == 0 and DataStore.balanceEnd == True:
        return redirect(url_for('success'))

    if request.method == "POST":
        if(request.args.get("moveTo") == "next") and len(DataStore.steps) > 0:
            print("continuing steps")
            return balance_process_cont()
            
        log("Balance algorithm triggered.")
        print("Balance algorithm triggered", file=sys.stderr)
        r, g = readFileInput(DataStore.fileName)
        
        # Perform the balance algorithm
        try:
            movements, cost = balance(r, g) #problem?
            movements.reverse()
            
            DataStore.balanceCost = cost

            index = 0
            moveInOrder = []
            for element in movements:
                temp = element.split()
                if(temp[3] == "UNUSED"):
                    moveInOrder.insert(index, element)
                    index += 1
                else:
                    moveInOrder.insert(index, element)
                    index = 0

            print("correct order")
            for element in moveInOrder:
                print(element)

            print("reversed order")
            for element in movements:
                print(element)
            if not movements:
                return render_template(
                    'Balance.html',
                    ship=DataStore.ship.containers,
                    message="Ship is already balanced!"
                )

            for element in movements:
                print(type(element))
            if len(DataStore.steps) == 0:
                DataStore.tempContainerArray = copy.deepcopy(DataStore.ship.containers)
                DataStore.problem = Problem(DataStore.tempContainerArray)
                DataStore.problem.loadNestedContainers()
                DataStore.steps = DataStore.problem.returnPathArray(moveInOrder)
                print("after steps")
                print(len(DataStore.steps))
                DataStore.tempContainerArray = copy.deepcopy(DataStore.steps[0])
                print("pop step from init")
                DataStore.steps.pop(0)

            return render_template(
                'Balance.html',
                ship=DataStore.tempContainerArray,
                current_operation=DataStore.current_operation,
                total_operations=DataStore.total_operations,
                movements=movements,
                cost=DataStore.balanceCost,
                action = "continue",
                message="Balance algorithm completed successfully!"
            )
        except Exception as e:
            print(f"Error during balance computation: {e}", file=sys.stderr)
            print(f"Metadata: {r}", file=sys.stderr)
            print(f"Ship Grid: {g}", file=sys.stderr)
            return render_template('Error.html', error=f"Balance algorithm failed: {e}")

    # Render the initial balance page
    return render_template('Balance.html', 
                           ship=DataStore.ship.containers,
                           current_operation = DataStore.current_operation,
                           cost = DataStore.balanceCost,
                           action = "start")

def balance_process_cont():
    print("in balance process cont")
    if len(DataStore.steps) > 0:
        DataStore.tempContainerArray = copy.deepcopy(DataStore.steps[0])
        print("pop step from balance cont")
        DataStore.steps.pop(0)
        print("remaining steps: " + str(len(DataStore.steps)), file = sys.stderr)
    else:
        print("no steps")

    if len(DataStore.steps) == 0:
        DataStore.action = "end"
        DataStore.balanceEnd = True
    else:
        DataStore.action = "continue"

    print(DataStore.action)

    return render_template(
            'Balance.html',
            ship=DataStore.tempContainerArray,
            current_operation=DataStore.current_operation,
            total_operations=DataStore.total_operations,
            action = str(DataStore.action),
            cost = DataStore.balanceCost,
            message = "Continuing algorithm"
        )


@app.route('/get_movements', methods=["GET"])
def get_movements():
    movements = session.get('movements', [])
    return jsonify({"movements": movements})


@app.route('/typeFile', methods=['GET', 'POST'])
def fileUpload():
    print("In fileUpload", file=sys.stderr)
    if request.method == "POST":
        file = request.files.get('file')
        if file:
            DataStore.fileName = file.filename
            DataStore.manifest_content = file.read().decode('utf-8')
            file.seek(0)
            file.save(file.filename)
            print(f"File {file.filename} uploaded successfully", file=sys.stderr)
            log(file.filename + ' was uploaded')

            try:
                DataStore.ship.loadGrid(DataStore.fileName)
                DataStore.ship.printContainers()

                with open(STATE_FILE, "wb") as f:
                    pickle.dump(DataStore.ship, f)

                save_state()

                print(f"Ship state saved to {STATE_FILE}", file=sys.stderr)
                print(f"DataStore.fileName: {DataStore.fileName}", file=sys.stderr)
            except Exception as e:
                print(f"Error loading grid: {e}", file=sys.stderr)
                return render_template('Error.html', error=f"Failed to load the grid: {e}")

        if DataStore.selectOption == "Balance":
            return redirect(url_for('Balance'))
        elif DataStore.selectOption == "Transfer":
            return redirect(url_for('comingoff'))

    return redirect(url_for('checkAction'))




@app.route('/log_comment', methods=["POST"])
def log_comment():
    print("in log comment", file = sys.stderr)
    data = request.get_json()
    comment = data.get("comment") if data else None
    print(comment, file = sys.stderr)
    if comment:
        log(f"User comment: {comment}")
        print(f"Comment logged: {comment}", file=sys.stderr)
        return jsonify({"status": "success", "message": "Comment logged successfully"})
    return jsonify({"status": "error", "message": "No comment provided."}), 400



@app.route('/Success', methods=["GET"])
def success():
    new_manifest_filename = session.get('new_manifest_filename', None)
    return render_template('Success.html')

if __name__ == "__main__":
    if os.path.exists(state_file):
        try:
            load_state()
        except Exception as e:
            print(f"Error loading state file: {e}", file=sys.stderr)
    else:
        print("State file not found. Starting with a clean state.", file=sys.stderr)

    if not os.path.exists(log_file):
        print("Log file not found. Creating a new log file.", file=sys.stderr)
        with open(log_file, 'w') as f:
            f.write("Log file initialized on " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
    else:
        print("Log file found. Appending to existing log file.", file=sys.stderr)

    app.run(debug=True)

# PLACE LINE 60 IN TransferProcess.html
# <!-- {% if action == "Off" or (action == "Off" and current_operation == total_operations) or (action == "On" and numLoad == 0) or (action == "On" and current_operation == total_operations) %} -->
