from pathlib import Path
import copy as c

# class Container():
#     def __init__(self, xPos, yPos, weight, name, id):
#         self.xPos = xPos
#         self.yPos = yPos
#         self.weight = weight
#         self.name = name
#         self.id = id

# class Ship():
#     def __init__(self):
#         self.containers = []
        

# StepsNeeded, Grid, isBalanced
# Grid is actual list of Rows and Cols
# Containers is list of container coords

# Gets coordinates of containers relative to their position on grid. So arr[0][0] = (8,1) on grid. Stores in list and returns.
def printG(grid):
    #print("Printing grid")
    for i in range(len(grid)):
        print(grid[i])

def getGCoord(grid):
    coords = []
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            temp = []
            row_temp = 0
            if row == 0:
                row_temp = len(grid)
            else:
                row_temp = len(grid) - row
            temp.append(row_temp)
            temp.append(col+1)
            if len(temp) != 0:
                coords.append(temp)
    return coords

# Gets coordinates of containers relative to their position in code. So arr[0][0] = (0,0). Stores in list and returns.      
def getCCoord(grid):
    coords = []
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] > 0:
                temp = []
                temp.append(row)
                temp.append(col)
                coords.append(temp)
    return coords

def canMove(grid, i, j):
    #print("In canMove")
    # Start on heavier side
    if i == 0: return True
    if grid[i-1][j] == 0: return True  # If there is no container directly above, then is movable
    return False

def moveContainer(grid,side,containers,val,movements,r,sift=[-2,-2]):   # Function to begin moving the ideal container once its movable
    newx,newy,cost=0,0,0
    if sift[0] == -2:
        newPos = findOpenSpot(grid,side)    # Get position to move to
        #print("newPos:",newPos)
        min = 10000
        newx = 0
        newy = 0
        for x in newPos:
            res = manhattanDis(x,containers[val])
            if res < min:
                newx = x[0]
                newy = x[1]
                min = res
    else:
        newx = sift[0]
        newy = sift[1]
    cost = calcCost(grid,containers[val][0],containers[val][1],newx,newy,movements,r)
    #print("cost 11111")
    temp = grid[containers[val][0]][containers[val][1]]
    grid[containers[val][0]][containers[val][1]] = 0
    grid[newx][newy] = temp

    #print("newpos",newPos)
    temp = val
    
   # movements.append("("+str(i)+","+str(j)+") => ("+str(newPos[0])+","+str(newPos[1])+")")
   # print("In moveContainer")
    return cost

def findOpenSpot(grid,side):
    #print("In findOpenSpot")
    print("before halfsies")
    Halfsies = int(len(grid[0])) // 2
    print("after halfsies")
    ShipGoalSide = []
    res = []
    Side = False
    #print("lhs",lhs,"rhs:",rhs)
    
    if side == 1: #Right Side is Lighter
        for row in grid: 
            ShipGoalSide.append(row[Halfsies:])
        Side = True
    else:                     #Left Side is Lighter
        for row in grid:
            ShipGoalSide.append(row[:Halfsies])
        
    #print("SGS",ShipGoalSide)

    for row in range(len(ShipGoalSide)):
        #print("row:",row)
        for pos in range(len(ShipGoalSide[row])):
            #print("pos:",pos)
            if ShipGoalSide[row][pos] == 0:
                if (row == len(ShipGoalSide) - 1): # On Ground
                    if Side:    # If right side is lighter
                        res.append([row, pos + len(ShipGoalSide[0])])
                    else:   # If left side is lighter
                        res.append([row, pos])
                    
                if row+1 < len(ShipGoalSide) and ShipGoalSide[row+1][pos] != 0: # Not Floating
                    if Side:    # Right lighter side
                        res.append([row, pos + len(ShipGoalSide[0])])
                    else:   # Left lighter side
                        res.append([row, pos])
    #print("LAMAYOOOOOOOOO")
    return res

def manhattanDis(coords1, coords2):
    return (abs(coords1[0]- coords2[0]) + abs(coords1[1] - coords2[1]))

def getOpenSpots(grid):
    ret = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                ret.append([i,j])
    #print("ret:",ret)
    return ret

def getGoals(grid):
    res = []
    for i in range(len(grid)-1,-1,-1):
        seen = {}
        for j in range(len(grid[0])):
            if (len(grid[0])//2)-j-1 >= 0:
                res.append([i,(len(grid[0])//2)-j-1])    # LEFT GOAL
            if (len(grid[0])//2)+j < len(grid[0]):
                res.append([i,(len(grid[0])//2)+j])    # LEFT GOAL
            if (len(grid[0])//2)-j == 0 and (len(grid[0])//2)+j == 0:
                break
    return res

def getContainers(grid):
    containers = []

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] != 0 and grid[row][col] != -1:
                containers.append([grid[row][col],[row,col]])
    #print("ererrereer",containers)
    return containers  

def locateContainerSift(grid, containerID):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] != 0 and grid[row][col] == containerID:
                return [row, col]
    return []

def getAllGridSpotsSift(grid):
    positions = list()
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            positions.append([row, col])
    return positions

def sift(grid,conts,movs,r):
    cost = 0
    cons = getContainers(grid)
    goalSpots = getGoals(grid)  # All goals spots in from left to right
    sorted_weight = sorted(cons, reverse=True, key=lambda x: x[0]) # [Weight] = Position(x,y)
    weights = []
    for w in sorted_weight:
        weights.append(w[0])
    
    # WHen moving containers that are blocking, you need to update their new location. In sorted_weight,
    # go in for loop to find container that matches weight, if len is more than 1 (theres duplicate),
    # check each coords until you find matching cords of blocked container that was just moved. once found
    # update coords

    for weight in weights:
        cons = getContainers(grid)
        pos = [sorted_weight[0][1][0],sorted_weight[0][1][1]] # Get position of heaviest container
        sorted_weight.pop(0)
        goalPos = goalSpots.pop(0)
        if weight == grid[goalPos[0]][goalPos[1]] : # Check if it was already moved
            continue
        else:   # Container has not been moved!!!!
            # check if blocked
            if (grid[goalPos[0]][goalPos[1]]) != 0 and grid[goalPos[0]][goalPos[1]] != -1:
                tempRow = 0
                tempcon = grid[tempRow][goalPos[1]] # Container in col of container to move that is blocking goal spot
                while tempRow < len(grid) and tempcon == 0:   # While temprow < 8 and we are in empty con
                    tempRow += 1
                    tempcon = grid[tempRow][goalPos[1]]
                tempcon = grid[tempRow][goalPos[1]] # Container in col of container to move that is blocking goal spot
                cost += siftBlock(grid,tempRow,goalPos[1],movs,r,sorted_weight)  # Potentially move container
                cost += calcCost(grid,pos[0],pos[1],goalPos[0],goalPos[1],movs,r)
                temp = grid[pos[0]][pos[1]] 
                grid[pos[0]][pos[1]] = 0
                grid[goalPos[0]][goalPos[1]] = temp
            else:   # Not blocked so move container directly to goal spot
                temp = grid[pos[0]][pos[1]] 
                grid[pos[0]][pos[1]] = 0
                grid[goalPos[0]][goalPos[1]] = temp
    return cost

def siftBlock(grid,i,j,movs,r,sw): #i,j = loc of block container
    open = getOpenSpots(grid)
    newx,newy = 0,0
    min = 100000
    cost = 0
    for x in range(len(open)):
        res = manhattanDis([open[x][0],open[x][1]],[i,j])
        if res < min and validSpot(grid,open[x][0],open[x][1],i,j):
            newx = open[x][0]
            newy = open[x][1]
            min = res
    for con in sw:
        if con[0] == grid[i][j]:    # Found the value of blocked container to move
            if con[1][0] == i and con[1][1] == j:   # Check if coords match the blocked container
                con[1][0] = newx
                con[1][1] = newy
                break

    temp = grid[i][j]
    cost += calcCost(grid,i,j,newx,newy,movs,r)
    grid[i][j] = 0
    grid[newx][newy] = temp
    return cost

# Moves blocked containers for non-sift movements
def moveBlocked(grid, i, j,movements,r):    # WORKS NOWWWWWWWWWWWWWWWW 
    min = 10000
    newX = 0
    newY = 0
    row = 0
    col = j
    cost = 0

    while True:
        open = getOpenSpots(grid)
        min = 10000
        while row < len(grid) and grid[row][col] == 0:  # Start at top of col with ideal container, go down until blocking container is found
            row = row + 1
        if row == i and col == j:  # Stop once ideal container is found in col
            break   
        for x in range(len(open)):
            res = manhattanDis([open[x][0],open[x][1]],[row,col])
            if res < min and validSpot(grid,open[x][0],open[x][1],row,col):
                newX = open[x][0]
                newY = open[x][1]
                min = res
        temp = grid[row][col]
        cost = cost + calcCost(grid,row,col,newX,newY,movements,r)
        grid[row][col] = 0
        grid[newX][newY] = temp
    return cost 

def validSpot(grid,i,j,r,c):
    temp1 = str(i+1)+str(j)
    temp2 = str(r)+str(c)
    # Check if spot is on the ground
    if i == len(grid)-1:
        return True
    # Check if spot is above another container
    if grid[i+1][j] != 0 and temp1 != temp2:
        return True
    return False    # Either spot is not on ground, or spot is floating (no container below it)

def calcCost(grid,i,j,x,y,movs,r):    # i,j = curPos => x,y = goalPos
    if i == 0:
        row_temp = len(grid)
    else:
        row_temp = len(grid) - i
    label = str(row_temp)+","+str(j+1)
    locname = r[label][0]
    locweight = r[label][1]
    movs.append(str(j+1)+" "+str(i+1)+" "+locweight+" "+locname)
    cost, tempx, tempy, nodes, count, movOff, movL, movR, offGrid = 0,i,j,{},1,False,False,False,0
    while True:   
        visited = str(tempx) + "," + str(tempy)
        nodes[visited]=1
        visiting = ""
        if tempx == x and tempy == y:
            break
        c = {} # Coords dict
        # Check left cell
        if offGrid == 0:
            visiting = str(tempx)+","+str(tempy-1)
            if (tempy-1 >= 0 and visiting not in nodes and grid[tempx][tempy-1] == 0):
                heur = manhattanDis([tempx,tempy-1],[x,y])
                if heur not in c:
                    c[heur] = [tempx,tempy-1]
            else: 
                offGrid = offGrid+1
            # Check right cell
            visiting = str(tempx)+","+str(tempy+1)
            if (tempy+1 < len(grid[0]) and visiting not in nodes and grid[tempx][tempy+1] == 0):
                heur = manhattanDis([tempx,tempy+1],[x,y])
                if heur not in c:
                    c[heur] = [tempx,tempy+1]
            else: 
                offGrid = offGrid+1
            # Check below cell
            visiting = str(tempx+1)+","+str(tempy)
            if (tempx+1 < len(grid) and visiting not in nodes and grid[tempx+1][tempy] == 0):
                heur = manhattanDis([tempx+1,tempy],[x,y])
                if heur not in c:
                    c[heur] = [tempx+1,tempy]
            else: 
                offGrid = offGrid+1
            # Check above cell
            visiting = str(tempx-1)+","+str(tempy)
            if (tempx-1 >= 0) and visiting not in nodes and grid[tempx-1][tempy] == 0:
                heur = manhattanDis([tempx-1,tempy],[x,y])
                if heur not in c:
                    c[heur] = [tempx-1,tempy]
            else: 
                offGrid = offGrid+1
        if offGrid == 4:
            label = str(tempx) + "," + str(tempy)
            if movOff is False: # First time going off grid so only going up
                cost = cost + 1
                movOff = True
                if grid[tempx][tempy+1] != 0: movR = True
                else: movL = True
                movs.append("(-1)"+","+str(tempy)+" 00000 UNUSED")
                count = count + 1
            # Moved to position above first row that has an empty slot below it on first row of grid
            elif grid[tempx][tempy] == 0 and label not in nodes:
                movOff = False
                offGrid = 0
                cost = cost + 1
                movs.append("(-1)"+","+str(tempy)+" 00000 UNUSED")
                count = count + 1
            # If still moving above grid and full col is to the right
            elif movR is True and grid[tempx][tempy+1] != 0:
                movR = True
                movL = False
                cost = cost + 1
                movs.append("(-1)"+","+str(tempy+1)+" 00000 UNUSED")
                tempy = tempy+1
                count = count + 1
            # If still moving above grid but space to right is 0!
            elif grid[tempx][tempy+1] == 0:
                movR = False
                movOff = False
                movL = False
                count = count + 1
                cost = cost + 2
                movs.append("(-1)"+","+str(tempy+1)+" 00000 UNUSED")
                tempy = tempy+1
            # If still moving above grid but space to left is 0!
            elif grid[tempx][tempy-1] == 0:
                movR = False
                movOff = False
                movL = False
                count = count + 1
                cost = cost + 2
                movs.append("(-1)"+","+str(tempy-1)+" 00000 UNUSED")
            # If still moving above grid and full col is to the left
            elif movL is True and grid[tempx][tempy-1] != 0:
                movL = True
                movR = False
                tempy = tempy-1
                cost = cost+1
                movs.append("(-1)"+","+str(tempy))
                count = count + 1
        if offGrid != 4:
            if tempx == 0:
                row_temp = len(grid)
            else:
                row_temp = len(grid) - tempx
            label = str(row_temp)+","+str(tempy+1)
            sorted_c = dict(sorted(c.items()))
            optVal = list(sorted_c.keys())[0]
            newx = c[optVal][0]
            newy = c[optVal][1]
            name = r[label][0]
            weight = r[label][1]
            del r[label]
            tempx = newx
            tempy = newy
            if tempx == 0:
                row_temp = len(grid)
            else:
                row_temp = len(grid) - tempx
            label = str(row_temp)+","+str(tempy+1)
            r[label] = [name,weight]

            movs.append(str(newy+1)+" "+str(newx+1)+" "+weight+" "+"UNUSED")
            cost = cost + 1
            count = count + 1
            offGrid = 0
    return cost                                                    

def bestMove(grid, lhs, rhs, side):
    min = 10000
    weight = 0
    for c in grid:
        tempL = lhs
        tempR = rhs
        if side == 0:
            tempL = tempL - c
            tempR = tempR + c
            if (abs(tempL - tempR)) < min:
                min = abs(tempL - tempR)
                weight = c
        else:
            tempR = tempR - c
            tempL = tempL + c
            if (abs(tempR - tempL)) < min:
                min = abs(tempL - tempR)
                weight = c
    return weight

def balance(r,grid):
    count = 0
    
    if not isinstance(grid, list):
        raise TypeError("grid should be a list")
    gridcpy = grid.copy()
    
    if not isinstance(r, dict):
        raise TypeError("r should be a dictionary")
    rcpy = r.copy()
    
    contcpy = {}
    containers = {}
    codeCoords = getCCoord(grid)
    cost = 0
    
    print("after get coord")

    if len(codeCoords) == 0:
        print("Ship is empty!")
        return [], 0 #, [], True  
    
    # print(type(grid))
    # print(grid)
    lhs, rhs, isBalanced = calculate_balance(grid)

    
    if isBalanced:
        print("Ship is already balanced!")
        return None, True
    print("not balanced")
    movements = []
    Half = len(grid[0]) // 2
    while (not isBalanced):   
        print("in while loop")   
        if count == 100:
            movements = []
            print("Ship cannot be balanced. Begin Sift operation!")
            cost = sift(gridcpy,contcpy,movements,rcpy)
            return movements,cost
        codeCoords = getCCoord(grid)  
        currContainer = []
        currVals = []
        lhs, rhs, isBalanced = calculate_balance(grid)
        #Check Max Iteration

        #Pick Side to Start on
        if lhs > rhs:
            for Position in codeCoords:
                if ((Position[1] < Half) and (grid[Position[0]][Position[1]] > 0)):
                    currContainer.append(Position)
                    currVals.append(grid[Position[0]][Position[1]])
                    containers[grid[Position[0]][Position[1]]] = Position
            
        else:
            for Position in codeCoords:
                if ((Position[1] >= Half) and (grid[Position[0]][Position[1]] > 0)):
                    currContainer.append(Position)
                    currVals.append(grid[Position[0]][Position[1]])
                    containers[grid[Position[0]][Position[1]]] = Position

        if count == 0:
            contcpy = containers

        side = 0 if lhs > rhs else 1
        bestContainerWeight = bestMove(currVals,lhs,rhs,side)

        print("before move container")

        if (not canMove(grid,containers[bestContainerWeight][0],containers[bestContainerWeight][1])):        
            cost = cost + moveBlocked(grid,containers[bestContainerWeight][0],containers[bestContainerWeight][1],movements,r)
        newSide = 0 if side == 1 else 1
        cost = cost + moveContainer(grid,newSide,containers,bestContainerWeight,movements,r)
        
        print("after move container")

        print("before second balance check")
        # Check if balanced again
        lhs, rhs, isBalanced = calculate_balance(grid)
        count+=1
        print("after balance check")
        ("print end while loop iteration")
    #Update Ships and return with Steps
    # print(type(movements))
    # print(movements)
    # print(type(cost))
    # print(cost)
    return movements, cost #Steps, cost
    
    

# Ship Grid (8, 12)
def calculate_balance(grid):
    lhsWeight = 0
    rhsWeight = 0
    isBalanced = False
    
    for Row in grid:
        Half = len(Row) // 2
        for Slot in range(len(Row)):
            if Row[Slot] == -1: continue
            elif Slot < Half:
                lhsWeight += Row[Slot]
            else:
                rhsWeight += Row[Slot]
    
    diff = (rhsWeight + lhsWeight) / 10
    if(abs(rhsWeight - lhsWeight) <= diff):
        isBalanced = True    
    
    return lhsWeight, rhsWeight, isBalanced


ShipOne = [
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [20, 30, 0, 0,0,0,0,0,0,0,0,0],
            [3, 7, 0, 0,0,0,0,0,0,0,0,40]
        ]

def readFileInput(file):
    PROJECT_DIR = Path(__file__).parent
    path = PROJECT_DIR / file
    contents = path.read_text()
    res = {}
    grid = []
    lines = contents.splitlines()
    switch = "z"
    count = 0
    newList = []
    for l in lines:
        first = l[1:3]
        if count == 0:
            switch = first
        elif switch != first and count != 0:
            switch = first
            grid.append(newList)
            newList = []
        x = int(l[1:3])
        y = int(l[4:6])
        loc = str(x)+","+str(y)
        name = l[18:].strip()
        weight = l[10:15].strip()
        res[loc] = [name, weight]
        if weight == "00000" and name == "NAN":
            newList.append(-1)
        elif weight == "00000" and name != "NAN":
            newList.append(0)
        else:
            newList.append(int(weight))
        count = count + 1
    grid.append(newList)

    idx = 0
    for row in range(len(grid) - 1, 3, -1):
        temp = grid[idx]
        grid[idx] = grid[row]
        grid[row] = temp
        idx = idx + 1
    return res, grid

def readFile():
    PROJECT_DIR = Path(__file__).parent
    path = PROJECT_DIR / 'ShipCase1.txt'
    contents = path.read_text()
    res = {}
    grid = []
    lines = contents.splitlines()
    switch = "z"
    count = 0
    newList = []
    for l in lines:
        first = l[1:3]
        if count == 0:
            switch = first
        elif switch != first and count != 0:
            switch = first
            grid.append(newList)
            newList = []
        x = int(l[1:3])
        y = int(l[4:6])
        loc = str(x)+","+str(y)
        name = l[18:].strip()
        weight = l[10:15].strip()
        res[loc] = [name, weight]
        if weight == "00000" and name == "NAN":
            newList.append(-1)
        elif weight == "00000" and name != "NAN":
            newList.append(0)
        else:
            newList.append(int(weight))
        count = count + 1
    grid.append(newList)

    idx = 0
    for row in range(len(grid) - 1, 3, -1):
        temp = grid[idx]
        grid[idx] = grid[row]
        grid[row] = temp
        idx = idx + 1
    return res, grid
        
def getVals(grid,val):
    return grid[val][0], grid[val][1]

# r,g = readFile()
# print("r length: " + str(len(r)) + " g length: " + str(len(g)))
# # for element in g:
# #     print(element)
# # for element in r:
# #     print(r)
# m,c = balance(r,g)
# m.reverse()
# print("TOTAL COST IS:",c)

# print("movements")
# for i in m:
#     print(i)
