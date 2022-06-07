from expand import *
import time


# make some text output speeds
slow = .1
med = .05
fast = .01

userSub = 'H'
enemySub = '%'
deadEnemySub = 'X'
waterStation = 'O'
deadWaterStation = '!'
ocean = '~'
firingSymbol = '*'



def makeGoodByeScreen(endCondition):

    if endCondition == 0:
        endText = "Congrats, VICTORY!"
    elif endCondition == 2:
        endText = "QUITTERS WILL NOT BE TOLERATED"
    else:
        endText = "DEFEAT."

    for i in range(10):
        print("")

    sym = "8"

    # this will make a line of values only at the edges of your terminal
    size = os.get_terminal_size()

    # how many columns are there?
    cols = size.lines

    spacing = 1

    for x in range(spacing):
        print(makeLine(sym))
    for x in range(spacing):
        print(makeBorder(sym))

    title = "Thank you for playing SUBMARINE HUNTER: ASCII BUT DEADLY"
    print(makeTextInBorder(sym,title))

    print(makeBorder(sym))
    print(makeBorder(sym))
    print(makeTextInBorder(sym,endText))
    print(makeBorder(sym))
    print(makeBorder(sym))
    print(makeTextInBorder(sym,"(Scroll up to see the map if you played)"))
    print(makeBorder(sym))
    print(makeBorder(sym))

    for x in range(spacing):
        print(makeLine(sym))


def makeTitleScreen():

    clearScreen()

    # Every great game has to have a great title screen
    sym = "8"

    # this will make a line of values only at the edges of your terminal
    size = os.get_terminal_size()

    # how many columns are there?
    cols = size.lines

    spacing = 1

    for x in range(spacing):
        print(makeLine(sym))
    for x in range(spacing):
        print(makeBorder(sym))

    title = "SUBMARINE HUNTER: ASCII BUT DEADLY"
    print(makeTextInBorder(sym,title))

    print(makeBorder(sym))
    print(makeBorder(sym))
    print(makeTextInBorder(sym,"PLAY"))
    print(makeBorder(sym))
    print(makeBorder(sym))
    print(makeTextInBorder(sym,"HOW TO PLAY"))
    print(makeBorder(sym))
    print(makeBorder(sym))
    print(makeTextInBorder(sym,"QUIT"))

    for x in range(spacing):
        print(makeBorder(sym))
    for x in range(spacing):
        print(makeLine(sym))

    possibleResponses = ["PLAY","HOW TO PLAY","QUIT"," "]
    commandResponse = getUserInput("How would you like to proceed?",possibleResponses)

    return int(commandResponse)

def makeBackgroundStory():

    clearScreen()

    # this will be the opening screen
    title = "SUBMARINE HUNTER: ASCII BUT DEADLY"

    print(makeTextInBorder(" ",title))
    print("")
    print("")
    timeDelayedText("It is the year 2145, humans finally begun to explore the inner planets and their moons.  ",fast)
    time.sleep(1)
    timeDelayedText("The Earth, however, is divided into two main factions after the Russia-Ukraine conflict.  ",fast)
    time.sleep(1)
    timeDelayedText("The United Nations of Soverign Democracies (UNSD) represents the countries that fought for the freedom of Ukraine.  ",fast)
    time.sleep(1)
    timeDelayedText("The Republic Peoples Nations (RPN) represents the countries that banded together to ultimately help Russia (and eventually China) dominate the east.  ",fast)
    time.sleep(1)
    timeDelayedText("However, this war ended in 2040 and in the 100 years since these two factions have made incredible scientific breakthroughs.  ",fast)
    time.sleep(1)
    print("")
    timeDelayedText("The biggest was the ability to launch submarines into orbit.  ",fast)
    time.sleep(1)
    timeDelayedText("Submarines are the perfect expeditionary vehichle: durable, long duration, combat capable, independent.  ",fast)
    time.sleep(1)
    timeDelayedText("The UNSD and RPN had the perfect tools to establish a foothold on the oceanic moons of Titan, Enceladus, and Europa. ",fast)
    time.sleep(1)
    timeDelayedText("Each nation needs the water these moons abudantly provide as Earth's freshwater supply trickles to its last drops",fast)
    time.sleep(1)
    timeDelayedText("Controlling these planets are the UNSD's and RPN's main objectives",fast)
    time.sleep(1)
    timeDelayedText("The UNSD Interplanetary Naval Force (INF) and the RPN Exo-Liberation Navy (ELN) have been entrenched in warfare on Europa, attempting to stake claim on the closest source of clean water...",fast)
    time.sleep(1)

    print("")
    timeDelayedText("Your story begins on Europa as captain of the INF vessel Trident of Poseidon, commanded to protect the UNSD water harvesting operation.", fast)
    print("")

    time.sleep(1)
    input("Press Enter to continue...")

def makeGameRules():
    clearScreen()
    # every good game needs some rules
    print("This is a turn based game, you must kill all enemy targets to survive.")
    print("You will be shown a map, on this map you will see several symbols.")
    print("The location of your submarine will be shown as " + userSub)
    print("The location of the enemy submarine(s) will be shown as " + enemySub + " but only if it is detectable!")
    print("The location of UNSD water stations will be shown as " + waterStation)
    print("Protect the water stations, they're worth extra points! (Also you lose the game if all water stations are destroyed)")
    print("Each turn you will be given the option to Fire Weapon, Move, or Use Sonar.")
    print("Moving is a good way to find the enemy sub(s).")
    print("Using sonar is necessary to find the enemy, submarines are hard to detect from far away, sonar lets you try and hone in on where they might be.")
    print("If you are within range, the enemy will be detectable without sonar, fire away!")
    print("Really it is pretty self explanatory, best way to figure it out is to just play the game!")
    print("Your score at the end depends on how many turns you take, how many shots you take, and how many water Stations survive (To be implemented)")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("Oh, the enemy subs will move randomly and if they are close to a water station it will be destroyed!")
    print("If a station is destroyed it means an enemy sub must be nearby")

def makeIntroText():
    # this function will handle the introduction to the user about the game

    # make it clear that we are breaking from the makeSplashScreen
    clearScreen()

    # Lets get into the story!
    print('_')
    print('_')



    timeDelayedText(makeLine('-'),med)

    timeDelayedText(makeTextInBorder('!','SECURE CONNECTION ESTABLISHED'),fast)
    timeDelayedText(makeTextInBorder('!','CLASSIFIED TOP SECRET'),fast)

    username = getUserInput("Enter your first name",[])

    print("")
    timeDelayedText("CAPTAIN " + username,fast)
    timeDelayedText("This is Admiral Turner, Commander of the UNSD Europa Expeditionary Water Combat Force (EXWCF)",med)
    timeDelayedText("We just detected an enemy submarine squadron dropping onto Europa",med)
    timeDelayedText("Your orders are to locate and neutralize this submarine ASAP",med)
    timeDelayedText("You must protect UNSD control of water on Europa at all cost",med)

    time.sleep(1)
    print("...")
    possibleResponses = ["Roger","Copy","Negative, I'm a RPN spy, the ship is mine now!"]
    commandResponse = getUserInput("How do you respond?",possibleResponses)

    # We'll use the responses to figure out which game mode to be in
    # if they accept the mission we'll run in normal mode (1 v 1)
    # if they decline the mission then it will run in hard mode (4 v 1) and
    # they will need to escape!
    if (int(commandResponse)<2):
        timeDelayedText("Good Hunting CAPTAIN " + username,fast)
        timeDelayedText("Admiral Turner out",fast)
    else:
        # give the adminal some time to process this insubordination!
        print("...")
        time.sleep(1)
        print("...")
        timeDelayedText("IT'S TREASON THEN!",med)
        timeDelayedText("Expect the full fleet force coming after you CAPTAIN " + username,med)
        timeDelayedText("You are a traitorous scum",med)
        timeDelayedText("Turner out",med)

    timeDelayedText(makeLine("-"),fast)
    timeDelayedText(makeTextInBorder('!','CLASSIFIED TOP SECRET'),fast)
    timeDelayedText(makeTextInBorder('!','SECURE CONNECTION TERMINATED'),fast)

    return username, int(commandResponse)
