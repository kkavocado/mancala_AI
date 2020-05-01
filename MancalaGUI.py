
from tkinter import * #gui
from MancalaBoard import *
import AI

class MancalaWindow:
    """ GUI for playing Mancala"""

    def __init__(self, master, p1, p2):
        self.HOLEW = 100 #width of hole
        self.HEIGHT = 250 #height of hole
        self.BOARDW = 500 #width of board
        self.PAD = 2 #padding between each hole
        self.game = MancalaBoard() #call Mancala Board class

        self.p1 = p1 #player 1
        self.p2 = p2 #player 2

        self.BINW = self.BOARDW / self.game.NHOLES #get the width of the board to fill the hole NHOLES=6

        self.turn = p1 #current player is player 1
        self.wait = p2 #player 2 has to wait
        self.root = master #root = Tk() open window

        frame = Frame(master,bg='light goldenrod yellow') #open frame
        frame.pack() #pack frame

        # Create the board
        self.makeBoard( frame ) #makeBoard function takes frame as argument

        displayStr = "Let's play Mancala!" #string

        # w = Label(master, option, ...)
        # master-parent window
        # option-list of commonly used option--text
        # self.frame is parent window
        self.status = Label(frame, text=displayStr,bg='light goldenrod yellow',fg='rosybrown4')  #display one or more lines of text that cannot be modified by the user
        self.status.config(font=('Jokerman', 18,'bold'))
        self.status.pack(side=BOTTOM) #show text in status

    def enableBoard(self):
        """ Allow a human player to make moves by clicking"""
        for i in [0, 1]:#only allow 1 click
            for j in range(self.game.NHOLES):
                self.holes[i][j].bind("<Button-1>", self.callback)
                #bind for each hole-can click on each hole
                #use the bind method of the frame widget to bind a callback function to an event called <Button-1>
                #click in the window that appears

    def disableBoard(self):
        """ Prevent the human player from clicking while the computer thinks"""
        for i in [0, 1]:
            for j in range(self.game.NHOLES):
                self.holes[i][j].unbind("<Button-1>")#unbind/disable key once it's clicked

    def makeBoard( self, frame ):
        """ Create the board """
        boardFrame = Frame(frame)#frame = Frame(master,bg='lemon chiffon') #open frame
        boardFrame.pack(side=BOTTOM)

        self.button = Button(frame, text="Start The Game!", command=self.newgame,bg='lightsalmon2',fg='lemon chiffon') #self.newgame is function to start the game-AI first
        self.button.config(font=('Jokerman', 16))
        self.button.pack(side=TOP)

        gamef = Frame(boardFrame) #boardFrame = Frame(frame)
        topRow = Frame(gamef)
        bottomRow = Frame(gamef)
        topRow.pack(side=TOP)
        bottomRow.pack(side=TOP)

        #temporary list
        tmpHoles = []
        tmpHoles2 = []

        binW = self.BOARDW/self.game.NHOLES #width of each bin for the hole
        binH = self.HEIGHT/2 #height of each bin for the hole

        for i in range(self.game.NHOLES): #create canvas for each hole
            c = Canvas(bottomRow, width=binW, height=binH,bg='lightsalmon2')
            c.pack(side=LEFT)
            tmpHoles += [c] #store each hole canvas created for bottom row

            c = Canvas(topRow, width=binW, height=binH,bg='lightsalmon2')
            c.pack(side=LEFT)
            tmpHoles2 += [c]#store each hole canvas created for top row

        self.holes = [tmpHoles, tmpHoles2]#holes two row
        self.p1hole = Canvas(boardFrame, width=self.HOLEW, height=self.HEIGHT,bg='lightsalmon2')
        self.p2hole = Canvas(boardFrame, width=self.HOLEW, height=self.HEIGHT,bg='lightsalmon2')

        self.p2hole.pack(side=LEFT)
        gamef.pack(side=LEFT)
        self.p1hole.pack(side=LEFT)

        self.drawBoard()#function


    def drawBoard( self ):
        """ Draw the board on the canvas """
        #create oval for each hole

        self.p2hole.create_oval(self.PAD, 10*self.PAD, self.HOLEW, 0.9*self.HEIGHT, width=2,fill='lemon chiffon',outline='brown')#player 2 house

        binW = self.BOARDW/self.game.NHOLES
        binH = self.HEIGHT/2#height for hole

        for j in range(self.game.NHOLES):  # column # create oval for holes
            self.holes[0][j].create_oval(self.PAD, self.PAD, binW, binH, fill='lemon chiffon',outline='brown',activefill='peach puff') #bottom row
            self.holes[1][j].create_oval(self.PAD, self.PAD, binW, binH, fill='lemon chiffon', outline='brown') #top row

        self.p1hole.create_oval(self.PAD, 10*self.PAD, self.HOLEW, 0.9*self.HEIGHT, width=2,fill='lemon chiffon',outline='brown' )#player 1 house


    def newgame(self):
        """ Start a new game between the players """
        self.game.reset() #MancalaBoard.py def reset(self):
        self.turn = self.p1
        self.wait = self.p2

        s = "Player " + str(self.turn) + "'s turn"

        if self.turn.type != Player.HUMAN:
            s += " Please wait..."

        self.status['text'] = s #status-string of text-s store to status

        #replace Let's play Mancala
        self.resetStones()#function
        self.continueGame()#function

    # Board must be disabled to call continueGame
    def continueGame( self ):
        """ Continue the game to next step. Announce the winner or continue to next move: human to click or AI to choose move"""
        self.root.update() #root = Tk()

        #updates the dictionary with the elements from the another dictionary object or from an iterable of key/value pairs.
        #updates the key with the new value

        if self.game.gameOver():#function in MancalaBoard.py def gameOver(self):
            if self.game.hasWon(self.p1.num):#def hasWon(self, playerNum): #check P1 has won
                self.status['text'] = "Player " + str(self.p1) + " wins"
            elif self.game.hasWon(self.p2.num): #check P2 has won
                self.status['text'] = "Player " + str(self.p2) + " wins"
            else:
                self.status['text'] = "Tie game"
            return

        if self.turn.type == Player.HUMAN: #Player class in AI.py
            self.enableBoard() #human turn,enable click
        else: #AI turn
            move = self.turn.chooseMove( self.game )#class in AI.py self.game = MancalaBoard()
            playAgain = self.game.makeMove( self.turn, move ) #def makeMove(self, player, hole) in MancalaBoard.py
            if not playAgain:
                self.swapTurns()
            self.resetStones()#function
            self.continueGame()#function to continue to next step-game over or continue

    def swapTurns( self ):
        """ Change turn/wait"""
        temp = self.turn

        self.turn = self.wait
        self.wait = temp

        statusstr = "Player " + str(self.turn) + "\'s turn "

        if self.turn.type != Player.HUMAN: #not human turn display wait
            statusstr += "Please wait..."

        self.status['text'] = statusstr


    def resetStones(self):
        """ Clear the stones and redraw them """
        # Put the stones in the holes

        for i in range(len(self.game.P2Holes)):#self.P2Holes = [4] * self.NHOLES total 24 stone for 1 player
            index = (len(self.game.P2Holes)-i)-1#traverse the hole and minus each stone
            self.clearHole(self.holes[1][index])#clear hole function
            # display number of stones in each hole at top row
            self.holes[1][index].create_text(self.BINW/2, 0.25*self.HEIGHT, text=str(self.game.P2Holes[i]), tag="num",font='Jokerman')

        for i in range(len(self.game.P1Holes)):
            # display number of stones in each hole at bottom row
            self.clearHole(self.holes[0][i])
            self.holes[0][i].create_text(self.BINW/2, 0.25*self.HEIGHT, text=str(self.game.P1Holes[i]), tag="num",font='Jokerman')

        self.clearHole(self.p1hole)#clear hole for house of p1
        self.clearHole(self.p2hole)#clear hole for house of p1

        #clear hole then redisplay new number of stone

        self.p2hole.create_text(self.HOLEW/2, 0.5*self.HEIGHT, text=str(self.game.scoreHoles[1]), tag="num",font='Jokerman')
        self.p1hole.create_text(self.HOLEW/2, 0.5*self.HEIGHT, text=str(self.game.scoreHoles[0]), tag="num",font='Jokerman')


    def clearHole( self, hole ):
        """ Clear the stones in the given hole"""
        titems = hole.find_withtag("num") #"all canvas items presently having that tag"
        #find tag num in hole
        stones = hole.find_withtag("stone")
        hole.delete(titems)
        hole.delete(stones)


    def callback(self, event):
        """ Handle the human player's move"""
        # calculate which box the click was in
        moveAgain = True
        self.disableBoard()#disable click
        if self.turn.num == 1:
            for i in range(len(self.holes[0])):#length of bottom row of holes
                if self.holes[0][i] == event.widget: #widget generated by this event
                    if self.game.legalMove( self.turn, i+1 ):#allow to move to next hole
                        moveAgain = self.game.makeMove( self.turn, i+1 )#continue moving to i+1

                        if not moveAgain:#cannot move
                            self.swapTurns()#opponent turn
                        self.resetStones()#display latest number of stone
        else:#AI side

            for i in range(len(self.holes[1])):#length of top row of holes
                if self.holes[1][i] == event.widget:
                    index = self.game.NHOLES - i #eg 6=6-1 1 is the first box from left to right and is index 6 for AI

                    if self.game.legalMove( self.turn, index ):#allow to move to next hole
                        moveAgain = self.game.makeMove( self.turn, index )#continue moving

                        if not moveAgain:#cannot move
                            self.swapTurns()#opponent turn

                        self.resetStones()#display latest number of stone

        if moveAgain: #if can move again
            self.enableBoard()#enable click for huamn player

        else:
            self.continueGame()


def startGame(p1, p2):
    """ Start the game of Mancala with two players """
    root = Tk()

    root.title("Mancala")
    root.iconbitmap("mancala.ico")

    MancalaWindow(root, p1, p2)

    root.mainloop()

def main():
    playerHuman = AI.AI(1, AI.Player.HUMAN)
    playerAI = AI.AI(2, AI.Player.ABPRUNE,9)
    startGame(playerAI,playerHuman)
    #startGame(playerHuman,playerAI)

if __name__ == '__main__':
    main()

