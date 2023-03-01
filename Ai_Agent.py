from numpy import mask_indices
import pygame
import math
from Player import Player
from State import State
from constant import *
from Graphics import *
from Hnefatafl import Hnefatafl

class Ai_Agent:
    def __init__(self, player : Player):
        self.player = player
        self.hnefatafl = Hnefatafl()

    def calculateKingManhattanDistance(self, state):
        corners = SPECIALSQS - {CENTERSQ}
        minDistance = 1000
        
        kingRowcol = self.hnefatafl.getKingRowcol(state)

        for corner in corners:
            distance = abs(corner[1] - kingRowcol[1]) + abs(corner[0] - kingRowcol[0])
            minDistance = min(minDistance, distance)

        return minDistance

    
    def pieceCountDifference(self, state):
        attacksCount = 0
        defendersCount = 0

        for row in state.board:
            for square in row:
                if square == 'a':
                    attacksCount += 1
                elif square == 'd' or square == 'k':
                    defendersCount += 1

        return attacksCount - defendersCount

    def eval(self, state : State):
        won = self.hnefatafl.isWon(state) # king on squares next to corner also wins
        if won:
            if won == Player.ATTACKER:
                return math.inf
            else:
                return -math.inf

        score = 10 * self.pieceCountDifference(state) + self.calculateKingManhattanDistance(state)

        return score

    def alphaBetaPruning(self, state, visited, maximizingPlayer : bool, gotAction, depth, alpha, beta):
        if depth == DEPTH or self.hnefatafl.isWon(state):
            value = self.eval(state)
            return value, gotAction

        if maximizingPlayer: # attacker.
            bestValue = -math.inf
            bestAction = gotAction
            for action in self.hnefatafl.getActions(True, state):
                newState = self.hnefatafl.move(action[0], action[1], state)
                if newState in visited:
                    continue
                visited.append(newState)
                newValue, newAction = self.alphaBetaPruning(newState, visited, False, action, depth + 1, alpha, beta)

                if newValue > bestValue:
                    bestValue = newValue
                    bestAction = action

                if bestValue > alpha:
                    alpha = bestValue


                if alpha <= beta:
                    break

            return bestValue, bestAction

        else: # minimizing player, defender.
            bestValue = math.inf
            bestAction = gotAction
            for action in self.hnefatafl.getActions(False, state):
                newState = self.hnefatafl.move(action[0], action[1], state)
                if newState in visited:
                    continue
                visited.append(newState)
                newValue, newAction = self.alphaBetaPruning(newState, visited, True, action, depth + 1, alpha, beta)
                if newValue < bestValue:
                    bestValue = newValue
                    bestAction = action

                if bestValue < beta:
                    beta = bestValue

                if alpha >= beta:
                    break

            return bestValue, bestAction




    def getAction(self, event, graphics, state : State, attackerTurn : bool):
        return self.alphaBetaPruning(state, [], attackerTurn, None, 0, -math.inf, math.inf)[1]

