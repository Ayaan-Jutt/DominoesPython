#******************************************************
# Assignment 2 Task 2: Play the game of Dominoes
# Author: Ayaan Jutt
# Collaborators/References: Stack and CircularQueue taken from CMPUT 175 labs
#******************************************************
from setDominoes import Domino, DominoDeck, DominoStack
class Table():
    def __init__(self):
        """input: N/A
        output: None
        sets up the table of Dominos, using a deck and stack 
        """
        #initialize a deck, a grid, and a list of stacks 
        
        self.__dominoDeck = DominoDeck()
        self.__dominoGrid = [ [None, None,None,None,None,None,None],
                       [None, None,None,None,None,None,None],
                       [None, None,None,None,None,None,None],
                       [None, None,None,None,None,None,None] ]
        self.__dominoStacks = [DominoStack(), DominoStack(), DominoStack()]

    def dealGrid(self, useFile):
        """input: a boolean that will determine whether or not we should use a file
        output: None
        checks whether or not the user wants to use a file, and populates the dominoGrid
        """
        #try this...
        try:
            #populate the file calling the populate function and the argument useFile
            self.__dominoDeck.populate(useFile)
            #if the deck isEmpty raise an exception saying so
            if self.__dominoDeck.isEmpty():
                raise Exception('Thank you for playing.')
            #go through the rows and columns,
            for row in range(0,4):
                for column in range(0,7):
                    #add a domino at that position 
                    self.__dominoGrid[row][column] = self.__dominoDeck.deal()
        #if the exception is raised, print the exception
        except Exception as gameOver:
            print(gameOver)
    def select(self, row, col):
        """input: an int for the column and an int for the row
        output: a domino at the row, col position
        Takes out a domino from a specified row and column, and if it exists, replace the domino with ***
        """
        #make sure the row and the column is an int 
        assert type(row) == int and type(col) == int, "Row and Column need to be integers"
        #try this...
        try:
            #get the row and column size
            row_size = self.getNumRows() 
            col_size = self.getNumColumns()
            #if either the row or the column is greater than the size, raise an exception
            if row > row_size or col > col_size:
                raise Exception("Error: Cannot go beyond the row index of: "+str(row_size)+" or the column index of: "+str(col_size))
            #else select a domino at that position
            selectedDomino = self.__dominoGrid[row][col]
            #if the domino is empty, raise an exception
            if selectedDomino == '***':
                raise Exception('There is no domino at row '+str(row)+', column' +str(col))
            #else turnover the chosen domino, return the selectedDomino, and the position we got the domino from is empty 
            selectedDomino.turnOver()
            self.__dominoGrid[row][col] = '***'
            return selectedDomino
        #if an exception is raised, print it
        except Exception as inst:
            print(inst)
    def playDomino(self, domino, stackNum):
        """input: a domino to add to the stack
        a stack that we are adding the domino to
        output: a boolean
        Adds a domino into the stack, returns true if it can, false otherwise
        """
        #check if the stackNum is an int 
        assert type(stackNum) == int, 'The index of the stack should be an int'
        assert type(domino) == Domino, 'The domino needs to be of the Domino class'
        #try pushing the domino on a stack at position stackNum
        self.__dominoStacks[stackNum].push(domino)
        #if the top of the dominoStack matches the top of the domino we want to add
        if self.__dominoStacks[stackNum].peek() == domino.getTop():
            #print success and return true
            print('Playing ' +str(domino) + ' on stack '+str(stackNum)+': Success!')
            return True        
        else:
            #else print fail, and return false
            print('Playing ' +str(domino) + ' on stack '+str(stackNum)+': Cannot play '+str(domino) +' on stack '+ str(stackNum))
            return False
    def isWinner(self):
        """input: N/A
        output: A boolean 
        returns whether or not any of the stacks sizes are 6, if they are, return true
        """
        return self.__dominoStacks[0].size() == 6 or self.__dominoStacks[1].size() == 6 or self.__dominoStacks[2].size()== 6
    def getNumStacks(self):
        """input: N/A
        output: The number of stacks
        returns how many dominoStacks there are"""
        return len(self.__dominoStacks)
    def getNumRows(self):
        """input: N/A
        output: the rows of a grid
        returns the amount of rows in a grid
        """
        return len(self.__dominoGrid)
    def getNumColumns(self):
        """input: N/A
        output: The columns of a grid
        returns the amount of columns in a grid
        """
        return len(self.__dominoGrid[0])
    def __numDisplay(self, footerItem):
        """input: a str that will be used as a footer/header
        output: a display for the columns, and a string for the footer
        creates a numbered column, and a footer for the str() display
        """
        #start off with 10 spaces to the right 
        numDisplay = '%10s'%''
        #go through every num, add it to the string with 12 spaces to the right 
        for num in range(len(self.__dominoGrid[0])):
            numDisplay = numDisplay + str(num)+ '%12s'%''
        #the displayFooter will be created by taking the param. and multiplied with the length of the numDisplay
        displayFooter = footerItem * (len(numDisplay))  
        #return them 
        return numDisplay, displayFooter
    
    def __dominoStr(self, displayStr, covered = True):
        """input: a string containing the current displayStr, and an optional boolean param/arg that will reveal or hide the domino
        output: a new, updated displayStr containing all the dominoes 
        turns every domino in the grid into a string and adds it into the displayStr so we can display it
        """
        #if we do not choose to add in the second arg,
        if covered:
            #go through every row of the grid, and create a temp string with 4 spaces to the left
            #then go through every column
            for row in range(len(self.__dominoGrid)):
                tempDisplay = '%-4s'%str(row) 
                for col in range(len(self.__dominoGrid[row])):
                    #the temp display will be updated with the string before it, the str domino with a specific center
                    tempDisplay = tempDisplay+ str(self.__dominoGrid[row][col]).center(13) 
                #after we go through one row, update the displayStr with itself and the new tempDisplay with a \n
                displayStr = displayStr + tempDisplay + '\n'
        else:
            #if it isn't covered, do teh same thing as before
            for row in range(len(self.__dominoGrid)):
                tempDisplay = '%-4s'%str(row) 
                for col in range(len(self.__dominoGrid[row])):
                    #before we add it to the temp display, turn the dodmino over. After adding it, turn the domino back over
                    turnedDomino = self.__dominoGrid[row][col]
                    turnedDomino.turnOver()
                    tempDisplay = tempDisplay+ str(turnedDomino).center(13) 
                    turnedDomino.turnOver()
                displayStr = displayStr + tempDisplay + '\n'
        #return the updated string 
        return displayStr
    def __str__(self):
        """input: N/A
        output: A string version of a table
        creates a table with labeled columns, rows, and dominoes
        """
        #start off the display string, create an empty string for the stack display, call a function to create the numDisplay and the footer
        displayStr = 'Selection Grid:\n'
        stackDisplay = ''
        numDisplay, displayFooter = self.__numDisplay('-')
        #update the displayStr with itself and the numDisplay + a new line 
        displayStr = displayStr + numDisplay + '\n'
        #update the displayStr with dominoes and a dominostack string
        displayStr = self.__dominoStr(displayStr) + '\nDomino Stacks:\n'
        #go through every stack, update the stackDisplay with itself, the number of the stack we're looking at, and the dominoes within the stack
        for stackNum in range(len(self.__dominoStacks)):
            stackDisplay = stackDisplay + str(stackNum) + '|| '+str(self.__dominoStacks[stackNum]) +'\n'
        #update the displayStr with itself, the stacks and a footer, then return it 
        displayStr = displayStr + stackDisplay + displayFooter
        return displayStr
    def revealGrid(self):
        """input: N/A
        output: a revealed version of the domino grid
        shows the domino locations of the Domino grid, with columns and rows labeled 
        """
        #create two intitial strings
        displayStr = 'For testing purposes, the grid contains:\n'
        numDisplay = '%10s'%''
        #update the numdisplay and create the footer with the called function 
        numDisplay, displayFooter = self.__numDisplay('/')
        #create a variable to add into the __dominoStr method so we can have uncovered dominoes 
        hidden = False 
        #update the displayStr with a footer, then itself with a numDisplay, the dominoes and the displayFooter again  and return it 
        displayStr = displayFooter +'\n'+ displayStr + numDisplay + '\n' 
        displayStr = self.__dominoStr(displayStr, hidden) + displayFooter +'\n'
        print(displayStr)
def playGame(table, rowCol):
    """input: the table of dominoes and the rows and columns of it
    output: a boolean that will determine if we continue the game 
    plays the game in testing, taking dominoes from left to right, then row by row
    """
    #create a variable for the stackNums
    stackNums = [0,1,2]    
    #print the table
    print(table)
    #select the domino starting at the left most domino 
    selectedDomino = table.select(rowCol[0],rowCol[1])
    #if we cannot add the selected domino onto stack 0, 1, or 2, the game will not continue and print a statement saying we lost 
    if not table.playDomino(selectedDomino, stackNums[0]):
        if not table.playDomino(selectedDomino, stackNums[1]):
            if not table.playDomino(selectedDomino, stackNums[2]):
                print('Game over! Unable to play a domino on any stack.')
                return False
    #update the column to the next domino in the row 
    updateSelectedDomino(rowCol, table)
    return True
def updateSelectedDomino(rowCol, table):
    """input; the row and column of the dominoes, the table of dominoes
    output: None
    updates the rows and columns so we can go to the next domino 
    """
    #go to the next domino 
    rowCol[1] += 1
    #if the column index is matching the actual length of the columns
    if rowCol[1] == table.getNumColumns():
        #go the the next row and reset the column to 0 
        rowCol[0] += 1
        rowCol[1] = 0 
def main():
    #assign a variable for the table class, creaate a title and a header, print both 
    table = Table()
    title = 'Welcome to DOMINOES 175'
    titleHeader = '=' *len(title)
    print(titleHeader)
    print(title)
    print(titleHeader)
    #ask for an input, if it doesn't match up with the numbers keep asking
    userInput = input('Please select your play mode:\n1. Test mode\n2. Game mode\n> ')
    while userInput != '1' and userInput != '2':
        userInput = input('Invalid selecction. You must enter 1 or 2.\nPlease select your play mode:\n1. Test mode\n2. Game mode\n> ')

    if userInput == '1':
        #if the input is 1, deal the grid using a file and create a variable for a displayed table 
        table.dealGrid(True)
        tableStr = str(table)
        #double checking to see if the actual dominoes were displayed or not, area 127:128 is where the first domino is displayed 
        if tableStr[127:128] != 'N':
            #set a variable so the game can keep going until we lose/win, reveal the grid and have lists for the stacks and rows and columns 
            continueGame = True
            table.revealGrid()
            rowCol = [0, 0]
            #while we haven't lost...
            while continueGame:
                #call the playGame function
                continueGame = playGame(table, rowCol)               
                
                #if we've won...
                if table.isWinner():
                    #stop the game, print the last selected domino and print a statement saying we've won 
                    continueGame = False
                    print(table)
                    print("Congrats! You've won!" )
                                            
    else:
        #if the selection is 2, print this statement 
        print("Currently in construction. Come back later!")
    #finally, tell the user the program is closing 
    print('Closing program...Goodbye')

main()

