#coming off algorithm
import array
import sys
from grid import *
import math
import numpy as np
import copy
import re
import time
import copy
import itertools

check = 0

class Node():
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
    def __init__(self):
        self.shipContainers = []

        #important, MUST DO DEEPCOPY TO COPY OG ARRAY,
        #so it does not reference same memory as shipContainers
        #self.tempShipContainers.clear()
        self.tempShipContainers = []
        self.shipContNested = []
        self.pathContNested = []
        self.pathContainers = []

    def __init__(self, shipContainers):
        self.shipContainers = shipContainers

        #important, MUST DO DEEPCOPY TO COPY OG ARRAY,
        #so it does not reference same memory as shipContainers
        #self.tempShipContainers.clear()
        self.tempShipContainers = copy.deepcopy(shipContainers)
        self.shipContNested = []
        self.pathContNested = []
        self.pathContainers = copy.deepcopy(self.shipContainers)

    def loadNestedContainers(self):
        self.shipContNested.clear()
        rowArray = []
        index = 0
        for container in self.shipContainers:
            #rint(container.name)
            if(index < 11):
                rowArray.append(container)
                #print(len(rowArray))
                index = index + 1
            else:
                rowArray.append(container)
                self.shipContNested.append(rowArray)
                rowArray = []
                index = 0
        self.pathContNested = copy.deepcopy(self.shipContNested)
    
    def loadPathNestedContainers(self):
        self.pathContNested.clear()
        rowArray = []
        index = 0
        # print("num containers= " + str(len(self.pathContainers)))
        for container in self.pathContainers:
            #print(container.name)
            if(index < 11):
                rowArray.append(copy.deepcopy(container))
                #print(len(rowArray))
                index = index + 1
            else:
                rowArray.append(copy.deepcopy(container))
                self.pathContNested.append(copy.deepcopy(rowArray))
                rowArray = []
                index = 0

    def printTempContainers(self):
        for element in self.tempShipContainers:
            print("Container: " + element.name + " xPos: " + str(element.xPos) + " yPos: " + str(element.yPos))
    
    def printShipContNested(self):
        for array in self.shipContNested:
            print("[", end = " ", file = sys.stderr)
            for element in array:
                print(element.name[0:3] + str(array.index(element)), end = " ", file = sys.stderr)
            print("] index = " + str(self.shipContNested.index(array)) + "\n", file = sys.stderr)

    def printPathContNested(self):
        for array in self.pathContNested:
            print("[", end = " ")
            for element in array:
                print(element.name[0:3] + str(array.index(element)) + element.action[0] + str(element.id), end = " ")
            print("] index = " + str(self.pathContNested.index(array)) + "\n")

    #fix to create a different array of ship() containers for each step    
    def returnPathArray(self, path):
        # print(path)
        steps = []
        print("in returnPathArray")
        arrayOfSteps = []
        arrayOfOps = []
        for element in path:
            print(element)
        for x in path:
            temp = x.split()
            if len(temp) > 4:
                longName = []
                for i in range(3, len(temp)):
                    print(temp[i])
                    longName.append(temp[i])
                    newName = " ".join(longName)

                print(newName)
                for i in range(3, len(temp)):
                    temp.pop()
                print(temp)
                temp.append(newName)
                arrayOfSteps.append(temp)
            else:    
                arrayOfSteps.append(temp)
            print(temp)
        print(arrayOfSteps)

        temp = []
        for i in arrayOfSteps:
            if i[3] == "UNUSED":
                temp.append(i)
            else:
                temp.append(i)
                arrayOfOps.append(temp)
                temp = []
        
        index = 0
        for part in arrayOfOps:
            # print("making new ship array")
            arrayOfOps[index] = arrayOfOps[index][::-1]
            # print(arrayOfOps[index])

            #working on creating a new shipContNested array -> shipContainers array for each step
            #make two variables storing start and end position of each path
            #store the rest of the points in array as middle
            for path in arrayOfOps[index]:
                if arrayOfOps[index].index(path) == 0:
                    arrayOfOps[index][arrayOfOps[index].index(path)].append("start")
                    #print("found start")
                elif arrayOfOps[index].index(path) == (len(arrayOfOps[index]) - 1):
                    arrayOfOps[index][arrayOfOps[index].index(path)].append("end")
                    #print("found end")   
                else:
                    arrayOfOps[index][arrayOfOps[index].index(path)].append("middle")

            #compare og shipContainers array with changes (start and end variables)
            #make new array set it to pathContainers array
            # print(arrayOfOps[index])
            # print(self.pathContainers[0].name)
            tempPathContainers = copy.deepcopy(self.pathContainers[::-1])
            for step in arrayOfOps[index]:
                #print(str(self.pathContainers[element.id].xPos) + " " + str(self.pathContainers[element.id].yPos))
                #temp = []
                
                #clear pathContainers action = "x"
                # for this in self.pathContainers:
                #     self.pathContainers[this.id].action = "x"

                # for thing in self.pathContainers:
                #     print(thing.name + " " + str(thing.xPos) + " " + str(thing.yPos) + " " + thing.action)
                
                #print(step)
                #print(len(arrayOfOps[index]))
                for element in tempPathContainers:
                    # print(element.name + " " +  str(element.xPos) + " " + str(element.yPos))
                    #print(step)
                    checkedFirst = False
                    if(str(self.pathContainers[element.id].xPos) == step[0]) and (str(self.pathContainers[element.id].yPos) == step[1]):
                        # print("CHECK" + self.pathContainers[element.id].name + " " + str(self.pathContainers[element.id].xPos) + " " + str(self.pathContainers[element.id].yPos) + " " + self.pathContainers[element.id].action)
                        # print("FOUND" + step[3] + " " + step[0] + " " + step[1])
                        # print("found step in pathContainers array")
                        # print("checking start")
                        # print("current step")
                        # print(step)
                        if(step[4] == "start"):
                            # print("in first")
                            # print(element.id)
                            temp = copy.deepcopy(self.pathContainers[element.id])
                            #print(self.pathContainers[element.id].name)
                            self.pathContainers[element.id].weight = "00000"
                            self.pathContainers[element.id].name = "UNUSED"
                            self.pathContainers[element.id].action = "start"
                            self.pathContainers[element.id].prevPath = True
                            break
                        elif((step[4] == "end")):
                            # print("in last")
                            # print(temp.name)
                            # print(temp.weight)
                            
                            self.pathContainers[element.id].weight = copy.deepcopy(temp.weight)
                            self.pathContainers[element.id].name = copy.deepcopy(temp.name)
                            self.pathContainers[element.id].action = "end"
                            self.pathContainers[element.id].prevPath = True
                            break
                        else:
                            #print("in middle")
                            self.pathContainers[element.id].weight = copy.deepcopy(step[2])
                            self.pathContainers[element.id].name = copy.deepcopy(step[3])
                            self.pathContainers[element.id].action = "middle"
                            self.pathContainers[element.id].prevPath = True
                            break
                        #print(self.pathContainers[element.id].name)
                # for element in 
                # print(tempPathContainers)
                #for thing in self.pathContainers:
                #    print(thing.name + " " + str(thing.xPos) + " " + str(thing.yPos) + " " + thing.action)
                #break

            #save the pathContainersArray as an element in step array
            tempPathContainers = copy.deepcopy(self.pathContainers)
            steps.append(tempPathContainers)
            
            # print("loading path and printing nested containers to check")
            self.loadPathNestedContainers()
            # self.printPathContNested()
            self.tempShipContainers = copy.deepcopy(self.pathContainers)

            for item in self.pathContainers:
                #print(item.id)
                self.pathContainers[item.id].action = "x"
            #self.pathContainers = copy.deepcopy(self.tempShipContainers)
            index = index + 1
            #break
        # print("length of steps need to take: " + str(len(steps)))
        return steps

    def returnShipArrays(self, nestedArray):
        arrayRet = []
        self.nestedArray = nestedArray
        for array in nestedArray:
            for element in array:
                arrayRet.append(element)
        arrayRet.sort(key=lambda c: (c.yPos, c.xPos))

class Transfer():
    def __init__(self, shipContNested, shipContainers):
        self.nestedArray = shipContNested
        self.shipContainers = shipContainers

    def calculateHeuristic(self, GoalX, GoalY, StartX, StartY):
        distance = abs(GoalX - StartX) + abs(GoalY - StartY)
        #print("|" + str(GoalX) + " - " + str(StartX) + "| + |" + str(GoalY) + " - " + str(StartY) + "| = " + str(distance))
        return distance

#returns array of neighboring containers(structs)
    def findNeighbors(self, container, direction):
        #print("inside findNeighbors")
        self.direction = direction
        neighbors = []
        checkAbove = 0
        #print("length of nested Array = " + str(len(self.nestedArray)))
        #print(container.name + ", x = " + str(container.xPos) + ", y = " + str(container.yPos))
        #print(self.nestedArray[abs(container.yPos - 8)][container.xPos - 1].name + ", x = " + str(self.nestedArray[abs(container.yPos - 8)][container.xPos - 1].xPos) + ", y = " + str(self.nestedArray[abs(container.yPos - 8)][container.xPos - 1].yPos))
        #left side
        if(container.xPos != 1): #FIX HERE
            #print(self.nestedArray[container.yPos - 1][container.xPos - 2].name + " left")
            if(self.nestedArray[container.yPos - 1][container.xPos - 2].name == "UNUSED"):
                neighbors.append(self.nestedArray[container.yPos - 1][container.xPos - 2])
        #right side
        if(container.xPos != 12):
            #print(self.nestedArray[container.yPos - 1][container.xPos].name + " right")
            if(self.nestedArray[container.yPos - 1][container.xPos].name == "UNUSED"):
                neighbors.append(self.nestedArray[container.yPos - 1][container.xPos])
        #above (only check if direction is above)
        if(direction == "above"):
            if(container.yPos != 1):
                #print(self.nestedArray[container.yPos - 2][container.xPos -1].name + " above")
                if(self.nestedArray[container.yPos - 2][container.xPos - 1].name == "UNUSED"):
                    neighbors.append(self.nestedArray[container.yPos- 2][container.xPos - 1])
                    checkAbove = 1
        #below
        if(container.yPos != 8):
            #print(self.nestedArray[container.yPos][container.xPos - 1].name + " below")
            if(self.nestedArray[container.yPos][container.xPos - 1].name == "UNUSED"):
                neighbors.append(self.nestedArray[container.yPos][container.xPos - 1])
        
        #print("neighbors length: " + str(len(neighbors)))
        #index = 0
        #for element in neighbors:
        #    print(element.name + ", x = "  + str(element.xPos) + ", y = " + str(element.yPos))
        if(direction == "above"):
            if neighbors != [] and checkAbove == 0 and container.yPos != 1:
                return -1
        return neighbors
    
    #returns path (ARRAY OF STRINGS: x y containerweight containername) to place container on (start position to first available slot on left side)
    def moveContainerOn(self, containerWeight, containerName, path):
        # print("Computing path for container: " + containerName + " - Coming On")

        # for element in self.shipContainers:
        #     self.shipContainers[element.id].action = "x"

        self.path = path
        self.check = check
        
        #find the first available spot on left side of ship
        GoalX = 0
        GoalY = 0
        openSpotFound = False
        # print("now here")
        while(not openSpotFound):
            if(GoalX == 12):
                path.append("ship is full")
                return path
            for array in self.nestedArray:
                #print("The name of observed container " + array[GoalX].name + " string length: " + str(len(array[GoalX].name)))
                if array[GoalX].name == "UNUSED":
                    #print("in UNUSED, container name = " + array[GoalX].name)
                    continue
                else:
                    #print("in else")
                    GoalY = array[GoalX].yPos - 2
                    openSpotFound = True
                    break
            if openSpotFound != True:
                # print("in openSpotFound check")
                GoalX = GoalX + 1
            else:
                #print("in openSpotFound else statement")
                break
        #print("Goal State: x = " + str(GoalX) + ", y = " + str(GoalY))

        self.nestedArray[0][0].name = copy.deepcopy(containerName)
        self.nestedArray[0][0].weight = copy.deepcopy(containerWeight)

        container = self.nestedArray[0][0]
        # print("This is the start container: " + container.name)
        #print("Container information: " + container.name + " " + container.weight)

        startNode = Node(container, 0, 0, "start")
        # 1) create two lists open and closed ^
        self.open = []
        self.closed = []

        # 2) evaluate current node f = g + h, then add to open list
        #print("start node x and y values: x = " + str(startNode.x) + ", y = " + str(startNode.y))
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
            currNode = self.open[0]
            for element in self.open:
                if(element.f < currNode.f):
                    currNode = element
            #print("lowest score f node: " + currNode.container.name + ", fscore = " + str(currNode.f) + ", x = " + str(currNode.container.xPos) + ", y = " + str(currNode.container.yPos))
            
            #check if at the goal state (x = 1, y = 1)
            if(currNode.container.xPos == GoalX + 1) and (currNode.container.yPos == GoalY + 1):
                # print("in goal node check")
                while currNode:
                    path.append(str(currNode.container.xPos) + " " + str(currNode.container.yPos) + " " + str(currNode.container.weight) + " " + str(currNode.container.name))
                    currNode = currNode.parent

                #print(container.name)
                #change nested container array to reflect changes in here
                #print(self.nestedArray[GoalY][GoalX].name + " " + str(self.nestedArray[GoalY][GoalX].xPos) + " " + str(self.nestedArray[GoalY][GoalX].yPos))
                tempName = container.name
                tempWeight = container.weight
                
                self.nestedArray[container.yPos - 1][container.xPos - 1].name = "UNUSED"
                self.nestedArray[container.yPos - 1][container.xPos - 1].weight = "00000"
                self.nestedArray[GoalY][GoalX].name = tempName
                self.nestedArray[GoalY][GoalX].weight = tempWeight
                # print(self.nestedArray[GoalY][GoalX].name + " " + str(self.nestedArray[GoalY][GoalX].xPos) + " " + str(self.nestedArray[GoalY][GoalX].yPos))

                # if(path != []):
                #     tempArray = []
                #     for element in path:
                #         if type(element) != list:
                #             tempArray.append(element)
                #     # print(type(tempArray))
                #     for element in tempArray:
                #         # print(type(element))
                #     if(len(tempArray) > 0):
                #         for element in tempArray:
                #             # print(element)

                return path

            #move node to closed list
            self.closed.append(currNode)
            #print("length of closed list: " + str(len(self.closed)))

            #pop element from open list
            #print("before pop currNode from open list, length = " + str(len(self.open)))
            newOpenArray = []
            for element in self.open:
                if currNode != element:
                    newOpenArray.append(element)
            self.open = newOpenArray
            #print("after pop currNode from open list, length = " + str(len(self.open)))

            
        # 4) generate neighbors
            # 4.1) for current node, generate neighboring nodes
            neighbors = self.findNeighbors(currNode.container, "below")
            if neighbors == -1:
                #print("blocked container has a container blocking it")
                break
            for neighbor in neighbors:

            # 4.2) ignore visited nodes (check closed list)
                if neighbor in self.closed:
                    continue

            # 4.3) calculate g h and f costs for each neighbor
                neighborNode = Node(neighbor, neighbor.xPos - 1, neighbor.yPos - 1, "neighbor")
                neighborNode.g = 1
                #print("neighbor node x and y values: x = " + str(neighbor.xPos) + ", y = " + str(neighbor.yPos))
                neighborNode.h = self.calculateHeuristic(GoalX, GoalY, neighborNode.x, neighborNode.y)
                neighborNode.f = neighborNode.g + neighborNode.h
                neighborNode.parent = currNode

            # 4.4) if neighbor not in open list, add    
                if all(neighborNode.f < openNode.f for openNode in self.open if openNode.name == "neighbor"):
                    self.open.append(neighborNode)

            #print("length of open: " + str(len(self.open)))
            #iteration = iteration + 1
            #if iteration > 10:
            #    break
        #account for blocked containers
        #print("containerblocking: name: " + self.nestedArray[container.yPos - 2][container.xPos - 1].name + ", x = " + str(self.nestedArray[container.yPos - 2][container.xPos - 1].xPos) + ", y = " + str(self.nestedArray[container.yPos - 2][container.xPos - 1].yPos))
        #print("check " + str(self.check))
        self.check = self.check + 1
        if(self.check > 10):
            return []
        #path.append(self.moveBlockingContainer(self.nestedArray[container.yPos - 2][container.xPos - 1], "above", path, self.check))
        return path
    
    #returns path (ARRAY OF STRINGS: x y containerweight containername) to take container off (start position to (x = 1, y = 8))
    def moveContainerOff(self, container, path):
        # print("Computing path for container: " + container.name + " - Coming Off")

        startNode = Node(container, container.xPos - 1, container.yPos - 1, "start")
        self.path = path
        # 1) create two lists open and closed ^
        self.open = []
        self.closed = []

        # 2) evaluate current node f = g + h, then add to open list
        #print("start node x and y values: x = " + str(startNode.x) + ", y = " + str(startNode.y))
        startNode.h = self.calculateHeuristic(0, 0, startNode.x, startNode.y)
        startNode.f = startNode.g + startNode.h
    
        self.open.append(startNode)
        #for element in self.open:
        #    print(element.container.name)

        #sanity check
        #iteration = 1
        # 3) loop through open list
        while(self.open):
            #check above cell
            #print("position of cell above container: x = " + str(self.nestedArray[container.yPos][container.xPos].x) + ", y = " + str(self.nestedArray[container.yPos][container.xPos].y))
            #if(self.nestedArray[container.yPos])

            #select node with lowest f score from open list
            currNode = self.open[0]
            for element in self.open:
                if(element.f < currNode.f):
                    currNode = element
            #print("lowest score f node: " + currNode.container.name + ", fscore = " + str(currNode.f) + ", x = " + str(currNode.container.xPos) + ", y = " + str(currNode.container.yPos))
            
            #check if at the goal state (x = 1, y = 1)
            if(currNode.container.xPos == 1) and (currNode.container.yPos == 1):
                #print("in goal node check")
                while currNode:
                    path.append(str(currNode.container.xPos) + " " + str(currNode.container.yPos) + " " + str(currNode.container.weight) + " " + str(currNode.container.name))
                    currNode = currNode.parent

                tempName = container.name
                tempWeight = container.weight
                
                self.nestedArray[container.yPos - 1][container.xPos - 1].name = "UNUSED"
                self.nestedArray[container.yPos - 1][container.xPos - 1].weight = "00000"
                self.nestedArray[0][0].name = tempName
                self.nestedArray[0][0].weight = tempWeight

                # print(len(path))
                #for element in path:
                #    print(element.container.name + " " + str(element.x) + " " + str(element.y))

                return path #return path reversed

            #move node to closed list
            self.closed.append(currNode)
            #print("length of closed list: " + str(len(self.closed)))

            #pop element from open list
            #print("before pop currNode from open list, length = " + str(len(self.open)))
            newOpenArray = []
            for element in self.open:
                if currNode != element:
                    newOpenArray.append(element)
            self.open = newOpenArray
            #print("after pop currNode from open list, length = " + str(len(self.open)))

            
        # 4) generate neighbors
            # 4.1) for current node, generate neighboring nodes
            neighbors = self.findNeighbors(currNode.container, "above")
            if neighbors == -1:
                break
            for neighbor in neighbors:

            # 4.2) ignore visited nodes (check closed list)
                if neighbor in self.closed:
                    continue

            # 4.3) calculate g h and f costs for each neighbor
                neighborNode = Node(neighbor, neighbor.xPos - 1, neighbor.yPos - 1, "neighbor")
                neighborNode.g = 1
                #print("neighbor node x and y values: x = " + str(neighbor.xPos) + ", y = " + str(neighbor.yPos))
                neighborNode.h = self.calculateHeuristic(0, 0, neighborNode.x, neighborNode.y)
                neighborNode.f = neighborNode.g + neighborNode.h
                neighborNode.parent = currNode

            # 4.4) if neighbor not in open list, add    
                if all(neighborNode.f < openNode.f for openNode in self.open if openNode.name == "neighbor"):
                    self.open.append(neighborNode)

            #print("length of open: " + str(len(self.open)))
            #iteration = iteration + 1
            #if iteration > 3:
            #    break

        #account for blocked containers
        #print("containerblocking: name: " + self.nestedArray[container.yPos - 2][container.xPos - 1].name + ", x = " + str(self.nestedArray[container.yPos - 2][container.xPos - 1].xPos) + ", y = " + str(self.nestedArray[container.yPos - 2][container.xPos - 1].yPos))
        path.append(self.moveBlockingContainer(self.nestedArray[container.yPos - 2][container.xPos - 1], "above", path, 0))
        if path == []:
            return []
        #print("after running move containers")
        self.moveContainerOff(container, path)
        return path

#moves blocked containers, MUST CHANGE NESTED ARRAY to reflect changes    
    def moveBlockingContainer(self, container , direction, path, check):
        self.direction = direction
        self.path = path
        self.check = check
        
        #need fix if more complex cases
        if direction == "above":
            GoalX = container.xPos
            for array in self.nestedArray:
                #print("The name of observed container " + array[GoalX].name)
                if array[GoalX].name == "UNUSED":
                    continue
                else:
                    GoalY = array[GoalX].yPos - 2
                    break
        # print("Goal State: x = " + str(GoalX) + ", y = " + str(GoalY))

        startNode = Node(container, container.xPos - 1, container.yPos - 1, "start")
        #path = []
        # 1) create two lists open and closed ^
        self.open = []
        self.closed = []

        # 2) evaluate current node f = g + h, then add to open list
        #print("start node x and y values: x = " + str(startNode.x) + ", y = " + str(startNode.y))
        startNode.h = self.calculateHeuristic(GoalX, GoalY, startNode.x, startNode.y)
        startNode.f = startNode.g + startNode.h
    
        self.open.append(startNode)
        #for element in self.open:
        #    print(element.container.name)

        #sanity check
        #iteration = 1
        # 3) loop through open list
        while(self.open):
            #check above cell
            #print("position of cell above container: x = " + str(self.nestedArray[container.yPos][container.xPos].x) + ", y = " + str(self.nestedArray[container.yPos][container.xPos].y))
            #if(self.nestedArray[container.yPos])

            #select node with lowest f score from open list
            currNode = self.open[0]
            for element in self.open:
                if(element.f < currNode.f):
                    currNode = element
            #print("lowest score f node: " + currNode.container.name + ", fscore = " + str(currNode.f) + ", x = " + str(currNode.container.xPos) + ", y = " + str(currNode.container.yPos))
            
            #check if at the goal state (x = 1, y = 1)
            if(currNode.container.xPos == (GoalX + 1)) and (currNode.container.yPos == (GoalY + 1)):
                #print("in goal node check")
                while currNode:
                    path.append(str(currNode.container.xPos) + " " + str(currNode.container.yPos) + " " + str(currNode.container.weight) + " " + str(currNode.container.name))
                    currNode = currNode.parent

                #print(container.name)
                #change nested container array to reflect changes in here
                #print(self.nestedArray[GoalY][GoalX].name + " " + str(self.nestedArray[GoalY][GoalX].xPos) + " " + str(self.nestedArray[GoalY][GoalX].yPos))
                tempName = container.name
                tempWeight = container.weight
                
                self.nestedArray[container.yPos - 1][container.xPos - 1].name = "UNUSED"
                self.nestedArray[container.yPos - 1][container.xPos - 1].weight = "00000"
                self.nestedArray[GoalY][GoalX].name = tempName
                self.nestedArray[GoalY][GoalX].weight = tempWeight
                #print(self.nestedArray[GoalY][GoalX].name + " " + str(self.nestedArray[GoalY][GoalX].xPos) + " " + str(self.nestedArray[GoalY][GoalX].yPos))

                if(path != []):
                    tempArray = []
                    for element in path:
                        if type(element) != list:
                            tempArray.append(element)
                    #for element in tempArray:
                    #    print(element.name + " " + str(element.xPos) + " " + str(element.yPos))

                return path #return path reversed

            #move node to closed list
            self.closed.append(currNode)
            #print("length of closed list: " + str(len(self.closed)))

            #pop element from open list
            #print("before pop currNode from open list, length = " + str(len(self.open)))
            newOpenArray = []
            for element in self.open:
                if currNode != element:
                    newOpenArray.append(element)
            self.open = newOpenArray
            #print("after pop currNode from open list, length = " + str(len(self.open)))

            
        # 4) generate neighbors
            # 4.1) for current node, generate neighboring nodes
            neighbors = self.findNeighbors(currNode.container, "above")
            if neighbors == -1:
                #print("blocked container has a container blocking it")
                break
            for neighbor in neighbors:

            # 4.2) ignore visited nodes (check closed list)
                if neighbor in self.closed:
                    continue

            # 4.3) calculate g h and f costs for each neighbor
                neighborNode = Node(neighbor, neighbor.xPos - 1, neighbor.yPos - 1, "neighbor")
                neighborNode.g = 1
                #print("neighbor node x and y values: x = " + str(neighbor.xPos) + ", y = " + str(neighbor.yPos))
                neighborNode.h = self.calculateHeuristic(GoalX, GoalY, neighborNode.x, neighborNode.y)
                neighborNode.f = neighborNode.g + neighborNode.h
                neighborNode.parent = currNode

            # 4.4) if neighbor not in open list, add    
                if all(neighborNode.f < openNode.f for openNode in self.open if openNode.name == "neighbor"):
                    self.open.append(neighborNode)

            #print("length of open: " + str(len(self.open)))
            #iteration = iteration + 1
            #if iteration > 10:
            #    break
        #account for blocked containers
        #print("containerblocking: name: " + self.nestedArray[container.yPos - 2][container.xPos - 1].name + ", x = " + str(self.nestedArray[container.yPos - 2][container.xPos - 1].xPos) + ", y = " + str(self.nestedArray[container.yPos - 2][container.xPos - 1].yPos))
        #print("check " + str(self.check))
        self.check = self.check + 1
        if(self.check > 10):
            return []
        path.append(self.moveBlockingContainer(self.nestedArray[container.yPos - 2][container.xPos - 1], "above", path, self.check))
        return path

# #testing ship coming off
# newShip = Ship()
# newShip.loadGrid("ShipCase4.txt")
# newShip.printContainers()
# Problem = Problem(newShip.containers)
# Problem.loadNestedContainers()
# Problem.printShipContNested()
# Problem.printTempContainers()

# Transfer = Transfer(Problem.shipContNested , Problem.shipContainers)
# for array in Problem.shipContNested:
#     for element in array:
#         if(element.name == "Cat"):
#             container = element
# pathArray = Transfer.moveContainerOff(container, [])
# print(type(pathArray))
# newPathArray = []
# for element in pathArray:
#     if type(element) != list:
#         newPathArray.append(element)

# #newPathArray = newPathArray[::-1]
# print(newPathArray)

# Problem.returnPathArray(newPathArray)

# print("path is: ")
# if(newPathArray == None):
#     print("No path available")
# else:
#     for element in newPathArray:
#         print(element)
# Problem.printShipContNested()
# #print("simulate taking out container from top left")
# Transfer.nestedArray[0][0].name = "UNUSED"
# Transfer.nestedArray[0][0].weight = "00000"

# #testing ship coming on
# pathArray = Transfer.moveContainerOn("01234", "Liam", [])
# print(type(pathArray))
# newPathArray = []
# for element in pathArray:
#     if type(element) != list:
#         newPathArray.append(element)
# #newPathArray = newPathArray[::-1]
# print(len(newPathArray))
# print("path is: ")
# if(newPathArray == None):
#     print("No path available")
# else:
#     for element in newPathArray:
#         print(element)
# Problem.printShipContNested()

# Problem.pathContainers[0] = Container(1, 1, "00000", "UNUSED", 0, "x", False)
# print(Problem.pathContainers[0].name + str(Problem.pathContainers[0].xPos) + str(Problem.pathContainers[0].yPos))
# Problem.pathContainers[0] = Container(1, 1, "01234", "Liam", 0, "x", False)
# print(Problem.pathContainers[0].name + str(Problem.pathContainers[0].xPos) + str(Problem.pathContainers[0].yPos))
# Problem.returnPathArray(newPathArray)