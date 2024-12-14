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
    Halfsies = int(len(grid[0])) // 2
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
    #print("THIS RIGHT HEREE HAHAHAHA")
    # for g in goalSpots:
    #     print(g)

    # steps = []
    # nearSpot = list()
    sorted_weight = sorted(cons, reverse=True, key=lambda x: x[0]) # [Weight] = Position(x,y)
    #print("sortedwwwww",sorted_weight)
    weights = []
    for w in sorted_weight:
        weights.append(w[0])
  #  print("Sift:", sorted_weight)
   # print("All Coords:", positions)
    # row = 0
    # onleft=True
    # goalCol = len(grid[0])//2
    # goalRow = len(grid)
    
    # WHen moving containers that are blocking, you need to update their new location. In sorted_weight,
    # go in for loop to find container that matches weight, if len is more than 1 (theres duplicate),
    # check each coords until you find matching cords of blocked container that was just moved. once found
    # update coords

    for weight in weights:
        cons = getContainers(grid)
        #print("THIS WEIGHT",weight)
        pos = [sorted_weight[0][1][0],sorted_weight[0][1][1]] # Get position of heaviest container
        sorted_weight.pop(0)
       # print("sirteweught after pop:",sorted_weight)
        goalPos = goalSpots.pop(0)
       # print("HI",pos)
        if weight == grid[goalPos[0]][goalPos[1]] : # Check if it was already moved
           # print("ALREADAY IN GOALLLL")
            continue
        else:   # Container has not been moved!!!L!
            # Get goal pos
          #  print("THE ELSE")
          #  print("Goal pos!:",goalPos)
            # check if blocked
            if (grid[goalPos[0]][goalPos[1]]) != 0 and grid[goalPos[0]][goalPos[1]] != -1:
                tempRow = 0
                tempcon = grid[tempRow][goalPos[1]] # Container in col of container to move that is blocking goal spot
                while tempRow < len(grid) and tempcon == 0:   # While temprow < 8 and we are in empty con
                    tempRow += 1
                    tempcon = grid[tempRow][goalPos[1]]
              #      print("row in thiss",tempRow)
                tempcon = grid[tempRow][goalPos[1]] # Container in col of container to move that is blocking goal spot
             #   print("tempcon issss",tempcon)
            #    print("goalpos[1] isss:",goalPos[1])
            #    print("row issss",tempRow)
                cost += siftBlock(grid,tempRow,goalPos[1],movs,r,sorted_weight)  # Potentially move container
              #  print("THIS IS CUR POS x:",pos[0]," ",pos[1])
              #  print("THIS IS GOAL POS x:",goalPos[0]," ",goalPos[1])
                cost += calcCost(grid,pos[0],pos[1],goalPos[0],goalPos[1],movs,r)
                
              #  print("cost 2222",cost)
                temp = grid[pos[0]][pos[1]] 
                grid[pos[0]][pos[1]] = 0
                grid[goalPos[0]][goalPos[1]] = temp
            else:   # Not blocked so move container directly to goal spot
                temp = grid[pos[0]][pos[1]] 
                grid[pos[0]][pos[1]] = 0
                grid[goalPos[0]][goalPos[1]] = temp
      #  print("AFTER EACH ITER")
        #printG(grid)
        #EMPCOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO LOL
    #printG(grid)
    #print("cost 4444",cost)
    return cost

def siftBlock(grid,i,j,movs,r,sw): #i,j = loc of block container
    open = getOpenSpots(grid)
    newx,newy = 0,0
    min = 100000
    cost = 0
    for x in range(len(open)):
        res = manhattanDis([open[x][0],open[x][1]],[i,j])
        #print("openx",open[x][0]," openy",open[x][1])
        if res < min and validSpot(grid,open[x][0],open[x][1],i,j):
            #print("valid is:",open[x][0]," y is",open[x][1])
            #print("x = ",open[x][0],"y = ",open[x][1])
            newx = open[x][0]
            newy = open[x][1]
            #print("newx",newX,"newy",newY)
            min = res
    for con in sw:
        if con[0] == grid[i][j]:    # Found the value of blocked container to move
            #print("i",i," j",j)
            if con[1][0] == i and con[1][1] == j:   # Check if coords match the blocked container
              #  print("dada",newx," dwdwwdwdw",newy)
                con[1][0] = newx
                con[1][1] = newy
                break

    temp = grid[i][j]
    cost += calcCost(grid,i,j,newx,newy,movs,r)
   # print("cost 333",cost)
    grid[i][j] = 0
    grid[newx][newy] = temp
    return cost


def moveBlocked(grid, i, j,movements,r):    # WORKS NOWWWWWWWWWWWWWWWW 
    # print("i:",i," j:",j)
    # print("IN moveBlocked")
    # print("grid in moveBlocked",grid)
    min = 10000
    newX = 0
    newY = 0
    row = 0
    col = j
    cost = 0

    while True:
        open = getOpenSpots(grid)
        min = 10000
        # print("open",open)
        while row < len(grid) and grid[row][col] == 0:  # Start at top of col with ideal container, go down until blocking container is found
            row = row + 1
          #  print("ZZZZZ")
      #  print("row:",row," col:",col)
        if row == i and col == j:  # Stop once ideal container is found in col
            #print("BREAK")
            break   
        #print("block container",grid[row][col])
        for x in range(len(open)):
            res = manhattanDis([open[x][0],open[x][1]],[row,col])
            #print("openx",open[x][0]," openy",open[x][1])
            if res < min and validSpot(grid,open[x][0],open[x][1],row,col):
                #print("valid is:",open[x][0]," y is",open[x][1])
                #print("x = ",open[x][0],"y = ",open[x][1])
                newX = open[x][0]
                newY = open[x][1]
                #print("newx",newX,"newy",newY)
                min = res
        temp = grid[row][col]
        cost = cost + calcCost(grid,row,col,newX,newY,movements,r)
        grid[row][col] = 0
        grid[newX][newY] = temp
       # print("In moveBlocked")
       # print("startx:",row," starty:",col," endx:", newX, " endy:",newY)
        # print("grid during block:")
        # print("HIIII")
        # printG(grid)
        # print("")
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
    ##print("aa",grid[i][j])
    #print("i",i," j",j)
    #print("rowtemp",row_temp," j+1",j+1)
    label = str(row_temp)+","+str(j+1)
   # print("lab",r["7,2"])
    locname = r[label][0]
    locweight = r[label][1]
    movs.append(str(i)+" "+str(j)+" "+locweight+" "+locname)
    cost, tempx, tempy, nodes, count, movOff, movL, movR, offGrid = 0,i,j,{},1,False,False,False,0
    while True:   
        #print("THIS IS START")
       # print("Offgrid is",offGrid)
        visited = str(tempx) + "," + str(tempy)
       # print("THIS IS VISITED:",visited)
        nodes[visited]=1
        visiting = ""
       # print("STARTTTTTT")
        #print("x:",tempx,"y:",tempy)
        if tempx == x and tempy == y:
          #  print("GOALLLLLLLLLLLLLLLLLLLLLLLLLLLL")
            break
        c = {} # Coords dict
        # Check left cell
        if offGrid == 0:
           # print("AAAA")
            visiting = str(tempx)+","+str(tempy-1)
            #print(visiting)
            if (tempy-1 >= 0 and visiting not in nodes and grid[tempx][tempy-1] == 0):
                heur = manhattanDis([tempx,tempy-1],[x,y])
                if heur not in c:
                # print("heur added in left cell:",heur)
                    c[heur] = [tempx,tempy-1]
            else: 
                offGrid = offGrid+1
              #  print(1)
            # Check right cell
            visiting = str(tempx)+","+str(tempy+1)
           # print(visiting)
            if (tempy+1 < len(grid[0]) and visiting not in nodes and grid[tempx][tempy+1] == 0):
                heur = manhattanDis([tempx,tempy+1],[x,y])
                if heur not in c:
                    #print("heur added in right cell:",heur)
                    c[heur] = [tempx,tempy+1]
                   # print(c)
            else: 
                offGrid = offGrid+1
               # print(2)
            # Check below cell
            visiting = str(tempx+1)+","+str(tempy)
            if (tempx+1 < len(grid) and visiting not in nodes and grid[tempx+1][tempy] == 0):
                heur = manhattanDis([tempx+1,tempy],[x,y])
                if heur not in c:
                # print("heur added in down cell:",heur)
                    c[heur] = [tempx+1,tempy]
            else: 
                offGrid = offGrid+1
                #print(3)
            # Check above cell
            visiting = str(tempx-1)+","+str(tempy)
            if (tempx-1 >= 0) and visiting not in nodes and grid[tempx-1][tempy] == 0:
                heur = manhattanDis([tempx-1,tempy],[x,y])
                if heur not in c:
                    #print("heur added in above cell:",heur)
                    c[heur] = [tempx-1,tempy]
                    #print(c)
            else: 
                offGrid = offGrid+1
                #print(4)
        if offGrid == 4:
         #   print("DDDD")
            label = str(tempx) + "," + str(tempy)
            if movOff is False: # First time going off grid so only going up
            #    print("IF movOff is FALSE")
                cost = cost + 1
                movOff = True
                if grid[tempx][tempy+1] != 0: movR = True
                else: movL = True
                movs.append("(-1)"+","+str(tempy)+" 00000 UNUSED")
                count = count + 1
            # Moved to position above first row that has an empty slot below it on first row of grid
            elif grid[tempx][tempy] == 0 and label not in nodes:
              #  print("IAMHERE")
                movOff = False
                offGrid = 0
                cost = cost + 1
                movs.append("(-1)"+","+str(tempy)+" 00000 UNUSED")
                count = count + 1
            # If still moving above grid and full col is to the right
            elif movR is True and grid[tempx][tempy+1] != 0:
             #   print("RIGHTRTT")
                movR = True
                movL = False
                cost = cost + 1
                movs.append("(-1)"+","+str(tempy+1)+" 00000 UNUSED")
                tempy = tempy+1
                count = count + 1
            # If still moving above grid but space to right is 0!
            elif grid[tempx][tempy+1] == 0:
              #  print("RIGHT IS 0")
                movR = False
                movOff = False
                movL = False
                count = count + 1
                cost = cost + 2
                movs.append("(-1)"+","+str(tempy+1)+" 00000 UNUSED")
                tempy = tempy+1
            # If still moving above grid but space to left is 0!
            elif grid[tempx][tempy-1] == 0:
               # print("Left IS 0")
                movR = False
                movOff = False
                movL = False
                count = count + 1
                cost = cost + 2
                movs.append("(-1)"+","+str(tempy-1)+" 00000 UNUSED")
            # If still moving above grid and full col is to the left
            elif movL is True and grid[tempx][tempy-1] != 0:
              #  print("LEFT")
                movL = True
                movR = False
                tempy = tempy-1
                cost = cost+1
                #loc = 
                movs.append("(-1)"+","+str(tempy))
                count = count + 1
        if offGrid != 4:
           # print("Tempx:",tempx,"tempy:",tempy)
            if tempx == 0:
                row_temp = len(grid)
            else:
                row_temp = len(grid) - tempx
           # print("adjusted = Tempx:",row_temp,"tempy:",tempy+1)
            # print("aa",grid[i][j])
            # print("i",i," j",j)
            label = str(row_temp)+","+str(tempy+1)
        # print("lab",r["7,2"])
            sorted_c = dict(sorted(c.items()))
           # print("aa",sorted_c)
            optVal = list(sorted_c.keys())[0]
            newx = c[optVal][0]
            newy = c[optVal][1]
            #print("Tempx:",tempx,"tempy:",tempy)
            # label = str(tempx)+","+str(tempy)
            # for n in r.keys():
            #     print(n)
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
            #print("label:",label)
            r[label] = [name,weight]

            movs.append(str(newx)+" "+str(newy)+" "+weight+" "+name)
            cost = cost + 1
            count = count + 1
            offGrid = 0
   # print("cost 555555555",cost)
    return cost                                                    

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

def balance(r,grid):
    count = 0
    gridcpy = c.deepcopy(grid)
    contcpy = {}
    rcpy = c.deepcopy(r)
  #  print("Grid at start:")
    #printG(grid)
    containers = {}
    #gridCoords = getGCoord(grid)
    codeCoords = getCCoord(grid)
    #print("grid coords:",gridCoords)
    #print("code coords:",codeCoords)
    cost = 0
    
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
    #print("ADADAAADADADA")
    while (not isBalanced):      
        if count == 100:
           # print("GRID BEFORE SIFT:")
           # printG(gridcpy)
            movements = []
            print("Ship cannot be balanced. Begin Sift operation!")
            cost = sift(gridcpy,contcpy,movements,rcpy)
            return movements,cost
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
                if ((Position[1] < Half) and (grid[Position[0]][Position[1]] > 0)):
                    currContainer.append(Position)
                    currVals.append(grid[Position[0]][Position[1]])
                    containers[grid[Position[0]][Position[1]]] = Position
            
        else:
            for Position in codeCoords:
                #print("X",Position)
                if ((Position[1] >= Half) and (grid[Position[0]][Position[1]] > 0)):
                    currContainer.append(Position)
                    currVals.append(grid[Position[0]][Position[1]])
                    containers[grid[Position[0]][Position[1]]] = Position

        if count == 0:
            contcpy = containers

       # print("Code Coords:",codeCoords)
        # print("Grid Coords:",gridCoords)
        # print("Coords of containers on side that is greater weight:",currContainer)        
        # print("Container weights associated with the coords",currVals)

        side = 0 if lhs > rhs else 1
        # print("lhs:",lhs,"rhs:",rhs)
        # print("side:",side)
        bestContainerWeight = bestMove(currVals,lhs,rhs,side)
        #print("Best container weight to move:",bestContainerWeight)
       # print("")

        # print(containers[bestContainerWeight])

        if (not canMove(grid,containers[bestContainerWeight][0],containers[bestContainerWeight][1])):        
            # print("Container cannot be moved!")
            #print("Grid before moveBlocked",grid)
            cost = cost + moveBlocked(grid,containers[bestContainerWeight][0],containers[bestContainerWeight][1],movements,r)
          #  print("Printing grid after moving blocked")
            # print("HELOOLO")
         #   printG(grid)
         #   print("")

            #print("Grid after moveBlocked",grid)
        # print("Container can be moved!")
        newSide = 0 if side == 1 else 1
        cost = cost + moveContainer(grid,newSide,containers,bestContainerWeight,movements,r)

        #print("Temp movements")
        # for cc in movements:
        #     print(cc)
        #print("moving:",moving)
        #print(currContainer)
        #print("HEREEEEEEEEEEEE",currVals)
        
        #Compute Cost of moving each container to the other side
      #  print("Printing grid after moving ideal container")
       # print("THIS IS GRID")
       # printG(grid)
       # print("")
        
        #SIFT???
        
        
        #Move the container
        
        #Update Containers
        lhs, rhs, isBalanced = calculate_balance(grid)
        count+=1
    
    #Update Ships and return with Steps
    
    
    return movements,cost #Steps, ShipGrid, True
    
    

# Ship Grid (8, 12)
def calculate_balance(grid):
    lhsWeight = 0
    rhsWeight = 0
    isBalanced = False
    
    for Row in grid:
        Half = len(Row) // 2
        #print("ROWWWW",Row,"HALFFFF",Half)
        for Slot in range(len(Row)):
            if Row[Slot] == -1: continue
            elif Slot < Half:
                lhsWeight += Row[Slot]
            else:
                rhsWeight += Row[Slot]
    
    diff = (rhsWeight + lhsWeight) / 10
    #print(lhsWeight,rhsWeight)
    #print("act dyf",diff)
    if(abs(rhsWeight - lhsWeight) <= diff):
      #  print("Diff:",abs(rhsWeight - lhsWeight))
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

def readFile():
    PROJECT_DIR = Path(__file__).parent
   # print("--- Reading in the entire file:")

    path = PROJECT_DIR / 'ShipCase5.txt'
    contents = path.read_text()

    #print(contents[0][18])
    res = {}
    grid = []

   # print("\n--- Looping over the lines:")
    #print("HEHEHEH")
    lines = contents.splitlines()
    switch = "z"
    count = 0
    newList = []
    for l in lines:
        first = l[1:3]
        #print("f",first)
        #print("count",count)
        if count == 0:
            switch = first
        elif switch != first and count != 0:
           # print("bef",switch)
            switch = first
         #   print("aft",switch)
            grid.append(newList)
            newList = []
        x = int(l[1:3])
        y = int(l[4:6])
        loc = str(x)+","+str(y)
        name = (l[18:])
        weight = l[10:15]
        res[loc] = [name,weight]
        #print(name)
       # print("loc",loc)
       # print(res[loc])
        if weight == "00000" and name == "NAN":
            newList.append(-1)
        elif weight == "00000" and name != "NAN":
            newList.append(0)
        else:
            newList.append(int(weight))
        count = count+1
    grid.append(newList)
    #for r in res:
       # print(res[r])

    idx = 0
    for row in range(len(grid)-1,3,-1):
        temp = grid[idx]
        grid[idx] = grid[row]
        grid[row] = temp
        idx = idx + 1
    return res,grid

# def update(grid,dict):
#     d = {}
#     for row in len(grid):
#         for col in len(grid[row]):
#             temp = str(row)+","+str(col)
#             d[temp]=

    # idx = 0
    # for row in range(len(grid)-1,3,-1):
    #     temp = grid[idx]
    #     grid[idx] = grid[row]
    #     grid[row] = temp
    #     idx = idx + 1
    # return res, grid
        
def getVals(grid,val):
    return grid[val][0], grid[val][1]

r,g = readFile()
# for a in g:
#     print(a)
# print("HIHIHIHIHIHI",getVals(r,"8,5"))

# z = getGCoord(g)
# for m in z:
#    print(m)

m,c = balance(r,g)
print("TOTAL COST IS:",c)

print("movements")
for i in m:
    print(i)

# g = getGoals(g)
# print(g)

# mmm = []
# lp = calcCost(ShipOne,2,0,1,2,mmm)
# print("movements:",mmm)
# print("cost:",lp)

# [2,1], [2,2], [1,1], [1,2]

ShipTwo = [
            [6, 0, 0, 0],
            [4, 0, 0, 10]
        ]

coordOne = [[1,1], [1,2], [1,4], [2,1], [2,2]]
coordTwo = [[1,1], [1,4], [2,1]] 
 
# with open(r"C:\Users\varga\Documents\CS-179\project_repo\projo179\TileShippingExpress\environments\my_env") as f:
#     print(f.read())

# from pathlib import Path

# PROJECT_DIR = Path(__file__).parent

# print("--- Reading in the entire file:")

# path = PROJECT_DIR / 'ShipCase1.txt'
# contents = path.read_text()

# # print(contents[0][18])

# # print("\n--- Looping over the lines:")
# print("HEHEHEH")
# lines = contents.splitlines()
# print(lines[2][18])
# temp1 = lines[len(lines)-1][1:3]
# temp2 = lines[len(lines)-1][4:6]
# xxx = int(temp1)
# yyy = int(temp2)
# print("x:",xxx," y:",yyy)
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