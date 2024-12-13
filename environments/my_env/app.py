from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sys
from grid import *
from datetime import datetime
import os
import pickle
import atexit
import time
import threading

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
        print(f"Loading grid from uploaded file: {uploaded_file}", file=sys.stderr)
        ship.loadGrid(uploaded_file)
        
        with open(STATE_FILE, "wb") as f:
            pickle.dump(ship, f)
    elif os.path.exists(STATE_FILE):
        with open(STATE_FILE, "rb") as f:
            ship = pickle.load(f)
        print("Restored ship state from saved file", file=sys.stderr)
    else:
        print("No state found, loading default ShipCase1.txt", file=sys.stderr)
        ship.loadGrid("ShipCase1.txt")
        with open(STATE_FILE, "wb") as f:
            pickle.dump(ship, f)

    print(f"Containers in restored ship: {len(ship.containers)}", file=sys.stderr)
    ship.printContainers()
    return ship


def log(append_str):
    with open(log_file, 'a') as f:
        f.write(datetime.now().strftime('%Y-%m-%d %H:%M') + ' ' + append_str + '\n')

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

        return redirect(url_for('transfer_process', current=1))

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

def Transfer():
    return render_template('Transfer.html')

@app.route('/Transfer-comingoff', methods=["GET", "POST"])
def comingoff():
    if not DataStore.ship.containers:
        print("No containers available in DataStore.ship.containers.", file=sys.stderr)
    else:
        print(f"Containers available: {len(DataStore.ship.containers)}", file=sys.stderr)
        for container in DataStore.ship.containers:
            print(f"Container Info: {container.name} at ({container.xPos}, {container.yPos})", file=sys.stderr)
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
    if request.method == "POST":
        log("Balance algorithm triggered.")
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
    data = request.get_json()
    comment = data.get("comment") if data else None
    if comment:
        log(f"User comment: {comment}")
        print(f"Comment logged: {comment}", file=sys.stderr)
        return jsonify({"status": "success", "message": "Comment logged successfully"})
    return jsonify({"status": "error", "message": "No comment provided."}), 400



@app.route('/Success', methods=["GET"])
def success():
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
