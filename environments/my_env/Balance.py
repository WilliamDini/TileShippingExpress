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

def balance(grid, containers):
    
    if len(containers) == 0:
        return [], [], True   
    
    lhsShip, rhsShip, isBalanced = calculate_balance(grid)
    
    if isBalanced:
        return None, True
    
    Steps, ShipGrid = [], []
    Half = len(grid[0]) // 2
    
    # print(lhsShip, rhsShip)
    
    while (not isBalanced):
        currContainer = []
        currVals = []
        #Check Max Iteration

        #Pick Side to Start on
        if lhsShip > rhsShip:
            for Position in containers:
                # print(Position)
                if ((Position[1] <= Half) and (grid[Position[0] - 1][Position[1] - 1] != 0)):
                    currContainer.append(Position)
                    currVals.append(grid[Position[0] - 1][Position[1] - 1])
        else:
            for Position in containers:
                if ((Position[1] > Half) and (grid[Position[0] - 1][Position[1] - 1] != 0)):
                    currContainer.append(Position)

                    
        print(currContainer)
        print(currVals)
        
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
print(balance(ShipOne, coordOne))
# print("Left:", L," Right:", R, "Balance:", B)

# L, R, B = 
print(balance(ShipTwo, coordTwo))
# print("Left:", L," Right:", R, "Balance:", B)


