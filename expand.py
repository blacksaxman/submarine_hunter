import os
import math, time, sys
import numpy as np
import random
from termcolor import colored


# reserve lines at the top and bottom for stuff
topReserve = 3
bottomReserve = 6

superUserNum1 = 0
superUserNum2 = 0
superUserNum3 = 0

# Define the shapes of the things
userSub = 'H'
enemySub = '%'
deadEnemySub = 'X'
waterStation = 'O'
deadWaterStation = '!'
ocean = '~'
firingSymbol = '*'

# Define the colors of the things
# documentation for colored is here https://pypi.org/project/colored/
oceanColor = 'white'
oceanBkgd = 'on_cyan'
enemySubColor = 'white'
enemySubBkgd = 'on_red'
userSubColor = 'white'
userSubBkgd = 'on_magenta'
waterStationColor = 'blue'
waterStationBkgd = 'on_yellow'
fireingColor = 'white'
fireingBkgd = 'on_green'

class waterstation:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.isKilled = -1
        self.symbol = waterStation
        self.color = waterStationColor
        self.bkgd = waterStationBkgd

    def kill(self):
        self.isKilled = 1
        self.symbol = deadWaterStation

class submarine:
    def __init__(self,x,y,flag):
        self.x = x
        self.y = y
        self.flag = flag # zero for user, 1 for AI
        self.detectionRadius = 5
        self.sonarRadius = 1000
        self.isKilled = -1
        self.isRevealed = 1
        self.weaponRange = 5
        self.symbol = userSub
        self.firingDirection = -1
        self.color = userSubColor
        self.bkgd = userSubBkgd
        self.firingX = np.arange(0,self.weaponRange)
        self.firingY = np.arange(0,self.weaponRange)
        if flag > 0:
            self.isRevealed = 0
            self.symbol = enemySub
            self.color = enemySubColor
            self.bkgd = enemySubBkgd
            self.weaponRange = 3 # reduced range for enemy subs


    def move(self,dx,dy):
        self.x += dx
        self.y += dy

    def kill(self):
        self.isKilled = 1
        self.symbol = deadEnemySub

    def reveal(self):
        self.isRevealed = 1

    def conceal(self):
        self.isRevealed = 0


def getSuperUserInput(option):
    global superUserNum1, superUserNum2

    # lets user set some values
    print(">>>>> " + option)
    n = int(input("Enter secret code : "))
    lst = []

    if n == 2:
        for i in range(0,n):
            sv = int(input())
            print("Accepted")
            lst.append(sv)

        print("You dirty dirty human...")
        superUserNum1 = lst[0]
        superUserNum2 = lst[1]
        time.sleep(.5)
        print("Loading cheats")
        time.sleep(1.5)
    else:
        print(colored("INCORRECT!! YOU DO NOT BELONG HERE!",'magenta'))
        time.sleep(2)

def getUserInput(option,cannedResponses):
    # setting up this function to handle all input output options, second
    # variable allows me to pass in a list of canned responses for the user
    # to input

    print(">>>>> " + option)
    if (len(cannedResponses) == 0):

        localUserInput = input(">>>>> Response: ")
    else:
        # allows me to do error checking
        acceptable = 0

        # if the user makes a bad input, repeat the prompt
        while (acceptable==0):
            for x in range(len(cannedResponses)):
                print(">>>>> " + "[" + str(x) + "] " + cannedResponses[x])
            localUserInput = input(">>>>> " + "Choose a respose (type a number): ")

            # error checking
            if (localUserInput.isnumeric() and int(localUserInput) < len(cannedResponses)):
                acceptable = 1
            else:
                print("BAD INPUT, PLEASE TYPE A NUMBER!")


    return localUserInput


def initObjects(combatGrid, rowBounds, colBounds,traitorFlag):
    # need to update the combat grid with the location of various objects

    # how many water stations are there?
    wsList = []
    nStations = 6
    for x in range(6):
        r = random.randint(0,rowBounds-1)
        c = random.randint(0,colBounds-1)
        wsList.append(waterstation(r,c))

        r = r*2 + 1
        c = c*2 + 1
        #combatGrid[r][c] = waterStation
        combatGrid[r][c] = colored(waterStation,waterStationColor,waterStationBkgd)

    # traitor flag determines how many bad guys there are
    nSubmarines = 3+superUserNum1
    if traitorFlag == 1:
        nSubmarines *= 2

    subList = []
    for x in range(nSubmarines+1):
        r = random.randint(0,rowBounds-1)
        c = random.randint(0,colBounds-1)
        flag = 1
        if x == 0:
            flag = 0
        tempSub = submarine(r,c,flag)
        subList.append(tempSub)
        if tempSub.isRevealed == 1:
            r = r*2 + 1
            c = c*2 + 1
            combatGrid[r][c] = colored(tempSub.symbol,tempSub.color,tempSub.bkgd)
            #colored

    return combatGrid, subList, wsList

def drawCombatGrid(combatGrid):
    print(makeLine('='))

    #get the number of rows
    rows = len(combatGrid)

    #get the number of columns
    cols = len(combatGrid[0])

    for x in range(rows):
        line = ''
        for y in range(cols):
            line+=combatGrid[x][y]
        print(line)

    print(makeLine('='))

def remainingEnemies(subList):
    count = -1
    for x in range(len(subList)):
        if subList[x].flag == 1 and subList[x].isKilled < 0:
            count +=1
    return count

def remainingStations(wsList):
    count = 0
    for x in range(len(wsList)):
        if wsList[x].isKilled<0:
            count+=1
    return count

def resetFiring(subList,combatGrid):
    x = subList[0].firingX
    y = subList[0].firingY
    for idx in range(len(x)):
        combatGrid[int((2*x[idx])+1)][int((2*y[idx])+1)] = colored(ocean,oceanColor,oceanBkgd)
    return combatGrid


def updateGame(combatGrid,subList,wsList,rowBounds, colBounds):
    # reset the old position back to water before drawing the new positions
    for ix in range(len(subList)):
        x = subList[ix].x
        y = subList[ix].y
        combatGrid[int((2*x)+1)][int((2*y)+1)] = colored(ocean,oceanColor,oceanBkgd)

    # check if the user killed anything
    if subList[0].firingDirection > -1:
        dir = subList[0].firingDirection
        if dir == 0:
            dy = -(np.arange(0,subList[0].weaponRange)+1)
            dx = 0*(np.arange(0,subList[0].weaponRange)+1)
        elif dir == 1:
            dy = (np.arange(0,subList[0].weaponRange)+1)
            dx = 0*(np.arange(0,subList[0].weaponRange)+1)
        elif dir == 2:
            dy = 0*(np.arange(0,subList[0].weaponRange)+1)
            dx = -(np.arange(0,subList[0].weaponRange)+1)
        else:
            dy = 0*(np.arange(0,subList[0].weaponRange)+1)
            dx = np.arange(0,subList[0].weaponRange)+1

        x = subList[0].x
        y = subList[0].y
        for idx in range(len(dx)):
            xf = np.minimum(np.maximum(x + dy[idx],0),rowBounds-1)
            yf = np.minimum(np.maximum(y + dx[idx],0),colBounds-1)
            combatGrid[int((2*xf)+1)][int((2*yf)+1)] = colored(firingSymbol,fireingColor,fireingBkgd)

            # store the values so we can clear them later
            subList[0].firingX[idx] = xf
            subList[0].firingY[idx] = yf

            pt1 = np.array((xf,yf))
            # check if any other subs are in range and kill them
            for idx2 in range(len(subList)-1):
                xtarg = subList[idx2+1].x
                ytarg = subList[idx2+1].y
                pt2 = np.array((xtarg,ytarg))
                dist = np.linalg.norm(pt1 - pt2)
                if dist == 0:
                    subList[idx2+1].kill()


    # move the enemy subs, for now they move randomly
    for x in range(len(subList)-1):
        # only move it if it isn't dead
        if (subList[x+1].isKilled < 1):
            moveValueInt = random.randint(0,3+superUserNum2)
            moveDirInt = random.randint(0,3)
            if moveDirInt == 0:
                dy = 1
                dx = 0
            elif moveDirInt ==1:
                dy = -1
                dx = 0
            elif moveDirInt == 2:
                dy = 0
                dx = -1
            else:
                dy = 0
                dx = 1
            dy *= moveValueInt
            dx *= moveValueInt
            subList[x+1].x =  np.minimum(np.maximum(subList[x+1].x+dy,0),rowBounds-1)
            subList[x+1].y = np.minimum(np.maximum(subList[x+1].y+dx,0),colBounds-1)

    # check if the enemy subs killed any water stations
    for x in range(len(subList)-1):
        point1 = np.array((subList[x+1].x,subList[x+1].y))
        for y in range(len(wsList)):
            point2 = np.array((wsList[y].x,wsList[y].y))
            dist = np.linalg.norm(point1 - point2)
            if dist < subList[x+1].weaponRange:
                wsList[y].kill()

    #print("c" + str(colBounds) + ", r" + str(rowBounds))
    # update combat grid positions
    for ix in range(len(subList)):
        x = subList[ix].x
        y = subList[ix].y
        #print("(" + str(ix) + " , " + str(x) + " , " + str(y) + ")")
        #combatGrid[int((2*x)+1)][int((2*y)+1)] = subList[ix].symbol

        # only display it if it is revealed
        if subList[ix].isRevealed == 1 or subList[ix].isKilled == 1:
            combatGrid[int((2*x)+1)][int((2*y)+1)] = colored(subList[ix].symbol,subList[ix].color,subList[ix].bkgd)


    for ix in range(len(wsList)):
        x = wsList[ix].x
        y = wsList[ix].y
        #combatGrid[int((2*x)+1)][int((2*y)+1)] = wsList[ix].symbol
        combatGrid[int((2*x)+1)][int((2*y)+1)] = colored(wsList[ix].symbol,wsList[ix].color,wsList[ix].bkgd)


    return combatGrid, subList, wsList

def resetReveals(subList):
    for x in range(len(subList)):
        if subList[x].flag == 1 and subList[x].isKilled < 0:
            subList[x].isRevealed = 0
    return subList

def checkReveals(subList):
    point1 = np.array((subList[0].x,subList[0].y))
    for x in range(len(subList) - 1):
        point2 = np.array((subList[x].x,subList[x].y))
        dist = np.linalg.norm(point1 - point2)
        if dist < subList[0].sonarRadius:
            subList[x].isRevealed = 1

    return subList

def checkProxReveals(subList):
    point1 = np.array((subList[0].x,subList[0].y))
    for x in range(len(subList) - 1):
        point2 = np.array((subList[x].x,subList[x].y))
        dist = np.linalg.norm(point1 - point2)
        if dist < subList[0].detectionRadius:
            subList[x].isRevealed = 1

    return subList

def makeCombatGrid():

    # this will make a line of values
    size = os.get_terminal_size()

    # how many columns are there?
    cols = size.columns
    lines = size.lines

    # define the grid here

    # we need an odd number of rows to make the grid
    gridRows = lines - topReserve - bottomReserve
    if (gridRows % 2) == 0:
        gridRows-=1

    gridCols = cols - 2
    if (gridCols % 2) == 0:
        gridCols-=1

    #combatGrid = [[None]*gridCols]*gridRows
    combatGrid = [[None]*gridCols for _ in range(gridRows)]

    for x in range(gridRows):
        for y in range(gridCols):
            combatGrid[x][y] = colored(ocean,oceanColor,oceanBkgd)

    for x in range(0,gridRows,2):
        temp = combatGrid[x]
        for y in range(0,gridCols,1):
            temp[y] = '—'
        combatGrid[x] = temp

    for x in range(1,gridRows,2):
        temp = combatGrid[x]
        for y in range(0,gridCols,2):
            temp[y] = '|'
        combatGrid[x] = temp

    # go ahead and define the bounds of where the ship can actually be
    rowBounds = int((gridRows-1)/2)
    colBounds = int((gridCols-1)/2)

    print(cols)
    print(colBounds)
    print(lines)
    print(rowBounds)

    return combatGrid, rowBounds, colBounds

def convert2dIndex(row,col,rowlength):
    return (row * rowlength) + col

def makeLine(symbol):
    # this will make a line of values
    size = os.get_terminal_size()

    # how many columns are there?
    cols = size.columns

    # make a string that is a line consisting fully of whatever symbol was input
    # first make sure it is a SINGLE value and if not just use the first value
    if (len(symbol) > 1):
        symbol = symbol[0]

    line = ''
    for x in range(cols-1):
        line += symbol

    return line

def makeBorder(symbol):
    # this will make a line of values only at the edges of your terminal
    size = os.get_terminal_size()

    # how many columns are there?
    cols = size.columns

    # make a string that is a line consisting fully of whatever symbol was input
    # first make sure it is a SINGLE value and if not just use the first value
    if (len(symbol) > 1):
        symbol = symbol[0]

    line = symbol
    for x in range(cols-3):
        line += ' '

    line += symbol

    return line

def makeTextInBorder(symbol,text):
    # this will make a line of values only at the edges of your terminal
    size = os.get_terminal_size()

    # how many columns are there?
    cols = size.columns

    # figure out how much text there is relative to the center of the screen
    tlen = len(text)

    # have to adjust the middle by hte length of the text
    adj = math.floor(tlen/2)

    # where is the middle of the terminal?
    termMid = math.floor(cols/2) - adj;

    line = symbol

    # remember range(a,b) is numbers from a to b, non inclusive of b
    c = 0
    for x in range(termMid):
        line += ' '
        c += 1

    for x in range(tlen):
        line += text[x]
        c += 1

    for x in range(c,cols-3):
        line += ' '

    line += symbol

    return line

def clearScreen():
    # the purpose of this is to

    # this will make a line of values only at the edges of your terminal
    size = os.get_terminal_size()

    # how many columns are there?
    cols = size.lines

    for x in range(cols):
        print()

def makeSplashScreen():
    # Every great game has to have a great title screen
    sym = "&"

    # this will make a line of values only at the edges of your terminal
    size = os.get_terminal_size()

    # how many columns are there?
    cols = size.lines

    spacing = math.floor(cols/4)

    for x in range(spacing):
        print(makeLine(sym))
    for x in range(spacing):
        print(makeBorder(sym))

    title = "SUBMARINE HUNTER: ASCII BUT DEADLY"
    print(makeTextInBorder(sym,title))
    author = "JOHNNY LEE WORTHY III"
    print(makeTextInBorder(sym,author))
    version = "VERSION 0.0.1"
    print(makeTextInBorder(sym,version))

    for x in range(spacing):
        print(makeBorder(sym))
    for x in range(spacing):
        print(makeLine(sym))


def timeDelayedText(text,delayRate):
    # this function will make it appear like the information/text is being sent
    # over a slow connection to be more dramatic

    for letter in text:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(delayRate)

    sys.stdout.write('\n')
    # for x in range(len(text)-1):
    #     #time.sleep(delayRate)
    #
    #     for x2 in range(int(1E7)):
    #         trash = math.sqrt(3.986E5)
    #
    #     print(text[x],sep='', end='')
    #
    #
    # # still need to print the last value
    # print(text[len(text)-1])
