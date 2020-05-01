
from AI import *
import math

#constant
INFINITY = +math.inf

class MancalaBoard:
    def __init__(self):
        """ Initilize a game board for the game of mancala"""
        self.reset()#function

    def reset(self):
        """ Reselt the mancala board for a new game"""
        self.NHOLES = 6  # holes per side
        self.scoreHoles = [0, 0]
        self.P1Holes = [4] * self.NHOLES #4 stone in each hole [4] [4] [4] [4] [4] [4]
        self.P2Holes = [4] * self.NHOLES

    def legalMove(self, player, hole): #player=self.turn = p1/p2   hole is the next hole to be moved
        """ Returns whether is legal move or not"""
        if player.num == 1:#from AI.py self.num = playerNum/ / 1=human // 2=AI
            holes = self.P1Holes #row of hole for player 1

        else:
            holes = self.P2Holes #row of hole for player 1

        return hole > 0 and hole <= len(holes) and holes[hole - 1] > 0 #within the row of holes and current hole is not empty

    def legalMoves(self, player):
        """ Returns a list of legal moves  """
        if player.num == 1:
            holes = self.P1Holes

        else:
            holes = self.P2Holes

        moves = []#list the move

        for m in range(len(holes)):
            if holes[m] != 0: #current hole not empty
                moves += [m + 1]  #store move 1 2 3 4 5 6

        return moves

    def makeMove(self, player, hole):#player and next hole
        again = self.makeMoveHelp(player, hole)#call fucntion for next move
        if self.gameOver():#return true/false
            # clear out the holes
            for i in range(len(self.P1Holes)):
                self.scoreHoles[0] += self.P1Holes[i]  #add the stone to the house
                self.P1Holes[i] = 0 #the row of holes cleared
            for i in range(len(self.P2Holes)):
                self.scoreHoles[1] += self.P2Holes[i]
                self.P2Holes[i] = 0
            return False #cannot make move coz game over
        else:
            return again#next move

    def makeMoveHelp(self, player, hole):#hole is the next hole to move
        """ Make a move for the given player.
            Returns True if the player gets another turn and False if not.
            Assumes a legal move"""
        if player.num == 1: #player 1 move
            holes = self.P1Holes
            oppHoles = self.P2Holes
        else:
            holes = self.P2Holes
            oppHoles = self.P1Holes
        initHoles = holes #own row
        nstones = holes[hole - 1]  # Pick up the stones at current hole
        holes[hole - 1] = 0  # Now the hole is empty
        hole += 1 #current hole is the next hole
        playAgain = False
        while nstones > 0:
            playAgain = False
            while hole <= len(holes) and nstones > 0: #while next hole is valid and current stone > 0
                holes[hole - 1] += 1 #current hole +1 can drop stone in current hole
                nstones = nstones - 1
                hole += 1 #to next hole
            if nstones == 0: # if no more stones, exit the loop
                break
            if holes == initHoles:  # If currently at own side
                self.scoreHoles[player.num - 1] += 1 #add one stone to current player house
                #self.scoreHoles = [0, 0]//  player1=scoreHoles[0] , player2=scoreHoles[1]
                nstones = nstones - 1
                playAgain = True #go into house can continue move
            # now switch sides and keep going
            tempHoles = holes
            holes = oppHoles
            oppHoles = tempHoles
            hole = 1 #switch side,hole start form 1

        # landed in own house,playAgain is true
        # play is over but get to go again
        if playAgain:
            return True

        #  if ended in a blank space at own side
        if holes == initHoles and holes[hole - 2] == 1:#current hole is one last stonne
            self.scoreHoles[player.num - 1] += oppHoles[(self.NHOLES - hole) + 1]#can take all the stone in opponent hole to house
            oppHoles[(self.NHOLES - hole) + 1] = 0 #opponent hole become empty
            self.scoreHoles[player.num - 1] += 1 # take own one last stone into house
            holes[hole - 2] = 0 #current hole is empty
        return False #move end

    def hasWon(self, playerNum): #if playerNum=1=human
        """ Returns whether or not the player has won """
        if self.gameOver(): #if current player game over
            opp = 2 - playerNum + 1 #oppoenet = minus self plus opponent
            return self.scoreHoles[playerNum - 1] > self.scoreHoles[opp - 1] #compare number of stone in house scoreHoles=[0,0]initially 2 element with index 0,1
        else:
            return False

    def getPlayersHoles(self, playerNum):
        """ Return the row of holes for  player """
        if playerNum == 1: #human
            return self.P1Holes
        else:#AI
            return self.P2Holes

    def gameOver(self):
        """ Is the game over?"""
        over = True
        for elem in self.P1Holes: #4 stone in each hole for player 1
            if elem != 0: #if still have stone in hole
                over = False #game not over
        if over: # over still true
            return True #game really over for P1
        over = True #reset over
        for elem in self.P2Holes: #4 stone in each hole for player 1
            if elem != 0:#if still have stone in hole
                over = False#game not over
        return over #game really over for P2

