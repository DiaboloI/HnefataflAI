# Environment
from typing import AsyncContextManager
from constant import *
from State import State
from Action import Action

class Hnefatafl:

    def __init__(self, state:State = None):
        if state == None:
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

        return State(board)

    def is_legal_action (self, action: Action, state:State = None):
        pass
        
    def get_actions (self, state: State = None):
        pass

    def get_piece_actions(self, piecePos : tuple):
        state = self.state
        self.currentPiece = piecePos
        actions = []
        for i in range(piecePos[0] + 1, 11):
            if state.board[i][piecePos[1]] == '.' and not (i, piecePos[1]) in SPECIALSQS:
                actions.append((i, piecePos[1]))
            else:
                break
        for i in range(piecePos[0] - 1, -1, -1):
            if state.board[i][piecePos[1]] == '.' and not (i, piecePos[1]) in SPECIALSQS:
                actions.append((i, piecePos[1]))
            else:
                break
        for i in range(piecePos[1] + 1, 11):
            if state.board[piecePos[0]][i] == '.' and not (piecePos[0], i) in SPECIALSQS:
                actions.append((piecePos[0], i))
            else:
                break
        for i in range(piecePos[1] - 1, -1, -1):
            if state.board[piecePos[0]][i] == '.' and not (piecePos[0], i) in SPECIALSQS:
                actions.append((piecePos[0], i))
            else:
                break
        return actions

    def getRowcol(self, pos : tuple):
        print(pos)
        x, y = pos
        row = ((y - BORDER) / SQUARE_SIZE) // 1
        col = ((x - BORDER) / SQUARE_SIZE) // 1
        print ((row, col))
        return int(row), int(col)
    
    def isAPiece(self, row_col):
        if not self.state.board[row_col[1]][row_col[0]] == '.':
            return True
        return False

    def handleMouseUp(self, pos):
        row_col = self.getRowcol(pos)
        if self.isAPiece(row_col):
            self.possibleMoves = self.get_piece_actions(row_col)
        elif row_col in self.possibleMoves:
            self.move(self.currentPiece, row_col)
            self.possibleMoves = []


        return self.possibleMoves.copy()


    def move (self, pieceRowcol, destRowcol):
        self.state.board[destRowcol[0]][destRowcol[1]] = self.state.board[pieceRowcol[0]][pieceRowcol[1]]
        self.state.board[pieceRowcol[0]][pieceRowcol[1]] = '.'


