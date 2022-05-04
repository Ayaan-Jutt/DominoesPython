#******************************************************
# Assignment 2 Task 1: Create Dominoes
# Author: Ayaan Jutt
# Collaborators/References: Stack and CircularQueue taken from CMPUT 175 labs
#******************************************************

from queues import CircularQueue
import random
from stack import Stack
class Domino():
    def __init__(self, dotsA, dotsB):
        """input: a bottom and a top set of dots for a domino
        output: None
        sets up a domino with a set of dots, and whether or not they're faced down 
        """
        #initialize the variables, bottom of the domino will be dotsA, top will be dotsB, and the domino is face up
        assert type(dotsA) == int and type(dotsB) == int, 'Domino dots need to be an int'
        if dotsA > dotsB:
            self.__bottom= dotsB
            self.__top = dotsA
        else:
            self.__top = dotsB
            self.__bottom = dotsA
        self.__faceDown = False
    def setTop(self, dots):
        """input: a set of dots that matches with a previous domino
        output: None
        matches a domino with the domino beneath it
        """
        #try adding a domino
        try:
            #if the top is equal to the dots, set the bottom of the dots to equal 
            #the dots, the top to be the bottom of the domino,
            #in other words, flip the domino
            if self.__top == dots:
                self.__top = self.__bottom
                self.__bottom = dots
            elif self.__bottom == dots:
                self.__bottom = dots
        #if none match, raise an assertion error and print it 
            else:
                raise AssertionError('Cannot add domino')
        except AssertionError as inst:
            print(inst)
        
        
    def turnOver(self):
        """
        input: N/A
        output: None
        turns the domino face up or down
        """
        #if the domino is face up, set it down, else face it up
        if not self.__faceDown:
            self.__faceDown = True
        else:
            self.__faceDown = False
    def getTop(self):
        """
        input: N/A
        output: None
        returns the top of the domino
        """
        #return the top of the domino
        return self.__top
    def getBottom(self):
        """
        input: N/A
        output: self.__getBottom
        returns the bottom of the domino
        """
        #return the bottom of the domino
        return self.__bottom
    def isFaceDown(self):
        """Input: N/A
        output: self.__faceDown
        Returns whether or not the domino is faced down
        """
        #return whether or not they are face down
        return self.__faceDown
    def __str__(self):
        """
        input: N/A
        output: A string version of the domino
        creates a string version of the Domino class
        """
        #create an empty string
        dominoStr = ''
        #if the domino is face down, the dominoStr is set up as question marks and return it
        if self.isFaceDown():
            dominoStr = '[?|?]'
            return dominoStr
        #else, get the bottom of the domino and the top into the string and return it
        else:
            dominoStr = '[' + str(self.getBottom()) + '|' + str(self.getTop()) + ']'
            return dominoStr
class DominoDeck():
    def __init__(self):
        """input: N/A
        output: None
        initializes the deck that will be used to hold multiple dominoes
        """
        #initialize the circularQueue class and assign it with 28 dominoes
        maxAmountOfDominoes = 28
        self.__dominoDeck = CircularQueue(maxAmountOfDominoes)

    def __createFile(self):
        """input: N/A
        output: A file and the lines in it
        a private metod that asks for a file, reads it, puts it into a list, and returns the file and list
        """
        #keep asking the user for a file until the text ends with .txt
        testFile = ''
        while not testFile.endswith('.txt'):
            #try this...
            try:
                #ask the user for a file
                testFile = input('Name of file that should be used to populate the grid of dominoes: ')
                #open up the testFile, reading it, and turning it into a list
                file = open(testFile)
                content = file.read()
                lines = content.splitlines()  
            #if the file doesn't exist print the statement saying that with the file we cannot read from 
            except FileNotFoundError:
                print('Cannot read from '+testFile)
                #the testFile should be an empty string, so the while loop can still go until we can read a file 
                testFile = ''
            else:
                return file,lines, testFile
    def populate(self, useFile):
        """input: a boolean
        output: None
        This file will add every domino into the deck as long as there are 28 of them in a file,
        if there is no file, 28 dominoes are added in and shuffled 
        """
        #check if the useFile is a bool, else raise an error
        assert type(useFile) == bool, "Cannot populate deck, invalid argument provided" 
        #if we are using a file...
        if useFile:
            file, lines, testFile = self.__createFile()
            #try this...
            try:
                #if the length of the list does not match the capacity of the dominoDeck, raise an error 
                if len(lines) != self.__dominoDeck.capacity():
                    raise ValueError("Cannot populate deck: invalid data in "+ testFile)
                #go through each line, take the numbers from the file and add it into a Domino class, then enqueue the Domino into the deck 
                for numbers in lines:
                    bottom, top= numbers.split('/')
                    
                    if type(int(bottom)) and type(int(top)) != int:
                        raise ValueError("Cannot populate deck: invalid data in "+ testFile)
                    domino = Domino(int(top), int(bottom))
                    self.__dominoDeck.enqueue(domino)
            #if either the length of the file doesn't match or a domino top or bottom can turn into an int...
            except ValueError as error:
                #say a statement saying so and clear the deck
                print(error)
                self.__dominoDeck.clear()
            #finally close the file 
            finally:
                file.close()
        else:
            #if we aren't populating the deck using a file...
            #create two variables, one for the top of the dominoes and one for the bottom of the dominoes 
            bottom = 0
            top = 0
            dominoList = []
            #while the top and bottom is less than 7
            while top < 7:
                while bottom < 7:
                    #add the top and bottom into a Domino class and enqueue it into the deck
                    domino = Domino(top, bottom)
                    dominoList.append(domino)
                    bottom += 1
                #after that while loop is done, add one to the top, and match the bottom to the top
                #i.e top = 1, bottom = 1
                top+=1
                bottom = top 
            random.shuffle(dominoList)
            #after populating the deck, shuffle it 
            for domino in dominoList:
                self.__dominoDeck.enqueue(domino)
                            
    def deal(self):
        """input: N/A
        output: a turned over domino
        turns over a domino and returns it to the user 
        """
        #takes the first domino of the dequeue, turns it over
        dominoDealt = self.__dominoDeck.dequeue()
        dominoDealt.turnOver()
        #return the dominoDealt
        return dominoDealt
    def isEmpty(self):
        """input: N/A
        output: a boolean
        Returns whether or not the deck is empty 
        """
        #return if the deck is empty
        return self.__dominoDeck.isEmpty()
    def size(self):
        """input: N/A
        output: an int based off the size of the deck
        returns the size of the domino Deck
        """
        #return the size
        return self.__dominoDeck.size()
    def __str__(self):
        """input: N/A
        output: a string version of the deck
        creates a string version of the deck, with a labeled head of the domino
        """
        #call the string function of the Queue class
        string = str(self.__dominoDeck)
        #The headOfString is at 1 because string[0] is a bracket. It ends before the 6th character because the that's the length of the domino
        headOfString = ' H = ' + string[1:6]
        return string + headOfString
class DominoStack(Stack): 
    def __init__(self) :
        """input: N/A
        output: None
        Creates the stack for dominoes via inheritance 
        """
        #initialize the stack by calling the stack Class
        Stack.__init__(self)
    def peek(self):
        """input: None
        output: The top dots of the top domino
        Returns the top dots of the domino on top of the stack
        """
        #try this...
        try:
            #if the items is empty
            if self.isEmpty():
                #print an error
                raise Exception('Error: cannot peak into an empty stack') 
            else:
                #else get the last item of the stack, and the top of the dots in the domino 
                return self.items[len(self.items)-1].getTop()
        except Exception as inst:
            print(inst)
    def isEmpty(self):
        """input: N/A
        output: a boolean on whether or not the stack is empty
        returns a true or false on whether or not the stack is empty
        """
        #checks if the items are empty
        return self.items == []
    def size(self):
        """input: N/A
        output: the size of the stack
        returns the length of the stack
        """
        #return the length of self.items
        return len(self.items)
    def push(self, domino):
        """input: a domino from the Domino class
        output: None
        adds a domino from the Domino class onto the stack
        """
        #check if what's being added is a domino, else raise an error
        assert type(domino) == Domino, "Can only push Dominoes onto the DominoStack"
        #if the stack is emepty, just append the domino 
        if self.isEmpty():
            self.items.append(domino)
        else:
            #if it's not empty, try this...
            try:
                #if the top of the domino and the bottom of the Domino do not match the top of the last domino
                if domino.getTop() != self.peek() and domino.getBottom() != self.peek():
                    #raise an exception, this exception only stops the try from continuing 
                    raise Exception('Cannot play '+str(domino) +' on stack')
                #if it doesn't, then set the top of the new domino with the argument of the top of the last domino
                domino.setTop(self.peek())
                #add the domino 
                self.items.append(domino)
            except Exception as inst:
                print(inst)
                
    def __str__(self):
        """input: None
        output: A string version of the DominoStack
        Returns the dominoes in a stack as a string
        """
        #create an empty string, and iterate through the items 
        stackString = ''
        for item in self.items:
            #add the string version of the item item to the string with a dash 
            stackString = stackString + str(item) + ' - '
        #return the string 
        return stackString

