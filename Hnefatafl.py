# Environment
from os import access
from typing import AsyncContextManager
from Player import Player
from constant import *
from State import State

class Hnefatafl:

    def __init__(self, state:State = None):
        if not state:
            self.state = self.getStartingPosition()
        else:
            self.state = state
        self.currentPiece = ()
        self.possibleMoves = []

    def getStartingPosition(self):
        board = [['.','.','.','a','a','a','a','a','.','.','.'],
                 ['.','.','.','.','.','a','.','.','.','.','.'],
                 ['.','.','.','.','.','.','.','.','.','.','.'],
                 ['a','.','.','.','.','d','.','.','.','.','a'],
                 ['a','.','.','.','d','d','d','.','.','.','a'],
                 ['a','a','.','d','d','k','d','d','.','a','a'],
                 ['a','.','.','.','d','d','d','.','.','.','a'],
                 ['a','.','.','.','.','d','.','.','.','.','a'],
                 ['.','.','.','.','.','.','.','.','.','.','.'],
                 ['.','.','.','.','.','a','.','.','.','.','.'],
                 ['.','.','.','a','a','a','a','a','.','.','.']]

        return State(board.copy())
   

    def getActions (self, isAttackerTurn : bool, state: State):
        actions = set([])
        piecesTurn = []
        if isAttackerTurn:
            piecesTurn = ['a']
        else:
            piecesTurn = ['d', 'k']


        for row in range(len(state.board)):
            for col in range(len(state.board[0])):
                if state.board[row][col] in piecesTurn:
                    for action in self.get_piece_actions((row, col), state):
                        actions.add(((row, col), action))
        return actions


    def get_piece_actions(self, piecePos : tuple, state : State):
        isKing = state.board[piecePos[0]][piecePos[1]] == 'k'
        isKinginCenter = state.board[CENTERSQ[0]][CENTERSQ[1]] == 'k'
        actions = set([])
        for i in range(piecePos[0] + 1, 11):
            if state.board[i][piecePos[1]] == '.' and (not (i, piecePos[1]) in SPECIALSQS or isKing):
                actions.add((i, piecePos[1]))
            elif (i, piecePos[1]) == CENTERSQ and not isKinginCenter:
                continue
            else:
                break
        for i in range(piecePos[0] - 1, -1, -1):
            if state.board[i][piecePos[1]] == '.' and (not (i, piecePos[1]) in SPECIALSQS or isKing):
                actions.add((i, piecePos[1]))
            elif (i, piecePos[1]) == CENTERSQ and not isKinginCenter:
                continue
            else:
                break
        for i in range(piecePos[1] + 1, 11):
            if state.board[piecePos[0]][i] == '.' and (not (piecePos[0], i) in SPECIALSQS or isKing):
                actions.add((piecePos[0], i))
            elif (piecePos[0], i) == CENTERSQ and not isKinginCenter:
                continue
            else:
                break
        for i in range(piecePos[1] - 1, -1, -1):
            if state.board[piecePos[0]][i] == '.' and (not (piecePos[0], i) in SPECIALSQS or isKing):
                actions.add((piecePos[0], i))
            elif (piecePos[0], i) == CENTERSQ and not isKinginCenter:
                continue
            else:
                break
        return actions
    
    def isPieceTurn(self, row_col, attackerTurn):
        row, col = row_col
        if attackerTurn and self.state.board[row][col] == 'a':
            return True
        elif not attackerTurn and (self.state.board[row][col] == 'd' or self.state.board[row][col] == 'k'):
            return True
        else:
            return False
    
    def isAPiece(self, row_col):
        if not self.state.board[row_col[0]][row_col[1]] == '.':
            return True
        return False

    def handleMouseClick(self, row_col, attackerTurn):
        moved = False
        if self.isAPiece(row_col) and self.isPieceTurn(row_col, attackerTurn):
            self.possibleMoves = self.get_piece_actions(row_col, self.state)
            self.currentPiece = row_col
        elif row_col in self.possibleMoves:
            self.state = self.move(self.currentPiece, row_col, self.state)
            self.possibleMoves = []
            moved = True
        return self.possibleMoves.copy(), moved

    def move(self, pieceRowcol, destRowcol, state : State):
        newState = state.copy()
        newState.board[destRowcol[0]][destRowcol[1]] = newState.board[pieceRowcol[0]][pieceRowcol[1]]
        newState.board[pieceRowcol[0]][pieceRowcol[1]] = '.'

        self.checkIfCapture(newState, destRowcol)

        return newState
    
    def getOppositePiece(self, piece):
        if piece == 'a':
            return 'd', 'k'
        else:
            return ('a')

    def isSquareDeadly(self, piece, square, state : State):
        board = state.board
        pieceOnSquare = board[square[0]][square[1]]
        deadlySpecialSqs = SPECIALSQS.copy()

        if board[CENTERSQ[0]][CENTERSQ[1]] == 'k':
            deadlySpecialSqs -= {CENTERSQ}


        if (piece != 'k' and square in deadlySpecialSqs) or (piece == 'd' and pieceOnSquare == 'a') or (piece == 'a' and (pieceOnSquare == 'd' or pieceOnSquare == 'k')):
            return True
        else:
            return False

    def areThereSurroundingPieces(self, state: State, square : tuple, pieces : tuple):
        row, col = square
        board = state.board

        if (row > 0 and board[row - 1][col] in pieces) or (row < 10 and board[row + 1][col] in pieces) or (col > 0 and board[row][col - 1] in pieces) or (col < 10 and board[row][col + 1] in pieces):
            return True
        return False

    def checkForShieldWall(self, state: State, move : tuple):
        row, col = move
        board = state.board
        # simple checks to eliminate cases which are clearly not shield wall:

        if (row > 1 and row < 9 and col > 1 and col < 9) or not self.areThereSurroundingPieces(state, move, self.getOppositePiece(board[row][col])):
            return # The shield wall only works in the edges.


    








    def checkIfCapture(self, state : State, move : tuple): # add sound effects and color effects
        row, col = move
        board = state.board
        thisPiece = board[row][col]
        
        oppositePiece = self.getOppositePiece(thisPiece)[0] # king is not relevant here.

        if row > 1 and board[row - 1][col] == oppositePiece and self.isSquareDeadly(oppositePiece, (row - 2, col), state):
            board[row - 1][col] = '.'
        if row < 9 and board[row + 1][col] == oppositePiece and self.isSquareDeadly(oppositePiece, (row + 2, col), state):
            board[row + 1][col] = '.'
        if col > 1 and board[row][col - 1] == oppositePiece and self.isSquareDeadly(oppositePiece, (row, col - 2), state):
            board[row][col - 1] = '.'
        if col < 9 and board[row][col + 1] == oppositePiece and self.isSquareDeadly(oppositePiece, (row, col + 2), state):
            board[row][col + 1] = '.'



    def getKingRowcol(self, state : State):
        for row in range(len(state.board)):
            for col in range(len(state.board[0])):
                if state.board[row][col] == 'k':
                    return row, col
    def isWon(self, state : State):
        for row_col in SPECIALSQS - {CENTERSQ}:
            row, col = row_col
            if 'k' == state.board[row][col]:
                return Player.DEFENDER
        
        row, col = self.getKingRowcol(state)
        if row != 0 and row != 10 and col != 0 and col != 10:
            board = state.board
            if board[row - 1][col] == 'a' and board[row + 1][col] == 'a' and board[row][col - 1] == 'a' and board[row][col + 1] == 'a':
                return Player.ATTACKER


        return None
