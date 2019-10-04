import psphelper
from random import randrange
###########################DICE FUNCTION###########################
def dice():
    return [randrange(1, 5) for i in range(5)] #roll dice 5 values 4 faces

def diceSpecific(specificRoll, diceData):
    for i in specificRoll: 
        diceData[i] = randrange(1, 5) #roll specific dice 
    return diceData
#################INPUT FUNCTION############################
def chooseInput():
    def ListProcess(List,increase, minVal, maxVal):
        try:
            List = [int(i)+increase for i in List]#convert intString to int
        except ValueError:
            return [] #List contain non intString, fail to convert 
        return List if min(List)>=minVal and max(List)<=maxVal else [] #check range

    while True:
        userInput = input("Input > ").upper().split(" ")#uppercase and split
        if userInput and userInput[0] in ["ROLL" ,"CHEAT" ,"SAVE"]: #possible case
            choice, *restList = userInput #split the choice and restList
            if not restList and choice in ["SAVE","ROLL"]: #input with only choice
                return (choice, [])
            elif choice == "ROLL":#check specific roll
                if number := ListProcess(restList,-1,0,4):
                    return (choice,list(set(number))) 
            elif choice == "CHEAT":#check cheat
                if len(restList)==5 and (number := ListProcess(restList,0,1,4)):
                    return (choice,number)
        print("ERROR: Invalid input.") #not fullfill         
##############CALC SCORE FUNCTION#################
def scoreResult(diceData):
    diceCount = [diceData.count(i) for i in range(1,5)]#dC[i] = amt face i+1
    maxDice, sumDice = max(diceCount), sum(diceData) #max num of face and sum of dice
    
    S = [diceCount[i]*(i+1) for i in range(4)] #1S to 4S
    trio = sumDice if maxDice >= 3 else 0 #more than 3 same face
    quartet = sumDice if maxDice >= 4 else 0 #more than 4 same face
    band = 30 if 2 in diceCount and 3 in diceCount else 0 #2 and 3 same faces
    doremi = 20 if 0 not in diceCount else 0 #no 0 if all face exist 
    orchestra = 40 if 5 in diceCount else 0  #5 same faces

    return [*S, trio, quartet, band, doremi, orchestra]
#####Declare variables
playerRow = ["Player 1", "Player 2"]
categoryName = ["1S", "2S", "3S" , "4S", "Trio", "Quartet", "Band", "Doremi", "Orchestra"]
playerScore = [ [None]*9, [None]*9 ] 
playerTotalScore = [0,0]

for i in range (19): #Run game
    print(" Battle of the Sexes (B.O.T.S) ".center(80, "="))
    psphelper.ShowTableByList("Scoreboard", playerRow, categoryName, playerScore)
    print(f"Player 1: {playerTotalScore[0]}")
    print(f"Player 2: {playerTotalScore[1]}" + "\n")

    if i == 18:
        break #end game when turn is 18
    
    playerIndex = i%2#0 for player 1, 1 for player 2
    print(f"Player {playerIndex+1}")
    print("========")
    input("Press ENTER to roll dice.")

    specificRoll =  [] #specificRoll for specific roll
    for chance in range (1,4): #accept roll 3 times
        #fetch and show dice data, diceSpecific if specific roll
        diceData = diceSpecific(specificRoll, diceData) if specificRoll else dice()
        print(f"\nRoll #{chance} :{diceData} \n")
        #fetch and show score result
        categoryScore = scoreResult(diceData)
        psphelper.ShowTableByList("Category Score", [], categoryName, [categoryScore])
        if chance == 3:
            break #skip input when 3rd chance
        
        print("Input Options:")
        print("  SAVE           :- Accept these dice.")
        print("  ROLL           :- Re-roll ALL dice.")
        print("  ROLL d1 ... dn :- Re-roll specified dice only.")
        (choice, number) = chooseInput() #get user input
        if choice == "SAVE":
            break #end loop
        elif choice == "ROLL": 
            specificRoll = number #store require dice
        elif choice == "CHEAT":
            categoryScore = scoreResult(number)#update score with cheat code
            psphelper.ShowTableByList("Category Score", [], categoryName, [categoryScore])
            break #end loop
          
    while True:
        defaultInput = input("Enter your desired category: ")
        category = defaultInput.title() #correct input
        if category not in categoryName: #input not category
            print(f"ERROR: Category '{defaultInput}' does not exist.")
            continue #get input from player
        scoreIndex = categoryName.index(category) #find index base on category name
        if playerScore[playerIndex][scoreIndex] is not None: #index taken
            print(f"ERROR: Category '{defaultInput}' has been used.")
            continue
        break
    score = categoryScore[scoreIndex] #find score base on index
    playerScore[playerIndex][scoreIndex] = score #add category
    playerTotalScore[playerIndex] += score #add total
    psphelper.ClearScreen() #restart

#Game Ended Show winner
if playerTotalScore[0]>playerTotalScore[1]:
    input("Player 1 wins!")
elif playerTotalScore[1]>playerTotalScore[0]:
    input("Player 2 wins!")
else:
    input("It's a tie.")
