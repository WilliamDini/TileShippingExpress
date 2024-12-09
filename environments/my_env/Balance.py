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
    # Should we actually move container in the way to furthest location??
    print()

def moveBlocked(grid, i, j):    # This is not done, dont call or run fails
    #print("HEEEEEEEEEEEEEEEEEEEEEEEEEEEE", len(grid)-1)
    row = 0
    col = j
    newCor = {} # 
    while True:
        cont = grid[row][col] # cont = container that is blocking and needs to be moved. Here cont is set to top of col
        found = False
        while cont == 0:    # Find first container to move that is blocking 
            row = row + 1   # Go down in row, same col, to find first blocking container
            cont = grid[row][col]
        if cont == grid[i][j]:
            break
        lCol = 0
        rCol = 0
        tempRow = len(grid)-1
        print("temprow:", tempRow)
        while (found is False):
            if (lCol < 0 or tempRow < 0):  # This current column is full and we are now out of bounds
                lCol = len(grid[row])-1    # reset cols to bottom of grid
                rCol = lCol
                print("HEEEEEEEEEEEEEEEEEEEEEEEEEEEE", lCol)
                tempRow = len(grid)-1
            if grid[tempRow][lCol] == 0:    # left of col is closest free spot so save that coord
                newCor[cont] = tempRow,lCol
                found = True
            elif grid[tempRow][rCol] == 0:  # right of col is closest free spot so save that coord
                newCor[cont] = tempRow,rCol
                found = True
            else:
                tempRow = tempRow - 1
        
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
    containers = {}
    gridCoords = getGCoord(grid)
    codeCoords = getCCoord(grid)
    #print("grid coords:",gridCoords)
    #print("code coords:",codeCoords)
    
    if len(codeCoords) == 0:
        return [], [], True   
    
    lhs, rhs, isBalanced = calculate_balance(grid)
    
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
                if ((Position[1] <= Half) and (grid[Position[0]][Position[1]] != 0)):
                    currContainer.append(Position)
                    currVals.append(grid[Position[0]][Position[1]])
                    containers[grid[Position[0]][Position[1]]] = Position
            
        else:
            for Position in codeCoords:
                print("X",Position)
                if ((Position[1] > Half) and (grid[Position[0]][Position[1]] != 0)):
                    currContainer.append(Position)
                    currVals.append(grid[Position[0]][Position[1]])

                    

        print("Code Coords:",codeCoords)
        print("Grid Coords:",gridCoords)
        print("Coords of containers on side that is greater weight:",currContainer)        
        print("Container weights associated with the coords",currVals)
        bestContainerWeight = bestMove(currVals,lhs,rhs,0)
        print("Best container weight to move:",bestContainerWeight)

        print(containers[bestContainerWeight])

        block = {}
        if (canMove(grid,containers[bestContainerWeight][0],containers[bestContainerWeight][1])):
            print("Container can be moved!")
        else:
            print("Container cannot be moved!")
            #block = moveBlocked(grid,containers[bestContainerWeight][0],containers[bestContainerWeight][1])
        #print(currContainer)
        #print("HEREEEEEEEEEEEE",currVals)
        
        #Compute Cost of moving each container to the other side
        
        
        #SIFT???
        
        
        #Move the container
        
        
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
        for Slot in range(len(Row)):
            if Slot <= Half:
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