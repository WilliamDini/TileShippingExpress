# grid.py
import array
import sys

class Container():
    def __init__(self, xPos, yPos, weight, name, id):
        self.xPos = xPos
        self.yPos = yPos
        self.weight = weight
        self.name = name
        self.id = id

class Ship():
    def __init__(self):
        #self.Containers = Containers
        self.containers = []

    def loadGrid(self, fileName):
        #print(fileName)
        with open(fileName, "r") as file:
            line = file.readline()
            index = 0
            while line:
                #split line by space into array in variable values
                values = line.split(" ")

                #replace unnecessary characters and place into corresponding variables
                values[0] = values[0].replace("[", "").replace("]", "")
                y = values[0][0:2]
                x = values[0][3:5]
                
                values[1] = values[1].replace("{","").replace("}","").replace(",","")
                values[2] = values[2].replace("\n","")
                weight = values[1]
                name = values[2]
                
                #add container(structs) to containers array in ship class
                self.containers.insert(0, Container(x, y, weight, name, index))
                index = index + 1
                line = file.readline()

    def printContainers(self):
        if len(self.containers) > 0:
            for container in self.containers:
                print("Container Info: XPOS:" + container.xPos 
                                    + " YPOS:" + container.yPos 
                                    + " Weight:" + container.weight
                                    + " Name:" + container.name, file=sys.stderr)

#containerArray = []
#newShip = Ship()
#newShip.loadGrid("ShipCase1.txt")
#newShip.printContainers()


