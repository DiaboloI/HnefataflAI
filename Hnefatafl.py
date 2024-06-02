# Environment
from os import access
from typing import AsyncContextManager
from Player import Player
from Constant import *
from State import State
import numpy as np

class Hnefatafl:

    def __init__(self, state:State = None):
        if not state:
            self.state = self.get_init_state()
        else:
            self.state = state


        self.sWcaptures = 0
        self.sBcaptures = 0

# . = 0, a = 1, d = 2, k = 3
    def get_init_state(self):
        board = np.array([[0,0,0,1,1,1,1,1,0,0,0],
                          [0,0,0,0,0,1,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0],
                          [1,0,0,0,0,2,0,0,0,0,1],
                          [1,0,0,0,2,2,2,0,0,0,1],
                          [1,1,0,2,2,3,2,2,0,1,1],
                          [1,0,0,0,2,2,2,0,0,0,1],
                          [1,0,0,0,0,2,0,0,0,0,1],
                          [0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,1,0,0,0,0,0],
                          [0,0,0,1,1,1,1,1,0,0,0]])

        state = State(board, player=1, legal_actions=[])
        state.legal_actions = self.getActions(True, state)
        #print(state.moveCount)
        return state
   

    def getActions (self, isAttackerTurn : bool, state: State):
        actions = set([])
        piecesTurn = []
        if isAttackerTurn:
            piecesTurn = [1]
        else:
            piecesTurn = [2, 3]


        for row in range(len(state.board)):
            for col in range(len(state.board[0])):
                if state.board[row][col] in piecesTurn:
                    for action in self.get_piece_actions((row, col), state):
                        actions.add(((row, col) + action))

        if (len(actions) == 0):
            with open("program.log", "a") as myfile:
                myfile.write(str(state.board) + "\n\n" + str(isAttackerTurn) + "\n\n\n")



        return actions


    def get_piece_actions(self, piecePos : tuple, state : State):
        isKing = state.board[piecePos[0]][piecePos[1]] == 3
        isKinginCenter = state.board[CENTERSQ[0]][CENTERSQ[1]] == 3
        actions = set([])
        for i in range(piecePos[0] + 1, 11):
            if state.board[i][piecePos[1]] == 0 and (not (i, piecePos[1]) in SPECIALSQS or isKing):
                actions.add((i, piecePos[1]))
            elif (i, piecePos[1]) == CENTERSQ and not isKinginCenter:
                continue
            else:
                break
        for i in range(piecePos[0] - 1, -1, -1):
            if state.board[i][piecePos[1]] == 0 and (not (i, piecePos[1]) in SPECIALSQS or isKing):
                actions.add((i, piecePos[1]))
            elif (i, piecePos[1]) == CENTERSQ and not isKinginCenter:
                continue
            else:
                break
        for i in range(piecePos[1] + 1, 11):
            if state.board[piecePos[0]][i] == 0 and (not (piecePos[0], i) in SPECIALSQS or isKing):
                actions.add((piecePos[0], i))
            elif (piecePos[0], i) == CENTERSQ and not isKinginCenter:
                continue
            else:
                break
        for i in range(piecePos[1] - 1, -1, -1):
            if state.board[piecePos[0]][i] == 0 and (not (piecePos[0], i) in SPECIALSQS or isKing):
                actions.add((piecePos[0], i))
            elif (piecePos[0], i) == CENTERSQ and not isKinginCenter:
                continue
            else:
                break
        return actions
    
    def isPieceTurn(self, row_col, attackerTurn):
        row, col = row_col
        if attackerTurn and self.state.board[row][col] == 1:
            return True
        elif not attackerTurn and (self.state.board[row][col] == 2 or self.state.board[row][col] == 3):
            return True
        else:
            return False
    
    def isAPiece(self, row_col):
        if not self.state.board[row_col[0]][row_col[1]] == 0:
            return True
        return False
    
    def isOutofRange(self, row_col):
        row, col = row_col

        if row < 0 or row > 10 or col < 0 or col > 10:
            return True
        return False

    def handleMouseClick(self, row_col, attackerTurn):
        moved = False
        if not self.isOutofRange(row_col):
            if self.isAPiece(row_col) and self.isPieceTurn(row_col, attackerTurn):
                self.state.possibleMoves = self.get_piece_actions(row_col, self.state)
                self.state.currentPiece = row_col
            elif row_col in self.state.possibleMoves:
                self.state = self.get_next_state((self.state.currentPiece + row_col), self.state)
                self.state.possibleMoves = []
                moved = True
        return self.state.possibleMoves.copy(), moved

    def captured(self, state : State, square):
        state.board[square[0]][square[1]] = 0

    def unpackAction(self, action):
        return (action[0], action[1]), (action[2], action[3])

    def get_next_state(self, action, state : State):
        pieceRowcol, destRowcol = self.unpackAction(action)

        newState = state.copy()
        newState.board[destRowcol[0]][destRowcol[1]] = newState.board[pieceRowcol[0]][pieceRowcol[1]]
        newState.board[pieceRowcol[0]][pieceRowcol[1]] = 0

        if (state.board[destRowcol[0], destRowcol[1]] == 3):
            newState.kingPos = destRowcol
        
        self.checkIfCapture(newState, destRowcol)
        state.isDraw = self.repetition(state, pieceRowcol, destRowcol)

        newState.moveCount += 1
        newState.switch_player()
        newState.legal_actions = self.getActions(newState.player == 1, newState)

        return newState
    
    def move(self, action, state):
        self.state = self.get_next_state(action, self.state)

    def get_all_next_states (self, state: State) -> tuple:
        legal_actions = state.legal_actions
        next_states = []
        for action in legal_actions:
            next_states.append(self.get_next_state(action, state))
        return next_states, legal_actions
    
    def getOppositePiece(self, piece):
        if piece == 1:
            return (2, 3)
        else:
            return tuple([1])

    def isSquareDeadly(self, piece, square, state : State):
        board = state.board
        pieceOnSquare = board[square[0]][square[1]]
        deadlySpecialSqs = SPECIALSQS.copy()

        if board[CENTERSQ[0]][CENTERSQ[1]] == 3:
            deadlySpecialSqs -= {CENTERSQ}


        if (piece != 3 and square in deadlySpecialSqs) or (piece == 2 and pieceOnSquare == 1) or (piece == 1 and (pieceOnSquare == 2 or pieceOnSquare == 3)):
            return True
        else:
            return False

    def getSurroundingSquares(self, square : tuple):
        row, col = square

        surSquares = []

        if row > 0:
            surSquares.append(tuple((row - 1, col)))

        if row < 10:
            surSquares.append(tuple((row + 1, col)))

        if col > 0:
            surSquares.append(tuple((row, col - 1)))

        if col < 10:
            surSquares.append(tuple((row, col + 1)))
        
        return surSquares

    def getSurroundingPieces(self, state: State, square : tuple, pieces : tuple):
        board = state.board

        surPieces = []

        for surSq in self.getSurroundingSquares(square):
            if board[surSq[0]][surSq[1]] in pieces:
                surPieces.append(surSq)
        
        return surPieces

    def inEdges(self, square : tuple, edge : int):
        row, col = square

        if (row < edge or row > (10 - edge) or col < edge or col > (10 - edge)):
            return True
        return False

    def checkForShieldWall(self, state: State, move : tuple):
        row, col = move
        board = state.board
        # simple checks to eliminate cases which are clearly not shield wall:

        surPieces = self.getSurroundingPieces(state, move, self.getOppositePiece(board[row][col]))

        if (row > 1 and row < 9 and col > 1 and col < 9) or not surPieces:
            #print ((row > 1 and row < 9 and col > 1 and col < 9))
            #print (surPieces)
            return # The shield wall only works in the edges.

        #print ("sur: " + str(surPieces))

        for piece in surPieces:
            shield = True
            shieldCaptured = []
            if self.inEdges(piece, 1):
                #print ("In, " + str(piece) + " type: " + str(board[piece[0]][piece[1]]))
                queue = [piece]
                visited = []
                while queue:
                    if not shield:
                        break
                    curPiece = queue.pop()
                    #print("cur: " + str(curPiece))
                    if not curPiece in visited:
                        visited.append(curPiece)
                        shieldCaptured.append(curPiece)
                        for surPiece in self.getSurroundingSquares(curPiece):
                            pieceType = board[surPiece[0]][surPiece[1]]
                            if pieceType == 0 and not surPiece in SPECIALSQS:
                                shield = False
                                break
                            elif pieceType in self.getOppositePiece(piece): # No idea why it works? this needs investigating.
                                queue.insert(0, surPiece)
                                #print("surPiece: " + str(surPiece) + " type: " + str(pieceType))
            #print (shield)
            #print (shieldCaptured)
            if shield:
                for capt in shieldCaptured:
                    if not board[capt[0]][capt[1]] == 3:
                        self.captured(state, capt)



        


    def repetition(self, state: State, moveSrc : tuple, moveDst : tuple):
        isDraw = False
        
        state.currentPattern.append((moveSrc, moveDst))

        if len(state.currentPattern) == 4:
            if state.currentPattern == state.repetitionPattern:
                state.repetitionCount += 1
                if state.repetitionCount == MAXREPETITION:
                    isDraw = True
            else:
                state.repetitionCount = 0
                state.repetitionPattern = state.currentPattern.copy()


            state.currentPattern = []
        
        
        return isDraw

            
            
    

    def checkIfCapture(self, state : State, move : tuple): # add sound effects and color effects
        row, col = move
        board = state.board
        thisPiece = board[row][col]
        
        oppositePiece = self.getOppositePiece(thisPiece)[0] # king is not relevant here.
        trr = 0
        if row > 1 and board[row - 1][col] == oppositePiece and self.isSquareDeadly(oppositePiece, (row - 2, col), state):
            board[row - 1][col] = 0
            trr += 1
        if row < 9 and board[row + 1][col] == oppositePiece and self.isSquareDeadly(oppositePiece, (row + 2, col), state):
            board[row + 1][col] = 0
            trr += 1
        if col > 1 and board[row][col - 1] == oppositePiece and self.isSquareDeadly(oppositePiece, (row, col - 2), state):
            board[row][col - 1] = 0
            trr += 1
        if col < 9 and board[row][col + 1] == oppositePiece and self.isSquareDeadly(oppositePiece, (row, col + 2), state):
            board[row][col + 1] = 0
            trr += 1

        if (oppositePiece == 1):
            state.blackCaptures += trr
            state.extraTreat -= trr
        else:
            state.whiteCaptures += trr
            state.extraTreat += trr
        #self.checkForShieldWall(state, move)



    def getKingRowcol(self, state : State):
        return state.kingPos

    def pieceCount(self, state, player):
        count = 0

        for row in state.board:
            for square in row:
                if square == player:
                    count += 1

        return count

    def is_end_of_game(self, state : State):
        if state.isDraw:
            return "draw"
        
        if state.moveCount > 100:
            #return "draw"
            if state.whiteCaptures < state.blackCaptures:
                return Player.DEFENDER
            elif state.whiteCaptures > state.blackCaptures:
                return Player.ATTACKER
            else:
                return "draw"

        for row_col in SPECIALSQS - {CENTERSQ}:
            row, col = row_col
            if state.board[row][col] == 3:
                state.extraTreat -= 100
                self.sBcaptures += 1
                return Player.DEFENDER
        
        row, col = self.getKingRowcol(state)
        if row != 0 and row != 10 and col != 0 and col != 10:
            board = state.board
            if board[row - 1][col] == 1 and board[row + 1][col] == 1 and board[row][col - 1] == 1 and board[row][col + 1] == 1:
                state.extraTreat += 100
                self.sWcaptures += 1
                return Player.ATTACKER


        if self.pieceCount(state, 1) == 0:
            state.extraTreat -= 50
            return Player.DEFENDER
        if self.pieceCount(state, 2) == 0:
            surround = self.getSurroundingSquares(self.getKingRowcol(state))
            for sq in surround:
                if state.board[sq[0]][sq[1]] == 0:
                    return None

            state.extraTreat += 50
            return Player.ATTACKER


        if (state.player == -1):
            if (len(state.legal_actions) == 0):
                state.extraTreat += 50
                return Player.ATTACKER

        if (state.player == 1):
            if (len(state.legal_actions) == 0):
                state.extraTreat -= 50
                return Player.DEFENDER

        return None

    def reward (self, state : State) -> tuple:
        next_state = state
        # if action:
        #     next_state = self.get_next_state(action, state)
        # else:
        #     next_state = state

        end = self.is_end_of_game(next_state)

        if (end):
            extra = state.extraTreat
            state.extraTreat = 0
            if end == Player.ATTACKER:
                return 30 + extra, True
            elif end == Player.DEFENDER:
                return -30 + extra, True
            elif end == "draw":
                return extra, True

        return state.extraTreat, False
