# grid.py

class Container():
    def __init__(self, xPos, yPos, weight, name):
        self.xPos = xPos
        self.yPos = yPos
        self.weight = weight
        self.name = name

class Ship():
    def __init__(self, Containers):
        self.Containers = Containers

def loadGrid(fileName):
    print(fileName)
    with open(fileName, "r") as file:
        line = file.readline()
        while line:
            print(line.strip())
            line = file.readline()

loadGrid("ShipCase1.txt")

