# StepsNeeded, Grid, isBalanced
# Grid is actual list of Rows and Cols
# Containers is list of container coords
from pathlib import Path
import copy
class Container():
    def __init__(self, xPos, yPos, weight, name, id):
        self.xPos = xPos
        self.yPos = yPos
        self.weight = weight
        self.name = name
        self.id = id
    
    def print(self):
        print("[{}, {}]  [{} lbs]  {}".format(self.xPos, self.yPos, self.weight, self.name), end="")

class Ship():
    def __init__(self):
        self.containers = []
    
    def print(self):
        for i in self.containers:
            i.print()
            
def printGrid(grid):
    for x in grid:
        print(x)
#------------------------------------------------------#
def notOpSift(grid, containers):
    
    steps, startingPos, goalPos, cost = [], [0,0], [], 0
    print("Start:", str(startingPos))
    printGrid(grid)
    shipBuff, cost = takeEveryThingOff(grid, cost)
    # print("")
    # print(grid)
    
    # sorted_weight = dict(sorted(containers.items(), reverse=True)) # [Weight] = Position(x,y)
    # weights = list(sorted_weight.keys()) # List of all Weights on the Ship
    positions = getLRSift(grid)
    
    print("L:", shipBuff)
    print("P:", positions)
    print("")
    
    
    incre, row = 0, len(grid) - 1
    while True:
        # print("INCR:", incre)
        goalPos = [row,positions[incre]]
        cost += manhattanDis(startingPos, goalPos)
        print("Start:", startingPos, "Goal:", goalPos, "Distance:", cost)
        
        val = shipBuff.pop(0)
        grid[goalPos[0]][goalPos[1]] = val
        
        print("POPPED:", val)
        
        if(incre >= len(grid[0]) - 1):
            # print("RUN")
            row -= 1
            incre = 0
            continue
        
        if(incre < len(grid[0]) - 1):
            incre+=1
        
        if len(shipBuff) == 0:
            break
    print("")
    # print("IDK")
    return grid

    """
    
        First Half      Second Half
        [0,1,2,3,4,5}   {6,7,8,9,10,11]

        6 -> 5 -> 7 -> 4 -> 8 -> 3 -> 9 -> 2 -> 10 -> 1 -> 11 -> 0
    
        Test
        [0,1} {2,3]
        
        2 -> 1 -> 3 -> 0
        
        
    """

def getLRSift(grid):
    Halfsies = len(grid[0]) // 2
    ListOfIndex = []
    ListOfIndex.append(Halfsies)
    # print("Half:", Halfsies, "Row Length:", len(grid[0]))
    
    for value in range(1, Halfsies + 1):
        ListOfIndex.append(Halfsies - value)
        RightRes = Halfsies + value
        # print(RightRes)
        if(RightRes < len(grid[0])):
            # print("HAllo")
            ListOfIndex.append(RightRes)
    
    print("")
    print(ListOfIndex)
    
    return ListOfIndex

def takeEveryThingOff(grid, cost):
    everyThingMustGo = list()
    row = 0
    print("")
    while True:
        for col in range(len(grid)):
            # print("[",col,",",row,"]")
            if grid[col][row] != 0 and grid[col][row] != -1: #Can Add NaN Check after for 0. -1 for unusable; 0 for empty
                everyThingMustGo.append(grid[col][row])
                cost += manhattanDis([col,row], [0,0])
                print("Moving", grid[col][row], "Starting Pos:", [col,row], "End Pos:", [0,0], "Cost:", cost)
                grid[col][row] = 0
                

        row += 1
        if row >= len(grid[0]):
            break
        
    # print("BYE BYE:", everyThingMustGo)
                
    return everyThingMustGo, cost

#Done
def manhattanDis(coords1, coords2):
    return (abs(coords1[0]- coords2[0]) + abs(coords1[1] - coords2[1]))

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
        #print(res[temp])
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


dictonary, grid = readFile()
notOpSift(grid, dictonary)
printGrid(grid)

#------------------------------------------------------#