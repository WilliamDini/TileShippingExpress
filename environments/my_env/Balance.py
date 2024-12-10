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
    # Start on heavier side
    if i != 0 and grid[i-1][j] == 0:    # If there is no container directly above, then is movable
        return True
    return False

def moveContainer(grid):
    newPos = findOpenSpot(grid,)
    print()

def findOpenSpot(grid, lhs, rhs, side):
    Halfsies = int(len(grid[0])) // 2
    ShipGoalSide = []
    print("lhs",lhs,"rhs:",rhs)
    
    if side == 1: #Right Side is Lighter
        for row in grid: 
            ShipGoalSide.append(row[Halfsies:])
            Side = True
    else:                     #Left Side is Lighter
        for row in grid:
            ShipGoalSide.append(row[:Halfsies])
        
    print(ShipGoalSide)
    


    for row in range(len(ShipGoalSide)):
        print("row:",row)
        for pos in ShipGoalSide[row]:
            print("pos:",pos)
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
    print("LAMAYOOOOOOOOO")
    return []

def moveBlocked(grid, i, j):    # WORKS NOWWWWWWWWWWWWWWWW 
    col = j
    row = 0
    newCor = {} # 
    newGrid = grid
    print("row:",row,"col:",col)
    while True:
        cont = grid[row][col] # cont = container that is blocking and needs to be moved. Here cont is set to top of col
        found = False
        print("cont =",cont)
        while cont == 0:    # Find first container to move that is blocking 
            row = row + 1   # Go down in row, same col, to find first blocking container
            print("HIIIII",row,"AA",col)
            cont = grid[row][col]
        if cont == grid[i][j]:
            break
        lCol = j-1
        rCol = j+1
        # print("rCol",rCol)
        # print("lCol",lCol)
        tempRow = len(grid)-1   # Set tempRow to bottom of the grid, or the last row
        #print("temprow:", tempRow)
        while (found is False):     # While a free spot hasnt been found
            #print("HIIIIIIIII")
            if lCol < 0 and rCol < 0:
                print("No free spaces anywhere on ship!")
                return {} 
            if tempRow < 0:
                tempRow = len(grid)-1
                lCol = lCol-1
                rCol = rCol+1
            if lCol >= 0 and grid[tempRow][lCol] == 0:
                newCor[cont] = tempRow,lCol
                temp = grid[row][col]
                grid[row][col] = 0
                grid[tempRow][lCol] = temp
                found = True
                break
            elif rCol >= 0 and grid[tempRow][rCol] == 0:
              #  print("tempRow:",tempRow,"rCol:",rCol)
                newCor[cont] = tempRow,rCol
                temp = grid[row][col]
                grid[row][col] = 0
                grid[tempRow][rCol] = temp
                found = True
                break
            else:
                tempRow = tempRow - 1
        row = row + 1

        
    return newCor                        
            
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

    # MAKE HASHMAP WITH WEIGHTS AND COORDS. USE WEIGHTS FROM BEST MOVE TO FIND COORDS OF BEST WEIGHT TO MOVE

def balance(grid):
    tempGrid = grid
    containers = {}
    gridCoords = getGCoord(grid)
    codeCoords = getCCoord(grid)
    #print("grid coords:",gridCoords)
    #print("code coords:",codeCoords)
    
    if len(codeCoords) == 0:
        return [], [], True   
    
    lhs, rhs, isBalanced = calculate_balance(grid)

    print("lhs:",lhs,"rhs:",rhs)
    
    if isBalanced:
        return None, True
    
    Steps, ShipGrid = [], []
    Half = len(grid[0]) // 2

    # print("HIIIIIII",coords)
    
    # print(lhsShip, rhsShip)
    
    while (not isBalanced):
        currContainer = []
        currVals = []
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
        #print("Coords of containers on side that is greater weight:",currContainer)        
        print("Container weights associated with the coords",currVals)
        side = 0 if lhs > rhs else 1
        bestContainerWeight = bestMove(currVals,lhs,rhs,side)
        print("Best container weight to move:",bestContainerWeight)

        print(containers[bestContainerWeight])

        block = {}
        if (canMove(grid,containers[bestContainerWeight][0],containers[bestContainerWeight][1])):
            print("Container can be moved!")
            moving = findOpenSpot(grid,lhs,rhs,1)
            print("moving:",moving)
        else:
            print("Container cannot be moved!")
            block = moveBlocked(grid,containers[bestContainerWeight][0],containers[bestContainerWeight][1])
            print("blocked:",block)
        #print(currContainer)
        #print("HEREEEEEEEEEEEE",currVals)
        
        #Compute Cost of moving each container to the other side
        
        
        #SIFT???
        
        
        #Move the container
        print("LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOL:",grid)
        
        #Update Containers
        isBalanced = True
    
    #Update Ships and return with Steps
    
    
    return 1 #Steps, ShipGrid, True
    
    

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
 

# 20, 30, 3, 7
# L, R, B = 
balance(ShipOne)
# print("Left:", L," Right:", R, "Balance:", B)

# L, R, B = 
#print(balance(ShipTwo, coordTwo))
# print("Left:", L," Right:", R, "Balance:", B)