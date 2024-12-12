#coming off algorithm
import array
import sys
from grid import *
import math
import numpy as np
import copy
import re
import time

#path = []

class Node:
    def __init__(self, container, x, y, name):
        self.container = container
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.name = name
        self.parent = None

class Problem():
    def __init__(self, shipContainers):
        self.shipContainers = shipContainers
        self.shipContNested = []

    def loadNestedContainers(self):
        rowArray = []
        index = 0
        for container in self.shipContainers:
            print(container.name)
            if(index < 11):
                rowArray.append(container)
                #print(len(rowArray))
                index = index + 1
            else:
                rowArray.append(container)
                self.shipContNested.append(rowArray)
                rowArray = []
                index = 0
    
    def printShipContNested(self):
        
        for array in self.shipContNested:
            print("[", end = " ")
            for element in array:
                print(element.name[0:3] + str(array.index(element)), end = " ")
            print("] index = " + str(self.shipContNested.index(array)) + "\n")

class ComingOff():
    def __init__(self, shipContNested):
        self.nestedArray = shipContNested

    def calculateHeuristic(self, GoalX, GoalY, StartX, StartY):
        distance = abs(GoalX - StartX) + abs(GoalY - StartY)
        print("|" + str(GoalX) + " - " + str(StartX) + "| + |" + str(GoalY) + " - " + str(StartY) + "| = " + str(distance))
        return distance

#returns array of neighboring containers(structs)
    def findNeighbors(self, container):
        #print("inside findNeighbors")
        neighbors = []
        #print("length of nested Array = " + str(len(self.nestedArray)))
        #print(container.name + ", x = " + str(container.xPos) + ", y = " + str(container.yPos))
        #print(self.nestedArray[abs(container.yPos - 8)][container.xPos - 1].name + ", x = " + str(self.nestedArray[abs(container.yPos - 8)][container.xPos - 1].xPos) + ", y = " + str(self.nestedArray[abs(container.yPos - 8)][container.xPos - 1].yPos))
        #left side
        if(container.xPos != 1): #FIX HERE
            print(self.nestedArray[container.yPos - 1][container.xPos - 2].name + " left")
            if(self.nestedArray[container.yPos - 1][container.xPos - 2].name == "UNUSED"):
                neighbors.append(self.nestedArray[container.yPos - 1][container.xPos - 2])
        #right side
        if(container.xPos != 12):
            print(self.nestedArray[container.yPos - 1][container.xPos].name + " right")
            if(self.nestedArray[container.yPos - 1][container.xPos].name == "UNUSED"):
                neighbors.append(self.nestedArray[container.yPos - 1][container.xPos])
        #above
        if(container.yPos != 1):
            print(self.nestedArray[container.yPos - 2][container.xPos -1].name + " above")
            if(self.nestedArray[container.yPos - 2][container.xPos - 1].name == "UNUSED"):
                neighbors.append(self.nestedArray[container.yPos- 2][container.xPos - 1])
        #below
        if(container.yPos != 8):
            print(self.nestedArray[container.yPos][container.xPos - 1].name + " below")
            if(self.nestedArray[container.yPos][container.xPos - 1].name == "UNUSED"):
                neighbors.append(self.nestedArray[container.yPos][container.xPos - 1])
        
        #print("neighbors length: " + str(len(neighbors)))
        #index = 0
        #for element in neighbors:
        #    print(element.name + ", x = "  + str(element.xPos) + ", y = " + str(element.yPos))

        return neighbors

#moves blocked containers, MUST CHANGE NESTED ARRAY to reflect changes    
    def moveBlockingContainer(self, container , direction):
        self.direction = direction
        #self.path = path
        #need fix if more complex cases
        if direction == "above":
            GoalX = container.xPos
            for array in self.nestedArray:
                print("The name of observed container " + array[GoalX].name)
                if array[GoalX].name == "UNUSED":
                    continue
                else:
                    GoalY = array[GoalX].yPos - 2
                    break
        print("Goal State: x = " + str(GoalX) + ", y = " + str(GoalY))

        startNode = Node(container, container.xPos - 1, container.yPos - 1, "start")
        #path = []
        # 1) create two lists open and closed ^
        self.open = []
        self.closed = []

        # 2) evaluate current node f = g + h, then add to open list
        print("start node x and y values: x = " + str(startNode.x) + ", y = " + str(startNode.y))
        startNode.h = self.calculateHeuristic(GoalX, GoalY, startNode.x, startNode.y)
        startNode.f = startNode.g + startNode.h
    
        self.open.append(startNode)
        #for element in self.open:
        #    print(element.container.name)

        #sanity check
        iteration = 1
        # 3) loop through open list
        while(self.open):
            #check above cell
            #print("position of cell above container: x = " + str(self.nestedArray[container.yPos][container.xPos].x) + ", y = " + str(self.nestedArray[container.yPos][container.xPos].y))
            #if(self.nestedArray[container.yPos])

            #select node with lowest f score from open list
            currNode = Node(self.open[0].container, self.open[0].x, self.open[0].y, "")
            currNode.g = self.open[0].g
            currNode.h = self.open[0].h
            currNode.f = self.open[0].f
            #currNode = self.open[0]
            for element in self.open:
                if(element.f < currNode.f):
                    currNode = element
            print("lowest score f node: " + currNode.container.name + ", fscore = " + str(currNode.f) + ", x = " + str(currNode.container.xPos) + ", y = " + str(currNode.container.yPos))
            
            #check if at the goal state (x = 1, y = 1)
            if(currNode.container.xPos == GoalX + 1) and (currNode.container.yPos == GoalY + 1):
                print("in goal node check")
                while currNode:
                    print(currNode.container.name)
                    pathContainer = currNode.container
                    path.append(pathContainer)
                    currNode = currNode.parent

                #change nested container array to reflect changes in here
                self.nestedArray[container.yPos - 1][container.xPos - 1].name = "UNUSED"
                self.nestedArray[container.yPos - 1][container.xPos - 1].weight = "00000"
                self.nestedArray[GoalY][GoalX] = currNode.container

                print("array at" + str(GoalX) + str(GoalY) + "is " + self.nestedArray[GoalY][GoalX].name)

                print(len(path))
                for element in path:
                    #print(element.container.name + " " + str(element.x) + " " + str(element.y))
                    print(element.name)
                print("after checking element types in blocking container")
                #return path[::-1] #return path reversed
                return

            #move node to closed list
            self.closed.append(currNode)
            print("length of closed list: " + str(len(self.closed)))

            #pop element from open list
            print("before pop currNode from open list, length = " + str(len(self.open)))
            newOpenArray = []
            for element in self.open:
                if currNode != element:
                    newOpenArray.append(element)
            self.open = newOpenArray
            print("after pop currNode from open list, length = " + str(len(self.open)))

            
        # 4) generate neighbors
            # 4.1) for current node, generate neighboring nodes
            neighbors = self.findNeighbors(currNode.container)
            for neighbor in neighbors:

            # 4.2) ignore visited nodes (check closed list)
                if neighbor in self.closed:
                    continue

            # 4.3) calculate g h and f costs for each neighbor
                neighborNode = Node(neighbor, neighbor.xPos - 1, neighbor.yPos - 1, "neighbor")
                neighborNode.g = 1
                print("neighbor node x and y values: x = " + str(neighbor.xPos) + ", y = " + str(neighbor.yPos))
                neighborNode.h = self.calculateHeuristic(GoalX, GoalY, neighborNode.x, neighborNode.y)
                neighborNode.f = neighborNode.g + neighborNode.h
                neighborNode.parent = currNode

            # 4.4) if neighbor not in open list, add    
                if all(neighborNode.f < openNode.f for openNode in self.open if openNode.name == "neighbor"):
                    self.open.append(neighborNode)

            print("length of open: " + str(len(self.open)))
            iteration = iteration + 1
            if iteration > 3:
                break

        #account for blocked containers
        print("containerblocking: name: " + self.nestedArray[container.yPos - 2][container.xPos - 1].name + ", x = " + str(self.nestedArray[container.yPos - 2][container.xPos - 1].xPos) + ", y = " + str(self.nestedArray[container.yPos - 2][container.xPos - 1].yPos))
        path.append(self.moveBlockingContainer(self.nestedArray[abs(container.yPos - 8) - 1][container.xPos - 1], "above"))

        return None
    
    #returns path to take container off (start position to (x = 1, y = 8))
    def moveContainerOff(self, container, path):
        startNode = Node(container, container.xPos - 1, container.yPos - 1, "start")
        self.path = path

        # 1) create two lists open and closed ^
        self.open = []
        self.closed = []

        # 2) evaluate current node f = g + h, then add to open list
        print("start node x and y values: x = " + str(startNode.x) + ", y = " + str(startNode.y) + " name: " + startNode.container.name)
        startNode.h = self.calculateHeuristic(0, 0, startNode.x, startNode.y)
        startNode.f = startNode.g + startNode.h
    
        self.open.append(startNode)
        #for element in self.open:
        #    print(element.container.name)

        #sanity check
        iteration = 1
        # 3) loop through open list
        while(self.open):
            #check above cell
            #print("position of cell above container: x = " + str(self.nestedArray[container.yPos][container.xPos].x) + ", y = " + str(self.nestedArray[container.yPos][container.xPos].y))
            #if(self.nestedArray[container.yPos])

            #select node with lowest f score from open list
            currNode = Node(self.open[0].container, self.open[0].x, self.open[0].y, "")
            currNode.g = self.open[0].g
            currNode.h = self.open[0].h
            currNode.f = self.open[0].f
            #currNode = self.open[0]
            for element in self.open:
                if(element.f < currNode.f):
                    currNode = element
            print("lowest score f node: " + currNode.container.name + ", fscore = " + str(currNode.f) + ", x = " + str(currNode.container.xPos) + ", y = " + str(currNode.container.yPos))
            
            #check if at the goal state (x = 1, y = 1)
            if(currNode.container.xPos == 1) and (currNode.container.yPos == 1):
                print("in goal node check")
                while currNode:
                    print(currNode.container.name)
                    path.append(currNode)
                    currNode = currNode.parent

                print(len(path))
                for element in path:
                    #print(element.container.name + " " + str(element.x) + " " + str(element.y))
                    print(type(element))

                return path[::-1] #return path reversed

            #move node to closed list
            self.closed.append(currNode)
            print("length of closed list: " + str(len(self.closed)))

            #pop element from open list
            print("before pop currNode from open list, length = " + str(len(self.open)))
            newOpenArray = []
            for element in self.open:
                if currNode.container != element.container:
                    newOpenArray.append(element)
            self.open = newOpenArray
            print("after pop currNode from open list, length = " + str(len(self.open)))

            
        # 4) generate neighbors
            # 4.1) for current node, generate neighboring nodes
            neighbors = self.findNeighbors(currNode.container)
            for neighbor in neighbors:

            # 4.2) ignore visited nodes (check closed list)
                if neighbor in self.closed:
                    continue

            # 4.3) calculate g h and f costs for each neighbor
                neighborNode = Node(neighbor, neighbor.xPos - 1, neighbor.yPos - 1, "neighbor")
                neighborNode.g = 1
                print("neighbor node x and y values: x = " + str(neighbor.xPos) + ", y = " + str(neighbor.yPos))
                neighborNode.h = self.calculateHeuristic(0, 0, neighborNode.x, neighborNode.y)
                neighborNode.f = neighborNode.g + neighborNode.h
                neighborNode.parent = currNode
                print("parent")
                exampleNode = neighborNode
                while(exampleNode):
                    print("in tree check" + exampleNode.container.name)
                    exampleNode = exampleNode.parent

            # 4.4) if neighbor not in open list, add    
                if all(neighborNode.f < openNode.f for openNode in self.open if openNode.name == "neighbor"):
                    self.open.append(neighborNode)

            print("length of open: " + str(len(self.open)))
            iteration = iteration + 1
            #if iteration > 10:
            #    break

        #account for blocked containers
        print("containerblocking: name: " + self.nestedArray[container.yPos - 2][container.xPos - 1].name + ", x = " + str(self.nestedArray[container.yPos - 2][container.xPos - 1].xPos) + ", y = " + str(self.nestedArray[container.yPos - 2][container.xPos - 1].yPos))
        path.append(self.moveBlockingContainer(self.nestedArray[container.yPos - 2][container.xPos - 1], "above", path))
        #self.moveBlockingContainer(self.nestedArray[container.yPos - 2][container.xPos - 1], "above")
        #print(len(pathArrayAdd))
        for element in path:
            print(type(element))
        print("after running move containers")
        #self.moveContainerOff(container)

        return None
        
newShip = Ship()
newShip.loadGrid("ShipCase4.txt")
newShip.printContainers()
Problem = Problem(newShip.containers)
Problem.loadNestedContainers()
Problem.printShipContNested()
newComingOff = ComingOff(Problem.shipContNested)
for array in Problem.shipContNested:
    for element in array:
        if(element.name == "Cat"):
            container = element
pathArray = newComingOff.moveContainerOff(container, [])
print(type(pathArray))
#print(type(pathArray))

print("path is: ")
if(pathArray == None):
    print("No path available")
else:
    for element in pathArray:
        print(element.container.name + ", x = " + str(element.container.xPos) + ", y = " + str(element.container.yPos) + ", f = " + str(element.f))