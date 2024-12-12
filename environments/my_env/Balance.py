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
            if grid[row][col] != 0:
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
            if grid[row][col] != 0:
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

def moveContainer(grid,side,containers,val,movements):   # Function to begin moving the ideal container once its movable
    #print("In moveContainer")
    newPos = findOpenSpot(grid,side)    # Get position to move to
    #print("newpos",newPos)
    temp = val
    i = containers[val][0]
    j = containers[val][1]
    grid[i][j] = 0
    grid[newPos[0]][newPos[1]] = temp
    movements.append("("+str(i)+","+str(j)+") => ("+str(newPos[0])+","+str(newPos[1])+")")
    return

def findOpenSpot(grid,side):
    #print("In findOpenSpot")
    Halfsies = int(len(grid[0])) // 2
    ShipGoalSide = []
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
                        return [row, pos + len(ShipGoalSide[0])]
                    else:   # If left side is lighter
                        return [row, pos]
                    
                if row-1 < len(ShipGoalSide) and ShipGoalSide[row-1][pos] != 0: # Not Floating
                    if Side:    # Right lighter side
                        return [row, pos + len(ShipGoalSide[0])]
                    else:   # Left lighter side
                        [row, pos]
    #print("LAMAYOOOOOOOOO")
    return []

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



def moveBlocked(grid, i, j,movements):    # WORKS NOWWWWWWWWWWWWWWWW 
    #print("IN moveBlocked")
    #print("grid in moveBlocked",grid)
    min = 10000
    newX = 0
    newY = 0
    row = 0
    col = j

    while True:
        open = getOpenSpots(grid)
        while row < len(grid) and grid[row][col] == 0:  # Start at top of col with ideal container, go down until blocking container is found
            row = row + 1
        if grid[row][col] == grid[i][j]:  # Stop once ideal container is found in col
            break   
        #print("block container",grid[row][col])
        for x in range(len(open)):
            res = manhattanDis([open[x][0],open[x][1]],[row,col])
            if res < min and validSpot(grid,open[x][0],open[x][1]):
                #print("x = ",open[x][0],"y = ",open[x][1])
                newX = open[x][0]
                newY = open[x][1]
                min = res
        temp = grid[row][col]
        grid[row][col] = 0
        grid[newX][newY] = temp
        movements.append("("+str(row)+","+str(col)+") => ("+str(newX)+","+str(newY)+")")
        #print("grid during block:",grid)
    return

def calcCost(grid,i,j,x,y,movs):    # i,j = curPos => x,y = goalPos
    movs.append("("+str(i)+","+str(j)+" tempweight tempname")
    cost = 0
    tempx = i
    tempy = j
    while True:        
        c = {} # Coords dict
        # Check left cell
        if (tempy-1 >= 0):
            if (grid[tempx][tempy-1] == 0):
                heur = manhattanDis([tempx,tempy-1],[x,y])
                if heur not in c:
                    c[heur] = [tempx,tempy-1]
        # Check right cell
        if (tempy+1 < len(grid[0])):
            if (grid[tempx][tempy+1] == 0):
                heur = manhattanDis([tempx,tempy+1],[x,y])
                if heur not in c:
                    c[heur] = [tempx,tempy+1]
        # Check below cell
        if (tempx+1 < len(grid)):
            if (grid[tempx+1][tempy] == 0):
                heur = manhattanDis([tempx+1,tempy],[x,y])
                if heur not in c:
                    c[heur] = [tempx+1,tempy]
        # Check above cell
        if (tempx-1 >= 0):
            if (grid[tempx-1][tempy] == 0):
                heur = manhattanDis([tempx-1,tempy],[x,y])
                if heur not in c:
                    c[heur] = [tempx-1,tempy]
        sorted_c = dict(sorted(c.items()))
        optVal = list(sorted_c.keys())[0]
        newx = c[optVal][0]
        newy = c[optVal][1]
        tempx = newx
        tempy = newy
        movs.append("("+str(newx)+","+str(newy)+" tempweight tempname")
        cost = cost + 1

                        
                        
                    

    
            
def validSpot(grid,i,j):
    # Check if spot is on the ground
    if i == len(grid):
        return True
    # Check if spot is above another container
    if grid[i-1][j] != 0:
        return True
    return False    # Either spot is not on ground, or spot is floating (no container below it)

def bestMove(grid, lhs, rhs, side):
   # print("In bestMove")
    #print("grid:",grid)
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
   # print("weight:",weight)
    return weight

    # MAKE HASHMAP WITH WEIGHTS AND COORDS. USE WEIGHTS FROM BEST MOVE TO FIND COORDS OF BEST WEIGHT TO MOVE

def balance(grid):
    print("Grid at start:")
    printG(grid)
    containers = {}
    #gridCoords = getGCoord(grid)
    codeCoords = getCCoord(grid)
    #print("grid coords:",gridCoords)
    #print("code coords:",codeCoords)
    
    if len(codeCoords) == 0:
        print("Ship is empty!")
        return [], [], True   
    
    lhs, rhs, isBalanced = calculate_balance(grid)

    
    if isBalanced:
        print("Ship is already balanced!")
        return None, True
    
    movements = []
    Half = len(grid[0]) // 2

    # print("HIIIIIII",coords)
    
    # print(lhsShip, rhsShip)
    
    while (not isBalanced):      
      #  print("In balance")
        codeCoords = getCCoord(grid)  
        currContainer = []
        currVals = []
        lhs, rhs, isBalanced = calculate_balance(grid)
       # print("lhs:",lhs,"rrrhs:",rhs)
       # print("GRID IN BALANCE:",grid)
        #Check Max Iteration

        #Pick Side to Start on
        if lhs > rhs:
            for Position in codeCoords:
                if ((Position[1] < Half) and (grid[Position[0]][Position[1]] != 0)):
                    currContainer.append(Position)
                    currVals.append(grid[Position[0]][Position[1]])
                    containers[grid[Position[0]][Position[1]]] = Position
            
        else:
            for Position in codeCoords:
                #print("X",Position)
                if ((Position[1] >= Half) and (grid[Position[0]][Position[1]] != 0)):
                    currContainer.append(Position)
                    currVals.append(grid[Position[0]][Position[1]])
                    containers[grid[Position[0]][Position[1]]] = Position

                    

       # print("Code Coords:",codeCoords)
        # print("Grid Coords:",gridCoords)
        # print("Coords of containers on side that is greater weight:",currContainer)        
        # print("Container weights associated with the coords",currVals)

        side = 0 if lhs > rhs else 1
        # print("lhs:",lhs,"rhs:",rhs)
        # print("side:",side)
        bestContainerWeight = bestMove(currVals,lhs,rhs,side)
        #print("Best container weight to move:",bestContainerWeight)

        # print(containers[bestContainerWeight])

        if (not canMove(grid,containers[bestContainerWeight][0],containers[bestContainerWeight][1])):        
            # print("Container cannot be moved!")
            #print("Grid before moveBlocked",grid)
            moveBlocked(grid,containers[bestContainerWeight][0],containers[bestContainerWeight][1],movements)
            print("Printing grid after moving blocked")
            printG(grid)
            
            #print("Grid after moveBlocked",grid)
        # print("Container can be moved!")
        newSide = 0 if side == 1 else 1
        moveContainer(grid,newSide,containers,bestContainerWeight,movements)
        #print("moving:",moving)
        #print(currContainer)
        #print("HEREEEEEEEEEEEE",currVals)
        
        #Compute Cost of moving each container to the other side
        print("Printing grid after moving ideal container")
        printG(grid)
        
        #SIFT???
        
        
        #Move the container
        
        #Update Containers
        lhs, rhs, isBalanced = calculate_balance(grid)
    
    #Update Ships and return with Steps
    
    
    return movements #Steps, ShipGrid, True
    
    

# Ship Grid (8, 12)
def calculate_balance(grid):
    lhsWeight = 0
    rhsWeight = 0
    isBalanced = False
    
    for Row in grid:
        Half = len(Row) // 2
        #print("ROWWWW",Row,"HALFFFF",Half)
        for Slot in range(len(Row)):
            if Slot < Half:
                lhsWeight += Row[Slot]
            else:
                rhsWeight += Row[Slot]
    
    if(abs(rhsWeight - lhsWeight) <= 2):
        isBalanced = True    
    
    return lhsWeight, rhsWeight, isBalanced


ShipOne = [
            [20, 30, 0, 0],
            [3, 7, 0, 40]
        ]

# [2,1], [2,2], [1,1], [1,2]

ShipTwo = [
            [6, 0, 0, 0],
            [4, 0, 0, 10]
        ]

coordOne = [[1,1], [1,2], [1,4], [2,1], [2,2]]
coordTwo = [[1,1], [1,4], [2,1]] 
 
# with open(r"C:\Users\varga\Documents\CS-179\project_repo\projo179\TileShippingExpress\environments\my_env") as f:
#     print(f.read())

from pathlib import Path

PROJECT_DIR = Path(__file__).parent

print("--- Reading in the entire file:")

path = PROJECT_DIR / 'ShipCase1.txt'
contents = path.read_text()

# print(contents[0][18])

# print("\n--- Looping over the lines:")
print("HEHEHEH")
lines = contents.splitlines()
print(lines[2][18])
temp1 = lines[len(lines)-1][1:3]
temp2 = lines[len(lines)-1][4:6]
xxx = int(temp1)
yyy = int(temp2)
print("x:",xxx," y:",yyy)
# for line in lines:
#     print(len(line))


# file = open("C:\Users\varga\Documents\CS-179\project_repo\projo179\TileShippingExpress\environments\my_env","r")
# print(file.read())
# file.close()
# 20, 30, 3, 7
# L, R, B = 
#m = balance(ShipOne)

# print("Movements to achieve balance")
# for i in range(len(m)):
#     print(m[i])
# print("Left:", L," Right:", R, "Balance:", B)

# L, R, B = 
#print(balance(ShipTwo, coordTwo))
# print("Left:", L," Right:", R, "Balance:", B)