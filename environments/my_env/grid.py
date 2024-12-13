# grid.py
import array
import sys
from Transfer import *

class Container():
    def __init__(self, xPos, yPos, weight, name, id, action, prevPath):
        self.xPos = xPos
        self.yPos = yPos
        self.weight = weight
        self.name = name
        self.id = id
        self.action = action
        self.prevPath = prevPath

class Ship():
    def __init__(self):
        #self.Containers = Containers
        self.containers = []

    def loadGrid(self, fileName):
        self.containers.clear()

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
                #split line by space into array in variable values
                values = line.split(" ")

                #replace unnecessary characters and place into corresponding variables
                values[0] = values[0].replace("[", "").replace("]", "")
                original_y = int(values[0][0:2])
                x = int(values[0][3:5])
                
                y = max_y - original_y + 1

                values[1] = values[1].replace("{","").replace("}","").replace(",","")
                values[2] = values[2].replace("\n","")
                weight = values[1]
                name = values[2]
                
                #add container(structs) to containers array in ship class
                self.containers.append(Container(x, y, weight, name, index, "x", False))
                index = index + 1
                line = file.readline()
        self.containers.sort(key=lambda c: (c.yPos, c.xPos))

    def printContainers(self):
        if len(self.containers) > 0:
            for container in self.containers:
                print("Container Info: XPOS:" + str(container.xPos) 
                                    + " YPOS:" + str(container.yPos) 
                                    + " Weight:" + container.weight
                                    + " Name:" + container.name, file=sys.stderr)

newShip = Ship()
newShip.loadGrid("ShipCase1.txt")
problem = Problem(newShip.containers)
#transfer = Transfer()

#containerArray = []
#newShip = Ship()
#newShip.loadGrid("ShipCase1.txt")
#newShip.printContainers()


