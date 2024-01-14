import pygame

DEPTH = 2
HEIGHT, WIDTH  = 900, 840
SQUARE_SIZE = WIDTH // 12
POSSIBLE_MOVES_RADIUS = SQUARE_SIZE // 8
MARGIN = SQUARE_SIZE // 40
BORDER = SQUARE_SIZE // 2
SPECIALSQS = set([(5, 5), (0, 0), (0, 10), (10, 10), (10, 0)])
CENTERSQ = (5, 5)
ATTACKERSQS = set([(0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 5), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (9, 5), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (5, 1), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (5, 9)])
DEFENDERSQS = set([(3, 5), (4, 4), (4, 5), (4, 6), (5, 3), (5, 4), (5, 6), (5, 7), (6, 4), (6, 5), (6, 6), (7, 5)])
ATTACKERTABLESLCS = [(3.75, 0.75), (5.75, 0.75), (3.75, 9.78), (5.75, 9.78), (0.75, 3.75), (0.75, 5.75), (9.78, 3.75), (9.78, 5.75)]
DEFENDERTABLESLCS = [(4.75, 3.78), (4.75, 6.78), (3.78, 4.75), (6.78, 4.75)]

MAXREPETITION = 3

# Colors
MARGIN_COLOR = (128, 102, 69)
DEFENDER_COLOR = (255, 255, 255) # White
ATTACKER_COLOR = (0, 0, 0) # Black
PICKED_COLOR = (150, 26, 30) # Picked square. Red.
SQUARE_COLOR = (224,213,202) # Square. Gray.
MOVES_COLOR = (230,242,219) # Possible moves circles color. Green.
ATTACKER_SQUARE_COLOR = (168,152,67) # 
DEFENDER_SQUARE_COLOR = (255,230,102) # Gold.
CENTER_SQUARE_COLOR = (153,170,255) # Blue.
SPECIAL_SQUARE_COLOR = (212,38,255) # Purple.

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHTGRAY = (211,211,211)
GREEN = (0, 128, 0)


# epsilon Greedy
epsilon_start = 1
epsilon_final = 0.01
epsiln_decay = 25000