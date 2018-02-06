#!/usr/bin/env python3
# Modified from Tetromino by lusob luis@sobrecueva.com
# http://lusob.com
# Released under a "Simplified BSD" license

# import random, time, pygame, sys
# from pygame.locals import *
import numpy as np
# from pynput import keyboard
import matplotlib as mpl
import matplotlib.pyplot as plt
from collections import namedtuple

def draw_on_grid(grid, x, y, width, border, maincolor, outlinecolor):
    for i in range(width):
        for j in range(width):
            if i < border-1 or j < border-1 or (width - i) < border or (width - j) < border:
                grid[i+y*width,j+x*width] = outlinecolor
            else:
                grid[i+y*width,j+x*width] = maincolor




mpl.rcParams.update({'image.cmap': 'Accent',
                     'image.interpolation': 'none',
                    #  'xtick.major.width': 0,
                    #  'xtick.labelsize': 0,
                    #  'ytick.major.width': 0,
                    #  'ytick.labelsize': 0,
                     'axes.linewidth': 0})

#
# BOARDWIDTH = 10
# BOARDHEIGHT = 20
#
#
#
# FPS = 25
# BOXSIZE = 20
# WINDOWWIDTH = BOXSIZE * BOARDWIDTH
# WINDOWHEIGHT = BOXSIZE * BOARDHEIGHT
# BLANK = '.'
#
# MOVESIDEWAYSFREQ = 0.15
# MOVEDOWNFREQ = 0.1
#
# XMARGIN = 0
# TOPMARGIN = 0
#
# #               R    G    B
# WHITE       = (255, 255, 255)
# GRAY        = (185, 185, 185)
# BLACK       = (  0,   0,   0)
# RED         = (155,   0,   0)
# LIGHTRED    = (175,  20,  20)
# GREEN       = (  0, 155,   0)
# LIGHTGREEN  = ( 20, 175,  20)
# BLUE        = (  0,   0, 155)
# LIGHTBLUE   = ( 20,  20, 175)
# YELLOW      = (155, 155,   0)
# LIGHTYELLOW = (175, 175,  20)
#
# BORDERCOLOR = BLUE
# BGCOLOR = BLACK
# TEXTCOLOR = WHITE
# TEXTSHADOWCOLOR = GRAY
# COLORS      = (     BLUE,      GREEN,      RED,      YELLOW)
# LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)
# assert len(COLORS) == len(LIGHTCOLORS) # each color must have light color
#
# TEMPLATEWIDTH = 5
# TEMPLATEHEIGHT = 5
# A piece is a list of points in a cartesian space with its origin at the point of rotation


#
# rotations = {
#     'Identity
# }
#
# periods = [1,2,4,4,4,4,4]
#
#
# S_SHAPE_TEMPLATE = [['..OO.',
#                      '.OO..',
#                      '.....',
#                      '.....',
#                      '.....'],
#                     ['..O..',
#                      '..OO.',
#                      '...O.',
#                      '.....',
#                      '.....']]
#
# Z_SHAPE_TEMPLATE = [['.OO..',
#                      '..OO.',
#                      '.....',
#                      '.....',
#                      '.....'],
#                     ['..O..',
#                      '.OO..',
#                      '.O...',
#                      '.....',
#                      '.....']]
#
# I_SHAPE_TEMPLATE = [['..O..',
#                      '..O..',
#                      '..O..',
#                      '..O..',
#                      '.....'],
#                     ['OOOO.',
#                      '.....',
#                      '.....',
#                      '.....',
#                      '.....']]
#
# O_SHAPE_TEMPLATE = [['.OO..',
#                      '.OO..',
#                      '.....',
#                      '.....',
#                      '.....']]
#
# J_SHAPE_TEMPLATE = [['.O...',
#                      '.OOO.',
#                      '.....',
#                      '.....',
#                      '.....'],
#                     ['..OO.',
#                      '..O..',
#                      '..O..',
#                      '.....',
#                      '.....'],
#                     ['.OOO.',
#                      '...O.',
#                      '.....',
#                      '.....',
#                      '.....'],
#                     ['..O..',
#                      '..O..',
#                      '.OO..',
#                      '.....',
#                      '.....']]
#
# L_SHAPE_TEMPLATE = [['...O.',
#                      '.OOO.',
#                      '.....',
#                      '.....',
#                      '.....'],
#                     ['..O..',
#                      '..O..',
#                      '..OO.',
#                      '.....',
#                      '.....'],
#                     ['.OOO.',
#                      '.O...',
#                      '.....',
#                      '.....',
#                      '.....'],
#                     ['.OO..',
#                      '..O..',
#                      '..O..',
#                      '.....',
#                      '.....']]
#
# T_SHAPE_TEMPLATE = [['..O..',
#                      '.OOO.',
#                      '.....',
#                      '.....',
#                      '.....'],
#                     ['..O..',
#                      '..OO.',
#                      '..O..',
#                      '.....',
#                      '.....'],
#                     ['.OOO.',
#                      '..O..',
#                      '.....',
#                      '.....',
#                      '.....'],
#                     ['..O..',
#                      '.OO..',
#                      '..O..',
#                      '.....',
#                      '.....']]
#
# PIECES = {'S': S_SHAPE_TEMPLATE,
#           'Z': Z_SHAPE_TEMPLATE,
#           'J': J_SHAPE_TEMPLATE,
#           'L': L_SHAPE_TEMPLATE,
#           'I': I_SHAPE_TEMPLATE,
#           'O': O_SHAPE_TEMPLATE,
#           'T': T_SHAPE_TEMPLATE}

moveLeft = np.matrix([ # <- (-y)
            [1,0,0],
            [0,1,-1],
            [0,0,1]])
moveRight = np.matrix([ # -> (+y)
            [1,0,0],
            [0,1,1],
            [0,0,1]])
moveDown = np.matrix([ # | (+x)
            [1,0,0],   # V
            [0,1,1],
            [0,0,1]])
CCWRotation = np.matrix([ # CCW rotation
            [0,-1,0],
            [1,0,0],
            [0,0,1]])
CWRotation = np.matrix([ # CW rotation
            [0,1,0],
            [-1,0,0],
            [0,0,1]])
NoMove = np.eye(3) # 3x3 identity matrix

TetrisPiece = namedtuple('TetrisPiece', 'name points moves')
pieces = {
    'O': TetrisPiece('O',
        np.array([[0,0,1],[1,0,1],[1,-1,1],[0,-1,1]]),
        [NoMove]),
    'I': TetrisPiece('O',
        np.array([[0,0,1],[0,1,1],[0,-1,1],[0,-2,1]]),
        [CCWRotation, CWRotation]),
    'S': TetrisPiece('S',
        np.array([[0,0,1],[0,1,1],[1,0,1],[1,-1,1]]),
        [CCWRotation]),
    'Z': TetrisPiece('Z',
        np.array([[0,0,1],[0,-1,1],[1,0,1],[1,1,1]]),
        [CCWRotation]),
    'L': TetrisPiece('L',
        np.array([[0,0,1],[0,-1,1],[0,1,1],[1,-1,1]]),
        [CCWRotation]),
    'J': TetrisPiece('J',
        np.array([[0,0,1],[0,-1,1],[0,1,1],[1,1,1]]),
        [CCWRotation]),
    'T': TetrisPiece('T',
        np.array([[0,0,1],[0,-1,1],[0,1,1],[1,0,1]]),
        [CCWRotation]),
}

class TetrisOutOfBounts(Exception):
    pass

class TetrisPiece(object):
    # 0, I, S, Z, L, J, T
    pieces = [
        # Homogenized co-ordinates to allow compound transforms
        np.array([[0,0,1],[1,0,1],[1,-1,1],[0,-1,1]]),
        np.array([[0,0,1],[0,1,1],[0,-1,1],[0,-2,1]]),
        np.array([[0,0,1],[0,1,1],[1,0,1],[1,-1,1]]),
        np.array([[0,0,1],[0,-1,1],[1,0,1],[1,1,1]]),
        np.array([[0,0,1],[0,-1,1],[0,1,1],[1,-1,1]]),
        np.array([[0,0,1],[0,-1,1],[0,1,1],[1,1,1]]),
        np.array([[0,0,1],[0,-1,1],[0,1,1],[1,0,1]])
    ]
    block_colors = [ # https://en.wikipedia.org/wiki/Tetris#Tetromino_colors : Tetris Company colors
        [1,1,0],
        [0,1,1],
        [0,1,0],
        [1,0,0],
        [1,.6,0],
        [0,0,1],
        [.5,0,.5],
    ]

    identity_rotation = np.eye(3)
    # Rotate pi/2 CCW
    ccw_rotation = np.array([[0,-1,0],
                          [1,0,0],
                          [0,0,1]])
    # Rotate pi/2 CW
    cw_rotation = np.array([[0,1,0],
                          [-1,0,0],
                          [0,0,1]])
    # l_rotation = base_rotation @ base_rotation @ base_rotation

    # We'll iterate over the list of rotations for the active piece, applying each
    # in turn (i % len(rotations[piece]))
    rotations = [
        [identity_rotation],
        [ccw_rotation, cw_rotation],
        [ccw_rotation],
        [ccw_rotation],
        [ccw_rotation],
        [ccw_rotation],
        [ccw_rotation],
    ]
    def __init__(self, piece=None, offsetx=0, offsety=6, rot_iter=0):
        if piece is None:
            piece = np.random.choice(np.arange(len(TetrisPiece.pieces)))
        self.piece = piece
        self.points=TetrisPiece.pieces[piece]
        self.rotations = TetrisPiece.rotations[piece]
        self.rot_iter = 0
        self.offsetx = offsetx
        self.offsety = offsety
        self.color = TetrisPiece.block_colors[piece]

    def calc_rotation(self):
        rot = (self.rot_iter + 1) % len(TetrisPiece.rotations[self.piece])
        return rot, np.vstack([TetrisPiece.rotations[self.piece][rot] @ p for p in self.points])


    def do_rotation(self, direction):
        self.rot_iter, self.points = self.calc_rotation()
        # self.rot_iter = (self.rot_iter + 1) % len(TetrisPiece.rotations[self.piece])

class TetrisBoard(object):
    affineMoves = [
        np.matrix([ # <- (-y)
            [1,0,0],
            [0,1,-1],
            [0,0,1]
        ]),
        np.matrix([ # -> (+y)
            [1,0,0],
            [0,1,1],
            [0,0,1]
        ]),
        np.matrix([ # | (+x)
            [1,0,0],# V
            [0,1,1],
            [0,0,1]
        ]),
        np.matrix([ # CCW rotation
            [0,-1,0],
            [1,0,0],
            [0,0,1]
        ]),
        np.matrix([ # CW rotation
            [0,1,0],
            [-1,0,0],
            [0,0,1]
        ]),
    ]
    moves = [
        (0,0,False),
        (0,-1,False),
        (0,1,False),
        (1,0,False),
        (0,0,True),
    ]
    # key_mapping = {
    #     None: 0,
    #     keyboard.Key.left: 1,
    #     keyboard.Key.right: 2,
    #     keyboard.Key.down: 3,
    #     keyboard.Key.up: 4,
    # }
    def __init__(self,
                 sizex=10,
                 sizey=20,
                 blockwidth=10,
                 blockborder=2):
        self.board = np.full([sizey, sizex], -1, dtype=np.int8)
        self.newpiece()
        self.blockborder = blockborder
        self.blockwidth = blockwidth
        # YxXxRBG array for the display
        # self.screen = np.zeros([blockwidth * sizey, blockwidth * sizex, 3])
        self.step_counter = 0
        self.total_frames = 0
        self.lines = 0
        self.level = 8
        self.move = 0

        # self.update()

    def isinbounds(self,x,y):
        # Really? Cool.
        # print("{}, {} inbounds: {}".format(x,y,0 <= x < self.board.shape[0] and 0 <= y < self.board.shape[1]))
        return 0 <= x < self.board.shape[0] and 0 <= y < self.board.shape[1]

    def newpiece(self):
        self.activepiece = TetrisPiece()

    def movepiece(self, move):
        # for x,y,_ in self.activepiece.points:
        #     self.board[x,y] = -1
        # newpoints = move @ self.activepiece.points.T
        #
        #

        self.delpiece()
        x, y, r = TetrisBoard.moves[move]
        self.move = 0 # 'Consume' a movement
        if r:
            _, points = self.activepiece.calc_rotation()
        else:
            points = self.activepiece.points
        for p in points:
            px = self.activepiece.offsetx + x + p[0]
            py = self.activepiece.offsety + y + p[1]

            if not self.isinbounds(px,py) or self.board[px,py] != -1:
                # Invalid move
                # print(self.board[px,py],self.isinbounds(px,py))
                self.putpiece()
                print("Couldn't execute move {}".format((x,y,r)))
                if x == 1: # If we were trying to moving down...
                    self.newpiece() # then place & spawn a new piece
                return False
        if r:
            self.activepiece.do_rotation()
        self.activepiece.offsetx += x
        self.activepiece.offsety += y
        self.putpiece()
        return True

    def putpiece(self):
        for p in self.activepiece.points:
            x = self.activepiece.offsetx + p[0]
            y = self.activepiece.offsety + p[1]
            self.board[x,y] = self.activepiece.piece # blocks keep the color of their piece

    def clearline(self):
        self.lines += 1
        if self.lines % 10 == 0 and self.level < 10:
            self.level += 1

    def delpiece(self):
        for p in self.activepiece.points:
            x = self.activepiece.offsetx + p[0]
            y = self.activepiece.offsety + p[1]
            self.board[x,y] = -1


    def draw(self):

        self.screen = np.ones([self.board.shape[0] * self.blockwidth,self.board.shape[1] * self.blockwidth,3])
        for x in range(self.board.shape[0]):
            for y in range(self.board.shape[1]):
                if self.board[x,y] != -1:
                    draw_on_grid(self.screen, y, x, self.blockwidth, self.blockborder, TetrisPiece.block_colors[self.board[x,y]], [0,0,0])
        # for p in self.activepiece.points:
        #     draw_on_grid(self.screen, p[1] + self.activepiece.offsety, p[0] + self.activepiece.offsetx, self.blockwidth, self.blockborder, self.activepiece.color, [0,0,0])
        mpl.image.imsave('tetris-board-frame-{}.png'.format(self.total_frames), self.screen)
        #
        # plt.imshow(image)
        # plt.show()
        # plt.imshow(self.board)
        # plt.xticks(np.arange(0,10,1))
        # plt.yticks(np.arange(0,20,1))
        # plt.grid()
        # plt.show()

    # def drop(self):
    #     if not self.movepiece(1,0):
    #         self.newpiece()
        # self.activepiece.offsetx += 1
        # self.draw()

    def getboard(self):
        return self.board

    def tick(self, inp):
        self.step_counter += 1
        self.total_frames += 1
        # self.move = inp
        if self.step_counter == 11 - self.level:
            self.step_counter = 0
            inp[2] == True # You are now pressing down.
        transform = np.eye(3)
        for button, move in zip(inp, TetrisBoard.affineMoves):
            if button:
                transform = transform @ move

        self.movepiece(transform)
        self.draw()


#
#
# if __name__ == '__main__':
#
#     plt.ion()
#     tb = TetrisBoard()
#     tb.drawpiece()
#     im = plt.imshow(tb.board, animated=True)
#     def update(*args):
#         print(tb.board)
#         tb.board = np.zeros([20,10])
#         tb.newpiece()
#         tb.drawpiece()
#         im.set_array(tb.board)
#         return im,
#     # plt.show()
#     # time.sleep(5)
#     import matplotlib.animation as animation
#     time.sleep(1)
#     plt.show()
#     update()
#     time.sleep(1)
#     # for i in range(100):
#         # print(i)
#
#         # ms.set_data(tb.board)
#         # time.sleep(1)
tb = TetrisBoard()
for i in range(300):
   tb.tick([True, False, False, False, False])

#
# class GameState:
#     def __init__(self):
#         global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
#         pygame.init()
#         FPSCLOCK = pygame.time.Clock()
#         DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
#         BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
#         BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
#         pygame.display.iconify()
#         pygame.display.set_caption('Tetromino')
#
#         # DEBUG
#         self.total_lines = 0
#
#         # setup variables for the start of the game
#         self.board = self.getBlankBoard()
#         self.lastMoveDownTime = time.time()
#         self.lastMoveSidewaysTime = time.time()
#         self.lastFallTime = time.time()
#         self.movingDown = False # note: there is no movingUp variable
#         self.movingLeft = False
#         self.movingRight = False
#         self.score = 0
#         self.lines = 0
#         self.height = 0
#         self.level, self.fallFreq = self.calculateLevelAndFallFreq()
#
#         self.fallingPiece = self.getNewPiece()
#         self.nextPiece = self.getNewPiece()
#
#         self.frame_step([1,0,0,0,0,0])
#
#         pygame.display.update()
#
#     def reinit(self):
#         self.board = self.getBlankBoard()
#         self.lastMoveDownTime = time.time()
#         self.lastMoveSidewaysTime = time.time()
#         self.lastFallTime = time.time()
#         self.movingDown = False # note: there is no movingUp variable
#         self.movingLeft = False
#         self.movingRight = False
#         self.score = 0
#         self.lines = 0
#         self.height = 0
#         self.level, self.fallFreq = self.calculateLevelAndFallFreq()
#
#         self.fallingPiece = self.getNewPiece()
#         self.nextPiece = self.getNewPiece()
#
#         self.frame_step([1,0,0,0,0,0])
#
#         pygame.display.update()
#
#
#     def frame_step(self,input):
#         # The meat
#         self.movingLeft = False
#         self.movingRight = False
#
#         reward = 0
#         terminal = False
#
#         #none is 100000, left is 010000, up is 001000, right is 000100, space is 000010, q is 000001
#         if self.fallingPiece == None:
#             # No falling piece in play, so start a new piece at the top
#             self.fallingPiece = self.nextPiece
#             self.nextPiece = self.getNewPiece()
#             self.lastFallTime = time.time() # reset self.lastFallTime
#
#             if not self.isValidPosition():
#                 image_data = pygame.surfarray.array3d(pygame.display.get_surface())
#                 terminal = True
#
#                 self.reinit()
#                 return image_data, reward, terminal # can't fit a new piece on the self.board, so game over
#         # Reimplement these as linear transforms
#
#
#         # moving the piece sideways
#         if (input[1] == 1) and self.isValidPosition(adjX=-1):
#             self.fallingPiece['x'] -= 1
#             self.movingLeft = True
#             self.movingRight = False
#             self.lastMoveSidewaysTime = time.time()
#
#         elif (input[3] == 1) and self.isValidPosition(adjX=1):
#             self.fallingPiece['x'] += 1
#             self.movingRight = True
#             self.movingLeft = False
#             self.lastMoveSidewaysTime = time.time()
#
#         # rotating the piece (if there is room to rotate)
#         elif (input[2] == 1):
#             self.fallingPiece['rotation'] = (self.fallingPiece['rotation'] + 1) % len(PIECES[self.fallingPiece['shape']])
#             if not self.isValidPosition():
#                 self.fallingPiece['rotation'] = (self.fallingPiece['rotation'] - 1) % len(PIECES[self.fallingPiece['shape']])
#
#         elif (input[5] == 1): # rotate the other direction
#             self.fallingPiece['rotation'] = (self.fallingPiece['rotation'] - 1) % len(PIECES[self.fallingPiece['shape']])
#             if not self.isValidPosition():
#                 self.fallingPiece['rotation'] = (self.fallingPiece['rotation'] + 1) % len(PIECES[self.fallingPiece['shape']])
#
#         # move the current piece all the way down
#         elif (input[4] == 1):
#             self.movingDown = False
#             self.movingLeft = False
#             self.movingRight = False
#             for i in range(1, BOARDHEIGHT):
#                 if not self.isValidPosition(adjY=i):
#                     break
#             self.fallingPiece['y'] += i - 1
#
#         # handle moving the piece because of user input
#         if (self.movingLeft or self.movingRight):
#             if self.movingLeft and self.isValidPosition(adjX=-1):
#                 self.fallingPiece['x'] -= 1
#             elif self.movingRight and self.isValidPosition(adjX=1):
#                 self.fallingPiece['x'] += 1
#             self.lastMoveSidewaysTime = time.time()
#
#         if self.movingDown:
#             self.fallingPiece['y'] += 1
#             self.lastMoveDownTime = time.time()
#
#         # let the piece fall if it is time to fall
#         # see if the piece has landed
#         cleared = 0
#         if not self.isValidPosition(adjY=1):
#             # falling piece has landed, set it on the self.board
#             self.addToBoard()
#
#             cleared = self.removeCompleteLines()
#             if cleared > 0:
#                 if cleared == 1:
#                     self.score += 40 * self.level
#                 elif cleared == 2:
#                     self.score += 100 * self.level
#                 elif cleared == 3:
#                     self.score += 300 * self.level
#                 elif cleared == 4:
#                     self.score += 1200 * self.level
#
#             self.score += self.fallingPiece['y']
#
#             self.lines += cleared
#             self.total_lines += cleared
#
#             reward = self.height - self.getHeight()
#             self.height = self.getHeight()
#
#             self.level, self.fallFreq = self.calculateLevelAndFallFreq()
#             self.fallingPiece = None
#
#         else:
#             # piece did not land, just move the piece down
#             self.fallingPiece['y'] += 1
#
#         # drawing everything on the screen
#         DISPLAYSURF.fill(BGCOLOR)
#         self.drawBoard()
#         #self.drawStatus()
#         #self.drawNextPiece()
#         if self.fallingPiece != None:
#            self.drawPiece(self.fallingPiece)
#
#         pygame.display.update()
#
#         if cleared > 0:
#             reward = 100 * cleared
#
#         image_data = pygame.surfarray.array3d(pygame.display.get_surface())
#         return image_data, reward, terminal
#
#     def getImage(self):
#         image_data = pygame.surfarray.array3d(pygame.transform.rotate(pygame.display.get_surface(), 90))
#         return image_data
#
#     def getActionSet(self):
#         return range(6)
#
#     def getHeight(self):
#         stack_height = 0
#         for i in range(0, BOARDHEIGHT):
#             blank_row = True
#             for j in range(0, BOARDWIDTH):
#                 if self.board[j][i] != '.':
#                     blank_row = False
#             if not blank_row:
#                 stack_height = BOARDHEIGHT - i
#                 break
#         return stack_height
#
#     def getReward(self):
#         # This should be configurable.
#         # In particular, the network should be able to learn this function.
#         stack_height = None
#         num_blocks = 0
#         for i in range(0, BOARDHEIGHT):
#             blank_row = True
#             for j in range(0, BOARDWIDTH):
#                 if self.board[j][i] != '.':
#                     num_blocks += 1
#                     blank_row = False
#             if not blank_row and stack_height is None:
#                 stack_height = BOARDHEIGHT - i
#
#         if stack_height is None:
#             return BOARDHEIGHT
#         else:
#             return BOARDHEIGHT - stack_height
#             return float(num_blocks) / float(stack_height * BOARDWIDTH)
#
#     def isGameOver(self):
#         # Termination
#         return self.fallingPiece == None and not self.isValidPosition()
#
#     def makeTextObjs(self,text, font, color):
#         surf = font.render(text, True, color)
#         return surf, surf.get_rect()
#
#     def calculateLevelAndFallFreq(self):
#         # Based on the self.score, return the self.level the player is on and
#         # how many seconds pass until a falling piece falls one space.
#         self.level = min(int(self.lines / 10) + 1, 10)
#         self.fallFreq = 0.27 - (self.level * 0.02)
#         return self.level, self.fallFreq
#
#     def getNewPiece(self):
#         # return a random new piece in a random rotation and color
#         shape = random.choice(list(PIECES.keys()))
#         newPiece = {'shape': shape,
#                     'rotation': random.randint(0, len(PIECES[shape]) - 1),
#                     'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
#                     'y': 0, # start it above the self.board (i.e. less than 0)
#                     'color': random.randint(0, len(COLORS)-1)}
#         return newPiece
#
#
#     def addToBoard(self):
#         # fill in the self.board based on piece's location, shape, and rotation
#         for x in range(TEMPLATEWIDTH):
#             for y in range(TEMPLATEHEIGHT):
#                 if PIECES[self.fallingPiece['shape']][self.fallingPiece['rotation']][y][x] != BLANK:
#                     self.board[x + self.fallingPiece['x']][y + self.fallingPiece['y']] = self.fallingPiece['color']
#
#
#     def getBlankBoard(self):
#         # create and return a new blank self.board data structure
#         self.board = []
#         for i in range(BOARDWIDTH):
#             self.board.append([BLANK] * BOARDHEIGHT)
#         return self.board
#
#
#     def isOnBoard(self,x, y):
#         return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT
#
#
#     def isValidPosition(self,adjX=0, adjY=0):
#         # Return True if the piece is within the self.board and not colliding
#         for x in range(TEMPLATEWIDTH):
#             for y in range(TEMPLATEHEIGHT):
#                 isAboveBoard = y + self.fallingPiece['y'] + adjY < 0
#                 if isAboveBoard or PIECES[self.fallingPiece['shape']][self.fallingPiece['rotation']][y][x] == BLANK:
#                     continue
#                 if not self.isOnBoard(x + self.fallingPiece['x'] + adjX, y + self.fallingPiece['y'] + adjY):
#                     return False
#                 if self.board[x + self.fallingPiece['x'] + adjX][y + self.fallingPiece['y'] + adjY] != BLANK:
#                     return False
#         return True
#
#     def isCompleteLine(self, y):
#         # Return True if the line filled with boxes with no gaps.
#         for x in range(BOARDWIDTH):
#             if self.board[x][y] == BLANK:
#                 return False
#         return True
#
#
#     def removeCompleteLines(self):
#         # Remove any completed lines on the self.board, move everything above them down, and return the number of complete lines.
#         numLinesRemoved = 0
#         y = BOARDHEIGHT - 1 # start y at the bottom of the self.board
#         while y >= 0:
#             if self.isCompleteLine(y):
#                 # Remove the line and pull boxes down by one line.
#                 for pullDownY in range(y, 0, -1):
#                     for x in range(BOARDWIDTH):
#                         self.board[x][pullDownY] = self.board[x][pullDownY-1]
#                 # Set very top line to blank.
#                 for x in range(BOARDWIDTH):
#                     self.board[x][0] = BLANK
#                 numLinesRemoved += 1
#                 # Note on the next iteration of the loop, y is the same.
#                 # This is so that if the line that was pulled down is also
#                 # complete, it will be removed.
#             else:
#                 y -= 1 # move on to check next row up
#         return numLinesRemoved
#
#
#     def convertToPixelCoords(self,boxx, boxy):
#         # Convert the given xy coordinates of the self.board to xy
#         # coordinates of the location on the screen.
#         return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))
#
#
#     def drawBox(self,boxx, boxy, color, pixelx=None, pixely=None):
#         # draw a single box (each tetromino piece has four boxes)
#         # at xy coordinates on the self.board. Or, if pixelx & pixely
#         # are specified, draw to the pixel coordinates stored in
#         # pixelx & pixely (this is used for the "Next" piece).
#         if color == BLANK:
#             return
#         if pixelx == None and pixely == None:
#             pixelx, pixely = self.convertToPixelCoords(boxx, boxy)
#         pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
#         pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))
#
#
#     def drawBoard(self):
#         # draw the border around the self.board
#         pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)
#
#         # fill the background of the self.board
#         pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
#         # draw the individual boxes on the self.board
#         for x in range(BOARDWIDTH):
#             for y in range(BOARDHEIGHT):
#                 self.drawBox(x, y, self.board[x][y])
#
#
#     def drawStatus(self):
#         # draw the self.score text
#         scoreSurf = BASICFONT.render('self.score: %s' % self.score, True, TEXTCOLOR)
#         scoreRect = scoreSurf.get_rect()
#         scoreRect.topleft = (WINDOWWIDTH - 150, 20)
#         DISPLAYSURF.blit(scoreSurf, scoreRect)
#
#         # draw the self.level text
#         levelSurf = BASICFONT.render('self.level: %s' % self.level, True, TEXTCOLOR)
#         levelRect = levelSurf.get_rect()
#         levelRect.topleft = (WINDOWWIDTH - 150, 50)
#         DISPLAYSURF.blit(levelSurf, levelRect)
#
#
#     def drawPiece(self,piece, pixelx=None, pixely=None):
#         shapeToDraw = PIECES[piece['shape']][piece['rotation']]
#         if pixelx == None and pixely == None:
#             # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
#             pixelx, pixely = self.convertToPixelCoords(piece['x'], piece['y'])
#
#         # draw each of the boxes that make up the piece
#         for x in range(TEMPLATEWIDTH):
#             for y in range(TEMPLATEHEIGHT):
#                 if shapeToDraw[y][x] != BLANK:
#                     self.drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))
#
#
#     def drawNextPiece(self):
#         # draw the "next" text
#         nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
#         nextRect = nextSurf.get_rect()
#         nextRect.topleft = (WINDOWWIDTH - 120, 80)
#         DISPLAYSURF.blit(nextSurf, nextRect)
#         # draw the "next" piece
#         self.drawPiece(self.nextPiece,pixelx=WINDOWWIDTH-120, pixely=100)
