from numpy import mask_indices
import pygame
import math
from Player import Player
from State import State
from Constant import *
from Graphics import *
from Hnefatafl import Hnefatafl

class Ai_Agent:
    def __init__(self, player : Player):
        self.player = player
        self.hnefatafl = Hnefatafl()
    
    def nextToKing(self, state):
        kingRowcol = self.hnefatafl.getKingRowcol(state)
        surrounding = self.hnefatafl.getSurroundingSquares(kingRowcol)

        count = 0
        for square in surrounding:
            if state.board[square[0]][square[1]] == 1:
                count += 1
        return count

    def countAttackersWhoBlockCorners(self, state):
        count = 0
        BLOCKSSQUARES = set([(0, 2), (1, 1), (2, 0), (0, 8), (1, 9), (2, 10), (8, 0), (9, 1), (10, 2), (10, 8), (9, 9), (8, 10)])

        for square in BLOCKSSQUARES:
            pType = state.board[square[0]][square[1]] 
            if pType == 1:
                count += 1
            elif pType == 2:
                count -= 1
            elif pType == 3:
                count -= 4

        return count

    def calculateKingManhattanDistance(self, state):
        corners = SPECIALSQS - {CENTERSQ}
        minDistance = 1000
        
        kingRowcol = self.hnefatafl.getKingRowcol(state)

        for corner in corners:
            distance = abs(corner[1] - kingRowcol[1]) + abs(corner[0] - kingRowcol[0])
            minDistance = min(minDistance, distance)

        return minDistance

    
    def pieceCountDifference(self, state):
        count = 0

        for row in state.board:
            for square in row:
                if square == 1:
                    count += 1
                elif square == 2 or square == 3:
                    count -= 1

        return count

    def eval(self, state : State):
        won = self.hnefatafl.is_end_of_game(state) # king on squares next to corner also wins
        if won:
            if won == Player.ATTACKER:
                return math.inf
            else:
                return -math.inf
        kingRowcol = self.hnefatafl.getKingRowcol(state)

        for corner in (SPECIALSQS - {CENTERSQ}):
            if kingRowcol in self.hnefatafl.getSurroundingSquares(corner):
                return -100000
        edgeScore = 0
        if self.hnefatafl.inEdges(kingRowcol, 1):
            edgeScore = 20

        score = 3 * self.nextToKing(state) + 3 * self.pieceCountDifference(state) + self.calculateKingManhattanDistance(state) + 3 * self.countAttackersWhoBlockCorners(state)  - edgeScore

        return score

    def alphaBetaPruning(self, state, maximizingPlayer : bool, gotAction, depth, alpha, beta):
        srt = 0

        if depth == DEPTH or self.hnefatafl.is_end_of_game(state):
            value = self.eval(state)
            return value, gotAction

        if maximizingPlayer: # attacker.
            bestValue = -math.inf
            bestAction = gotAction
            for action in self.hnefatafl.getActions(True, state):
                newState = self.hnefatafl.get_next_state(action, state)
                newValue, newAction = self.alphaBetaPruning(newState, False, action, depth + 1, alpha, beta)

                if (bestAction == None):
                    bestAction = newAction

                if newValue > bestValue:
                    bestValue = newValue
                    bestAction = action

                if bestValue > alpha:
                    alpha = bestValue


                if beta <= alpha:
                    break

            return bestValue, bestAction

        else: # minimizing player, defender.
            bestValue = math.inf
            bestAction = gotAction
            for action in self.hnefatafl.getActions(False, state):
                newState = self.hnefatafl.get_next_state(action, state)
                newValue, newAction = self.alphaBetaPruning(newState, True, action, depth + 1, alpha, beta)

                if (bestAction == None):
                    bestAction = newAction

                if newValue < bestValue:
                    bestValue = newValue
                    bestAction = action
                    srt = newState

                if bestValue < beta:
                    beta = bestValue

                if beta <= alpha:
                    break

            return bestValue, bestAction




    def get_Action(self, event = None, graphics = None, state : State = None, attackerTurn : bool = None, train = False):
        f = self.alphaBetaPruning(state, self.player == Player.ATTACKER, None, 0, -math.inf, math.inf)[1]

        #print(f)
        return f

