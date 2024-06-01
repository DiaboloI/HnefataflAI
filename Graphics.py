import pygame
import numpy as np
from Player import Player
from Constant import *
import State
import time


pygame.init()

class Graphics: #TODO: fix row_col to col_row so it will be x_y as is traditional instead of y_x.
    def __init__(self, win):
        # self.board = state.board
        # self.rows, self.cols = self.board.shape
        self.win = win 
        self.moveCount = 1
        self.onGame = False
        self.loadImages()
    
    def loadImages(self):
        self.img_attacker = self.loadImage('imgs/attacker.png', ((SQUARE_SIZE - (MARGIN * 2)) // 1.2, (SQUARE_SIZE - (MARGIN * 2)) // 1.2)) 
        self.img_defender = self.loadImage('imgs/defender.png', ((SQUARE_SIZE - (MARGIN * 2)) // 1.2, (SQUARE_SIZE - (MARGIN * 2)) // 1.2))
        self.img_king = self.loadImage('imgs/king.png', ((SQUARE_SIZE - (MARGIN * 2)), (SQUARE_SIZE - (MARGIN * 2))))

        self.img_square = self.loadImage('imgs/square.png', (SQUARE_SIZE - (MARGIN * 2), SQUARE_SIZE - (MARGIN * 2)))
        self.img_square_king = self.loadImage('imgs/square_king.png', (SQUARE_SIZE - MARGIN * 2, SQUARE_SIZE - MARGIN * 2))

        self.img_sit_attacker = self.loadImage('imgs/sit_attacker.png', ((SQUARE_SIZE - MARGIN * 2) // 1.8, (SQUARE_SIZE - MARGIN * 2) // 1.8))
        self.img_sit_defender = self.loadImage('imgs/sit_defender.png', ((SQUARE_SIZE - MARGIN * 2) // 1.8, (SQUARE_SIZE - MARGIN * 2) // 1.8))
        self.img_sit_king = self.loadImage('imgs/sit_king.png', ((SQUARE_SIZE - MARGIN * 2) // 1.3, (SQUARE_SIZE - MARGIN * 2) // 1.3))

        self.img_table_attacker = self.loadImage('imgs/table_attacker.png', (SQUARE_SIZE - self.img_sit_attacker.get_size()[0] + MARGIN * 2, SQUARE_SIZE * 2 - (self.img_sit_attacker.get_size()[0]) + MARGIN * 2))
        self.img_table_defender = self.loadImage('imgs/table_defender.png', (SQUARE_SIZE - self.img_sit_defender.get_size()[0] + MARGIN * 2, SQUARE_SIZE * 2 - (self.img_sit_defender.get_size()[0]) + MARGIN * 2))


        self.img_corner_down_right = self.loadImage('imgs/corner_down_right.png', (SQUARE_SIZE - MARGIN * 2, SQUARE_SIZE - MARGIN * 2))
        
        self.img_border = self.loadImage('imgs/border.png', (SQUARE_SIZE // 2, SQUARE_SIZE * 5.5))
        self.img_border_corner = self.loadImage('imgs/corner_border_left_up.png', (BORDER, BORDER))

    def loadImage(self, path, size : tuple):
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, size)
        return img

    def drawAllSquares(self):
        # draw all the squares. corner and center squares appear uniquely. starting squares also appear differently.
        for row in range(11):
            for col in range(11):
                row_col = (row, col)
                if row_col == CENTERSQ:
                    self.win.blit(self.img_square_king, np.add(self.calc_base_pos(row_col), (MARGIN, MARGIN)))
                else:
                    self.win.blit(self.img_square, np.add(self.calc_base_pos(row_col), (MARGIN, MARGIN)))


                if row_col in SPECIALSQS and not row_col == CENTERSQ:
                    img = self.img_corner_down_right
                    match row_col:
                        case (0, 10):
                            img = pygame.transform.rotate(img, 90)
                        case (0, 0):
                            img = pygame.transform.rotate(img, 180)
                        case (10, 0):
                            img = pygame.transform.rotate(img, 270)

                    self.win.blit(img, np.add(self.calc_base_pos(row_col), (MARGIN, MARGIN)))


                pygame.draw.rect(self.win, BLACK, (*self.calc_base_pos(row_col), SQUARE_SIZE, SQUARE_SIZE), MARGIN) # margin of squares 


    def drawTablesandSits(self):
        for row_col in ATTACKERSQS:
            possit = self.calc_piece_pos(row_col, self.img_sit_attacker.get_size())
            self.win.blit(self.img_sit_attacker, possit) # draw attacker sit
        for row_col in DEFENDERSQS:
            possit = self.calc_piece_pos(row_col, self.img_sit_defender.get_size())
            self.win.blit(self.img_sit_defender, possit) # draw defender sit
        
        self.win.blit(self.img_sit_king, self.calc_piece_pos(CENTERSQ, self.img_sit_king.get_size()))

        count = 0
        img = self.img_table_attacker
        for row_col in ATTACKERTABLESLCS:
            if count == 4:
                img = pygame.transform.rotate(img, 90)
            pos = self.calc_base_pos(row_col)
            self.win.blit(img, pos)

            count += 1
        
        count = 0
        img = self.img_table_defender
        for row_col in DEFENDERTABLESLCS:
            if count == 2:
                img = pygame.transform.rotate(img, 90)
            pos = self.calc_base_pos(row_col)
            self.win.blit(img, pos)

            count += 1
        
      
    def draw_all_pieces(self, state:State): # and sits
        board = state.board
        for row in range(len(board)): # row : String
            for col in range(len(board[0])):
                if board[row][col] != 0:
                    self.draw_piece(state, (row, col))
            
    def draw_piece(self, state:State, row_col): # and sit
        row, col = row_col
        board = state.board
        piece = board[row][col]
        img : pygame.surface.Surface
        match piece:
            case 2:
                img = self.img_defender
            case 1:
                img = self.img_attacker
            case 3:
                img = self.img_king
        pos = self.calc_piece_pos(row_col, img.get_size())
        self.win.blit(img, pos) # draw piece
    
    def drawTurnCaption(self, attackerTurn):
        row_col = (12, 5)
        if (not self.onGame):
            self.moveCount += 1
        if attackerTurn:
            self.drawCaption("Attacker's Turn! " + str(self.moveCount), row_col)
        else:
            self.drawCaption("Defender's Turn! " + str(self.moveCount), row_col)

    def drawCaption(self, caption, row_col): 
        font = pygame.font.SysFont('ariel', (SQUARE_SIZE - (MARGIN*2)))
        text = font.render(caption, 1, BLACK)
        textPos = self.calc_num_pos(row_col, font, caption)
        self.win.blit(text, textPos)

    def drawWinningMessage(self, winner):
        winn = ""
        if winner == Player.ATTACKER:
            winn = "Attacker"
        else:
            winn = "Defender"

        self.moveCount = 1

        font = pygame.font.SysFont('ariel', HEIGHT // 7)
        text = font.render(winn + " won!", 1, RED)
        textPos = (WIDTH // 10, HEIGHT // 2.5)
        pygame.draw.rect(self.win, WHITE, (*textPos, WIDTH // 1.3, HEIGHT // 10))
        self.win.blit(text, textPos)


    def drawBorder(self): # and tables
        self.win.blit(self.img_border, (0, SQUARE_SIZE // 2))
        self.win.blit(self.img_border, (0, SQUARE_SIZE // 2 + SQUARE_SIZE * 5.5))
        # TODO: Copy this border to every line
        pygame.draw.line(self.win, BLACK, (0, BORDER), (0, SQUARE_SIZE * 11), MARGIN) # margin of border
        pygame.draw.line(self.win, BLACK, (BORDER - 1, BORDER), (BORDER - 1, SQUARE_SIZE * 11), MARGIN) # margin of border
        self.win.blit(self.img_border, (BORDER + SQUARE_SIZE * 11, BORDER))
        self.win.blit(self.img_border, (BORDER + SQUARE_SIZE * 11, BORDER + SQUARE_SIZE * 5.5))
        img_rotated = pygame.transform.rotate(self.img_border, 90)
        self.win.blit(img_rotated, (SQUARE_SIZE // 2, 0))
        self.win.blit(img_rotated, (SQUARE_SIZE // 2 + SQUARE_SIZE * 5.5, 0))
        self.win.blit(img_rotated, (SQUARE_SIZE // 2, SQUARE_SIZE * 11 + SQUARE_SIZE // 2))
        self.win.blit(img_rotated, (SQUARE_SIZE // 2 + SQUARE_SIZE * 5.5, SQUARE_SIZE * 11 + SQUARE_SIZE // 2))

        border_corner = self.img_border_corner
        for row_col in SPECIALSQS:
            if row_col == CENTERSQ:
                continue
            match row_col:
                case (0, 10):
                    border_corner = pygame.transform.rotate(self.img_border_corner, 90)
                case (10, 0):
                    border_corner = pygame.transform.rotate(self.img_border_corner, 270)
                case (10, 10):
                    border_corner = pygame.transform.rotate(self.img_border_corner, 180)
                case (0, 0):
                    border_corner = self.img_border_corner


            row_col = np.divide(row_col, (10, 10))
            self.win.blit(border_corner, (row_col[0] * (SQUARE_SIZE * 11 + BORDER), row_col[1] * (SQUARE_SIZE * 11 + BORDER)))

            # attacker tables:


    def drawPossibleMoves(self, possibleMoves : list[tuple]):
        for row_col in possibleMoves:
            pygame.draw.circle(self.win, PICKED_COLOR, self.calc_pos(row_col), POSSIBLE_MOVES_RADIUS)

    def calc_pos(self, row_col):
        row, col = row_col
        y = row * SQUARE_SIZE + SQUARE_SIZE//2 + BORDER
        x = col * SQUARE_SIZE + SQUARE_SIZE//2 + BORDER
        return x, y
    
    def calcRowcol(self, pos : tuple):
        x, y = pos
        row = ((y - BORDER) / SQUARE_SIZE) // 1
        col = ((x - BORDER) / SQUARE_SIZE) // 1
        return int(row), int(col)

    def calc_base_pos(self, row_col):
        row, col = row_col
        y = row * SQUARE_SIZE + BORDER
        x = col * SQUARE_SIZE + BORDER
        return x, y

    def calc_piece_pos(self, row_col, size : tuple[int, int]):
        return tuple(np.add(np.add(self.calc_base_pos(row_col), np.divide(np.subtract((SQUARE_SIZE - MARGIN, SQUARE_SIZE - MARGIN), size), 2)), (MARGIN, MARGIN)))

    def calc_num_pos(self, row_col, font, char):
        row, col = row_col
        font_width, font_height = font.size(char)
        y = row * SQUARE_SIZE + (SQUARE_SIZE - font_height)//2
        x = col * SQUARE_SIZE + BORDER + (SQUARE_SIZE - font_width)//2
        return x, y
    
    def determineSquareColor(self, row_col):
        color : Tuple
        if row_col == CENTERSQ:
            color = CENTER_SQUARE_COLOR
        elif row_col in SPECIALSQS:
            color = SPECIAL_SQUARE_COLOR
        elif row_col in ATTACKERSQS:
            color = ATTACKER_SQUARE_COLOR
        elif row_col in DEFENDERSQS:
            color = DEFENDER_SQUARE_COLOR
        else:
            color = SQUARE_COLOR
        return color

    def draw(self, state, possibleMoves, attackerTurn):
        self.win.fill(LIGHTGRAY)
        self.drawAllSquares(state)
        self.drawBorder()
        self.drawTablesandSits()
        self.draw_all_pieces(state)
        self.drawPossibleMoves(possibleMoves)
        self.drawTurnCaption(attackerTurn)

    def draw_square(self, row_col, color):
        pos = self.calc_base_pos(row_col)
        pygame.draw.rect(self.win, color, (*pos, SQUARE_SIZE - MARGIN, SQUARE_SIZE - MARGIN))
        pygame.draw.rect(self.win, BLACK, (*pos, SQUARE_SIZE, SQUARE_SIZE), MARGIN) # margin of squares
    """def blink(self, row_col, color):
        row, col = row_col
        player = self.board[row][col]
        for i in range (3):
            self.draw_square((row, col), color)
            pygame.display.update()
            time.sleep(0.2)
            self.draw_piece((row, col))
            pygame.display.update()
            time.sleep(0.2)"""

