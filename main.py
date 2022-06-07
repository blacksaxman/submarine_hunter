# This is a starter for a text based game in python.
# fill it in and tell a story that would be fun to play

from expand import *
from storyboarding import *
import os, time
from termcolor import colored

# I use multiple modules as an example for you to try and replicate to keep your
# story neat and get used to using them

# Basic control flow is what this file mostly deals with and the end goal is
# to let others use it. Try to make your code so it doesn’t break easily.

ocean = '~'
oceanColor = 'white'
oceanBkgd = 'on_cyan'

def main():

    # need this for colors to show up in the terminal
    os.system('color')

    # warning to the user
    print("WARNING: For best experience, do not use PowerShell terminal")
    time.sleep(1.5)

    # always start from a clean terminal
    clearScreen()

    # show the spash screen first! Always take credit for your work
    makeSplashScreen()
    input("Press Enter to continue...")

    # now show the title screen for the game, this is the first time
    # they'll see options and have thigns to input
    userTitleResponse = makeTitleScreen()

    # gameState controls what when we exit, but need to map userTitleResponse
    # to a game state
    if userTitleResponse == 2:
        gameState = 0
    else:
        gameState = 1

    # whatToDo should be a number, if it is 0 then we start the game
    while (gameState > 0):

        # if statement, if we want to look at the rules then show them
        if userTitleResponse == 1:
            makeGameRules()
            input("Press Enter to continue...")
            userTitleResponse = makeTitleScreen()
            if userTitleResponse == 2:
                gameState = 0
            else:
                gameState = 1
        else:
            # start the game!

            # give some cheats
            if userTitleResponse==3:
                getSuperUserInput(colored("Careful, they be dragons ahead",'red'))
                username = "Slick_Rick"
                commandResponse = 0
            else:
                # only show background if they didn't cheat
                makeBackgroundStory()
                username, commandResponse = makeIntroText()
            #username = "J"
            #commandResponse = 0

            if commandResponse < 2:
                traitorFlag = 0
            else:
                traitorFlag = 1

            combatGrid, cgrows, cgcols = makeCombatGrid()

            combatGrid, subList, wsList = initObjects(combatGrid, (cgrows), (cgcols),traitorFlag)
            for ix in range(len(subList)):
                x = subList[ix].x
                y = subList[ix].y
                print("(" + str(ix) + " , " + str(x) + " , " + str(y) + ")")
            subList = checkProxReveals(subList)


            isPlaying = 1
            turnCounter = 0
            clearFires = 0

            while (isPlaying>0):
                turnCounter+=1
                clearScreen()
                print("Battlefield Europa - Captain " + username + " --- Turn: " + str(turnCounter) +" . Remaining Stations: "+str(remainingStations(wsList))+" --- Remaining Enemies: "+str(remainingEnemies(subList)))
                drawCombatGrid(combatGrid)

                possibleResponses = ["Move ","Fire weapon! (Weapon range = 5)","Use Sonar (Detection range = 10)","Quit"]
                commandResponse = getUserInput("Your orders, Captain " + username + "?",possibleResponses)

                # clear fires of the screen
                if clearFires == 1:
                    clearFires = 0
                    combatGrid = resetFiring(subList,combatGrid)

                # for ease of handling
                commandResponse = int(commandResponse)

                if commandResponse == 3:
                    isPlaying = 0
                    gameState = 0
                    endCondition = 2
                else:
                    # need to follow up on what additional inputs we need from the user
                    if commandResponse == 0:
                        #move input handling
                        clearScreen()
                        print("Battlefield Europa - Captain " + username + " --- Turn: " + str(turnCounter) +" . Remaining Stations: "+str(remainingStations(wsList))+" --- Remaining Enemies: "+str(remainingEnemies(subList)))
                        drawCombatGrid(combatGrid)
                        possibleResponses = ["0","1","2","3","4","5"]
                        moveValue = getUserInput("How far to move?",possibleResponses)
                        moveValueInt = int(moveValue)

                        clearScreen()
                        print("Battlefield Europa - Captain " + username + " --- Turn: " + str(turnCounter) +" . Remaining Stations: "+str(remainingStations(wsList))+" --- Remaining Enemies: "+str(remainingEnemies(subList)))
                        drawCombatGrid(combatGrid)
                        possibleDirections = ["up","down","left","right"]
                        moveDir = getUserInput("Which Direction?",possibleDirections)
                        moveDirInt = int(moveDir)

                        # delete the old user sub position from the map
                        x = subList[0].x
                        y = subList[0].y
                        combatGrid[int((2*x)+1)][int((2*y)+1)] = colored(ocean,oceanColor,oceanBkgd)

                        # set the new position of the user sub
                        if moveDirInt == 0:
                            dy = -1
                            dx = 0
                        elif moveDirInt ==1:
                            dy = 1
                            dx = 0
                        elif moveDirInt == 2:
                            dy = 0
                            dx = -1
                        else:
                            dy = 0
                            dx = 1

                        dy *= moveValueInt
                        dx *= moveValueInt

                        subList[0].x+=dy
                        subList[0].y+=dx

                    elif commandResponse == 1:
                        clearScreen()
                        print("Battlefield Europa - Captain " + username + " --- Turn: " + str(turnCounter) +" . Remaining Stations: "+str(remainingStations(wsList))+" --- Remaining Enemies: "+str(remainingEnemies(subList)))
                        drawCombatGrid(combatGrid)
                        possibleDirections = ["up","down","left","right"]
                        firDir = getUserInput("Which Direction to Fire? (Weapon has range of 5 cells)",possibleDirections)
                        subList[0].firingDirection = int(firDir)
                        clearFires = 1

                    elif commandResponse == 2:
                        subList = checkReveals(subList)

                    subList = checkProxReveals(subList)
                    combatGrid, subList, wsList = updateGame(combatGrid,subList,wsList,cgrows, cgcols)
                    for ix in range(len(subList)):
                        x = subList[ix].x
                        y = subList[ix].y
                        print("(" + str(ix) + " , " + str(x) + " , " + str(y) + ")")
                    drawCombatGrid(combatGrid)
                    # at the end of the turn always reset the reveal status
                    subList = resetReveals(subList)

                    # reset the firing Direction
                    subList[0].firingDirection = -1

                # conditions to end the game go here
                if remainingEnemies(subList)==0:
                    #victory
                    endCondition = 0
                    isPlaying = 0
                elif remainingStations(wsList)==0:
                    endCondition = 1
                    isPlaying = 0

            # for now just end the game
            gameState = 0

            # print stats (could give a score in a future update!)
            print(colored("Battlefield Europa - Captain " + username + " --- Turn: " + str(turnCounter) +" . Remaining Stations: "+str(remainingStations(wsList))+" --- Remaining Enemies: "+str(remainingEnemies(subList)),'red','on_white'))
            makeGoodByeScreen(endCondition)


# Remove this and try to run your code to try and understand what it does so
# if you write a main module and its not working you can tell why.
if __name__ == '__main__':
    main()
