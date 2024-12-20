# grid.py
import array
import sys
#from Transfer import *

class Container():
    def __init__(self, xPos, yPos, weight, name, id, action, prevPath):
        self.xPos = xPos
        self.yPos = yPos
        self.weight = weight
        self.name = name
        self.id = id
        self.action = action
        self.prevPath = prevPath
    
    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__.update(state)
class Ship():
    def __init__(self):
        #self.Containers = Containers
        self.containers = []

    def __getstate__(self):
        return {"containers": self.containers}

    def __setstate__(self, state):
        self.containers = state.get("containers", [])

    def generate_manifest_content(self):
        manifest_lines = []
        max_y = max(container.yPos for container in self.containers) 

        for adjusted_yPos in range(1, max_y + 1):
            original_yPos = max_y - adjusted_yPos + 1

            for container in sorted(self.containers, key=lambda c: c.xPos):
                if container.yPos == original_yPos:
                    line = f"[{adjusted_yPos:02},{container.xPos:02}], {{{container.weight}}}, {container.name}\n"
                    manifest_lines.append(line)

        return ''.join(manifest_lines)

     
    def loadGrid(self, fileName):
        self.containers.clear()
        print(f"Loading grid from file: {fileName}", file=sys.stderr)

        try:
            with open(fileName, "r") as file:
                lines = file.readlines()  # Read all lines to determine maximum yPos
                max_y = 0  # Track the maximum yPos

            for line in lines:
                values = line.split(" ")
                values[0] = values[0].replace("[", "").replace("]", "")
                y = int(values[0][0:2])
                if y > max_y:
                    max_y = y

            with open(fileName, "r") as file:
                line = file.readline()
                index = 0
                while line:
                    # Split line by space into array in variable values
                    values = line.split(" ")

                    # Replace unnecessary characters and place into corresponding variables
                    values[0] = values[0].replace("[", "").replace("]", "")
                    original_y = int(values[0][0:2])
                    x = int(values[0][3:5])
                    
                    y = max_y - original_y + 1

                    values[1] = values[1].replace("{","").replace("}","").replace(",","")
                    values[2] = values[2].replace("\n","")
                    weight = values[1]
                    name = values[2]
                    
                    # Add container(structs) to containers array in ship class
                    container = Container(x, y, weight, name, index, "x", False)
                    self.containers.append(container)
                    print(f"Loaded container: {container.name} at ({container.xPos}, {container.yPos}) with weight {container.weight}", file=sys.stderr)
                    index = index + 1
                    line = file.readline()
            self.containers.sort(key=lambda c: (c.yPos, c.xPos))
            print(f"Total containers loaded: {len(self.containers)}", file=sys.stderr)

        except Exception as e:
            print(f"Error loading grid: {e}", file=sys.stderr)


    def printContainers(self):
        if len(self.containers) > 0:
            for container in self.containers:
                print("Container Info: XPOS:" + str(container.xPos) 
                                    + " YPOS:" + str(container.yPos) 
                                    + " Weight:" + container.weight
                                    + " Name:" + container.name, file=sys.stderr)

# newShip = Ship()
# newShip.loadGrid("ShipCase1.txt")
# problem = Problem(newShip.containers)
#transfer = Transfer()

#containerArray = []
#newShip = Ship()
#newShip.loadGrid("ShipCase1.txt")
#newShip.printContainers()


