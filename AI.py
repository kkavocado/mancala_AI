

from decimal import *
from copy import *
#for copy operations
# because Assignment statements do not copy objects, they create bindings between a target and an object
# creates a new variable that shares the reference of the original object
from MancalaBoard import *
import math

# constant
INFINITY =+math.inf
start = 0.0
end = 0.0

class Player:
    """ A basic AI or human player """
    HUMAN = 1
    ABPRUNE = 2



    def __init__(self, playerNum, playerType, ply=0):#ply default=0 depth of search
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1 #opponent number /current player human 2-1+1=2 opponent is AI
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)#return player number


    def alphaBetaMove(self, board, ply): #board = self.game in ChooseMove = MancalaBoard() ply=depth
        """ Choose a move with alpha beta pruning.  Returns (score, move)
        score,move from alphaMaxValue()"""
        alpha = -INFINITY
        beta = INFINITY

        return self.alphaMaxValue(board, ply, self, alpha, beta) #return final move for alpha beta


    def alphaMaxValue(self, board, ply, turn, alpha, beta): #turn = self in alphaBetaMove s
        """ Find the alphamax value for the next move for this player
        at a given board configuration. Returns score, move."""

        if board.gameOver() or ply == 0 or abs(board.scoreHoles[0] - board.scoreHoles[1]) > 24: #game over or ply==0 done search or over half of stone in house
            return turn.score(board), -1 #score(self, board) function returns score, move

        score = -INFINITY #like alpha
        move = -1

        for m in board.legalMoves(self):  #board.legalMoves list of legal move

            # make a new player to play the other side -- simulate opponent
            opponent = Player(self.opp, self.type, self.ply)#current is AI opp is human

            # Copy the board and not to ruin it
            nextBoard = deepcopy(board) #board=MancalaBoard()
            #constructs a new compound object and then, recursively, inserts copies into it of the objects found in the original. copies everything

            again = nextBoard.makeMove(self, m) #def makeMove(self, player, hole): #player and next hole  m-still in legal move
            #Make the next move

            if again: #legal move for AI
                s, mv = self.alphaMaxValue(nextBoard, ply - 1, turn, alpha, beta) #returns score, move #recursive call to evaluate nextBoard with next depth (ply-1)
            else:
                s, mv = opponent.alphaMinValue(nextBoard, ply-1, turn, alpha, beta)#opponent use min  return this is like beta

            #If this state is greater then store that in score
            if s > score: #s return from recurive call initial score=-INFINITY  get bigger alpha value
                # score return from alpha function bigger than the previous value return from the function
                score = s #s return from alpha Msx or Min get better score so can take this move
                move = m #current move inside list of legal move

            #If score is greater than or equal to beta return score
            if score >= beta: #previous value ald good bigger than beta
                return score, move #alpha>=beta

           #if score is greater than alpha, make alpha score
            if score > alpha: #alpha take maximum value and getting larger
                alpha = score #alpha want bigger value and updata alpha

        return score, move #final score-the largest value

    def alphaMinValue(self, board, ply, turn, alpha, beta): #turn = self in alphaBetaMove s
        """ Find the alphamin value for the next move for this player
            at a given board configuration. Returns score,move."""

        if board.gameOver() or ply == 0 or abs(board.scoreHoles[0] - board.scoreHoles[1]) > 24:
            return turn.score(board), -1 #returns score, move
        score = INFINITY #like beta
        move = -1

        for m in board.legalMoves(self):
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)#current is AI opp is human
            # Copy the board not to ruin it
            nextBoard = deepcopy(board)
            again = nextBoard.makeMove(self, m)

            if again:
                s, mv = self.alphaMinValue(nextBoard, ply - 1, turn, alpha, beta) #returns score, move #recursive call to evaluate nextBoard with next depth (ply-1)
            else:
                #Make the next move
                s, mv = opponent.alphaMaxValue(nextBoard, ply-1, turn, alpha, beta)#opponent use min  return this is like alpha

            #If this state is less then store that in score
            if s < score: #get smaller beta value
                score = s
                move = m

            #If score is less than or equal to alpha return score
            if score <= alpha:
                #smaller than alpha then return - prune
                return score, move

            #if score is less than beta, make beta score
            if score < beta:
                #beta getting smaller
                beta = score #update beta
        # f = open('alphaMinValue.txt', 'a+')
        # f.write('\nscore \t')
        # f.write('%f' % score)
        # f.close()
        return score, move


    def chooseMove(self, board): #move = self.turn.chooseMove( self.game )  self.game = MancalaBoard()
        """ Returns the next move that this player wants to make """

        if self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)#alphaBetaMove return final score and move after alpha beta pruning
            print ("chose move", move, " with value", val)
            return move

class AI(Player):
    """ Defines AI player that evaluates Mancala gameboard"""


    def score(self, board):
        #board=MancalaBoard()
        """ Evaluate the Mancala board for this player """

        if board.hasWon(self.num):
            #evaluate the current player won
            return 500.0

        elif board.hasWon(self.opp):
            #opponent will win
            return -500.0

        elif board.scoreHoles[self.num - 1] > 24:
            #own house >24 may win
            return 250

        elif board.scoreHoles[self.opp - 1] > 24:
            #opponent house >24 may lose
            return -250

        else:
            #Get the holes first
            if (self.num == 1):
                #human player
                holes = board.P1Holes  #row of hole for player 1
                oppHoles = board.P2Holes #row of hole for player 2
                scoreDiff = board.scoreHoles[0] - board.scoreHoles[1]

            else:
                #opponent
                holes = board.P2Holes  #row of hole for player 2
                oppHoles = board.P1Holes  #row of hole for player 1
                scoreDiff = board.scoreHoles[1] - board.scoreHoles[0]


            # Check if the score is better
            score =(scoreDiff + 30) * 10 / 6

            # initialize value
            additional = 0.0
            capturing = 0.0
            stones = 0.0

            for i in range(len(holes)):

                numStones = holes[i]#number of stone in hole i  #[4] * self.NHOLES #4 stone in each hole [4] [4] [4] [4] [4] [4]

                if numStones > 0 or oppHoles[i] > 0:
                    if numStones == (6 - i):
                        #go into house can have additional turn
                        #example marble=6,at first hole with index=0,with 6 stones can get into house and evaluate it with additional score
                        # example marble=5,at second hole with index=1,with 5 stones can get into house and evaluate it with additional score
                        additional = (50.0 * (i + 1))/6 #give 50*current hole of points for the current hole  average for 6 holes
                        #additional=50

                    #Capturing
                    temp = oppHoles[i] % 13
                    #number of stone at opponent hole[i]  eg oppHoles[0]=4  maximum temp=12
                    #12 holes in total can go one round and back to same hole  oppHoles=P1Holes/P2holes
                    temp_capturing = 0.0
                    ownStones = -1

                    if temp <= (5 - i):
                        #Stones will land on holes[i+temp] means not get into house have 5 stones in the first hole cant get to house  5-i=5 4 3 2 1 0
                        #eg current i=0,oppHoles[0]at the rightest hole at top row,stone=4
                        #can move 4 hole and land at holes[0+4],which is hole with index 4,calculate index from the right to left at top row

                        if temp == 0:
                            #land back on same hole
                            #if it land back on the same hole,that hole is empty so can take away the stone in opposite hole
                            #the stone in own side hole is taken by opponent
                            ownStones = holes[5 - i] #eg i=0, opponent move at oppHoles[0] go back to that hole so take away stones in holes[5]

                        else:
                            #eg i=0 ownstones=holes[5-0-4]=holes[1] which is the hole at own row,and is the hole which the opponent landed
                            ownStones = holes[5 - i - temp]

                    elif temp >= (13 - i):
                        #13-i = 13 12 11 10 9 8 #reach the hole beside the current hole
                        ownStones = holes[5 - i + temp - 13] #opponent take the stone in the hole at the opposite is the hole at own side
                    #eg i=4,13-i=9 ,temp=10 holes[5-4+10-13]=holes[-2] negative means print from the back

                    #Calculate capturing
                    if ownStones == 0:
                        #opponent take no stone
                        temp_capturing = 50.0 # own score get higher

                    elif ownStones == 1:
                        temp_capturing = 40.0

                    elif ownStones == 2:
                        temp_capturing = 25

                    if temp_capturing > capturing:
                        #current capture bigger than previous capture in loop
                        capturing = temp_capturing #update current capturing score


                    #stones
                    if numStones < 4:
                        stones += 5
                else:
                    #if no stones in own side and opposite side at particular column of hole
                    if i == 5:
                        #easy to get into house
                        stones += 30 #higher score
                    else:
                        #other hole
                        stones += 10 #give lower score

            total = capturing + score + additional + stones
            #print ("total=", total, "capturing=", capturing, "score=", score, "additional=", additional, "stones=", stones)

            return total



