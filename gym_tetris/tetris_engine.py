#!/usr/bin/env python3
# Modified from Tetromino by lusob luis@sobrecueva.com
# http://lusob.com
# Released under a "Simplified BSD" license

import numpy as np
# import cv2
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

# mpl.rcParams.update({'image.cmap': 'Accent',
#                      'image.interpolation': 'none',
#                      'axes.linewidth': 0})
TetrisMove = namedtuple('TetrisMove', 'translation rotation')

moveList = [
    # (<X,Y move as column vector>, <number of CCW pi/2 rotations>)
    TetrisMove(np.array([[0],[-1]]), 0), # <
    TetrisMove(np.array([[0],[1]]), 0),  # >
    TetrisMove(np.array([[0],[0]]), 1),  # CCW
    TetrisMove(np.array([[0],[0]]), -1), # CW
    TetrisMove(np.array([[1],[0]]), 0),  # V
]
moveCount = len(moveList)
moveSpace = np.arange(moveCount)

class TetrisPiece(object):
    # 0, I, S, Z, L, J, T
    pieces = [
        np.array([[0,0],[1,0],[1,-1],[0,-1]]).T,
        np.array([[0,0],[0,1],[0,-1],[0,-2]]).T,
        np.array([[0,0],[0,1],[1,0],[1,-1]]).T,
        np.array([[0,0],[0,-1],[1,0],[1,1]]).T,
        np.array([[0,0],[0,-1],[0,1],[1,-1]]).T,
        np.array([[0,0],[0,-1],[0,1],[1,1]]).T,
        np.array([[0,0],[0,-1],[0,1],[1,0]]).T
    ]
    block_colors = [ # https://en.wikipedia.org/wiki/Tetris#Tetromino_colors : Tetris Company colors
        [1,1,0],[0,1,1],[0,1,0],[1,0,0],[1,.6,0],[0,0,1],[.5,0,.5],
    ]

    identity_rotation = np.array([[ 1, 0], [ 0, 1]])
    # Rotate pi/2 CCW
    ccw_rotation = np.array([[ 0,-1], [ 1, 0]])
    # Rotate pi/2 CW
    cw_rotation = np.array([[ 0, 1], [-1, 0]])
    # Rotate 180 degrees
    pi_rotation = np.array([[-1,  0], [ 0, -1]])

    # We'll iterate over the list of rotations for the active piece, applying each
    # in turn (i % len(rotations[piece]))
    rotations = [
        [identity_rotation, identity_rotation, identity_rotation, identity_rotation],
        [identity_rotation, ccw_rotation, identity_rotation, ccw_rotation],
        [identity_rotation, ccw_rotation, identity_rotation, ccw_rotation],
        [identity_rotation, ccw_rotation, identity_rotation, ccw_rotation],
        [identity_rotation, ccw_rotation, pi_rotation, cw_rotation],
        [identity_rotation, ccw_rotation, pi_rotation, cw_rotation],
        [identity_rotation, ccw_rotation, pi_rotation, cw_rotation],
    ]
    def __init__(self, piece=None, offsetx=0, offsety=6, rot_iter=0):
        if piece is None:
            piece = np.random.choice(np.arange(len(TetrisPiece.pieces)))
        self.piece = piece
        self.translation = np.array([[offsetx],[offsety]])
        self.rotation = 0

    @property
    def points(self):
        return TetrisPiece.rotations[self.piece][self.rotation % 4] @ TetrisPiece.pieces[self.piece] + self.translation


class TetrisBoard(object):
    block_colors = [ # https://en.wikipedia.org/wiki/Tetris#Tetromino_colors : Tetris Company colors
        [1,1,1],[1,1,0],[0,1,1],[0,1,0],[1,0,0],[1,.6,0],[0,0,1],[.5,0,.5],
    ]
    border_colors = [
        [1,1,1],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
    ]

    def __init__(self,
                 sizex=10,
                 sizey=20,
                 blockwidth=10,
                 blockborder=2,
                 forcedmove=4):
        self.board = np.zeros([sizey, sizex], dtype=np.int8)
        self.oldboard = np.ones([sizey, sizex], dtype=np.int8)
        self.newpiece()
        self.blockborder = blockborder
        self.blockwidth = blockwidth
        # YxXxRBG array for the display
        # self.screen = np.ones([blockwidth * sizey, blockwidth * sizex, 3], dtype=np.uint8)
        self.screen = np.ones([self.board.shape[0] * self.blockwidth,self.board.shape[1] * self.blockwidth,3])
        self.oldscreen = np.ones([self.board.shape[0] * self.blockwidth,self.board.shape[1] * self.blockwidth,3])

        self.step_counter = 0
        self.total_frames = 0
        self.lines = 0
        self.level = 1
        # self.move = NoMove
        self.rot_iter = 0
        self.forcedmove = forcedmove
        self.gameover = False


        # self.update()

    def isinbounds(self,points):
        # Really? Cool.
        for x,y in points:
            if not (0 <= x < self.board.shape[0] and 0 <= y < self.board.shape[1] and self.board[x,y] == 0):
                return False
        return True
        # Slightly cooler:
        # return (np.array([0,0]) <= point) * (point < self.board.shape)

    def newpiece(self):
        self.check_lines()
        piece = np.random.choice(np.arange(len(TetrisPiece.pieces)))
        self.activepiece = TetrisPiece(piece)
        if not self.isinbounds(self.activepiece.points.T):
            # Waa-wahh
            self.gameover = True
            print("You lose!")

    def movepiece(self, move):
        # print("Move: {}".format(move))
        oldpoints = self.activepiece.points
        lockpiece = False
        self.board[oldpoints[0,:],oldpoints[1,:]] = 0
        for i, bit in enumerate(move):
            self.activepiece.translation += bit * moveList[i].translation
            self.activepiece.rotation += bit * moveList[i].rotation
            if not self.isinbounds(self.activepiece.points.T):
                if i == self.forcedmove:
                    lockpiece = True
                self.activepiece.translation -= bit * moveList[i].translation
                self.activepiece.rotation -= bit * moveList[i].rotation
        newpoints = self.activepiece.points
        self.board[newpoints[0,:],newpoints[1,:]] = self.activepiece.piece + 1
        if lockpiece:
            self.newpiece()

    def check_lines(self):
        for i in range(len(self.board)):
            if np.product(self.board[i]) > 0:
                self.clearline(i)


    def clearline(self, line):
        self.lines += 1
        if self.lines % 10 == 0 and self.level < 10:
            self.level += 1
        for i in range(line,0,-1):
            self.board[i] = self.board[i-1]
        self.board[0] = np.zeros([self.board.shape[1]])

    def draw(self):
        # print(np.average(self.oldscreen-self.screen))
        changed = self.oldboard != self.board
        # print(self.oldboard - self.board)
        # Should really draw a differential, rather than blitting the whole thing
        # self.screen = np.ones([self.board.shape[0] * self.blockwidth,self.board.shape[1] * self.blockwidth,3])
        count = 0
        for x in range(self.board.shape[0]):
            for y in range(self.board.shape[1]):
                # if self.board[x,y] != self.oldboard[x,y]:
                if changed[x,y]:
                # if True:
                    draw_on_grid(
                        self.screen,
                        y, x,
                        self.blockwidth,
                        self.blockborder,
                        TetrisBoard.block_colors[self.board[x,y]],
                        TetrisBoard.border_colors[self.board[x,y]]
                    )
                    count += 1
        self.oldboard = np.copy(self.board)
        # print("Updated {} blocks".format(count))
        # plt.imshow(self.screen)
        # plt.show()
        mpl.image.imsave('tetris-board-frame-{:03}.png'.format(self.total_frames), self.screen)
        # self.oldscreen = np.copy(self.screen)
        # cv2.imshow('Tetris', self.screen)
        # if self.total_frames % 20 == 0:
        # return cv2.waitKey(1)


    def tick(self, inp):
        self.step_counter += 1
        self.total_frames += 1
        if self.step_counter == 11 - self.level:
            self.step_counter = 0
            inp[self.forcedmove] = True # You are now pressing down.
            print("Dropping...")
        self.movepiece(inp)
        self.draw()
        return self.screen




tb = TetrisBoard()

input_mapping = {
    -1: np.array([False, False, False, False, False]),
    81: np.array([True, False, False, False, False]),
    83: np.array([False, True, False, False, False]),
    122: np.array([False, False, True, False, False]),
    120: np.array([False, False, False, True, False]),
    84: np.array([False, False, False, False, True]),
}


def convolve(screen, imgfilter, stride, padding):
    # print(screen.shape)
    # newscreen = np.pad(screen, [(1,1),(1,1),(0,0)], 'constant')
    d0 = imgfilter.shape[0]
    d1 = imgfilter.shape[1]
    padded = np.pad(
        screen,
        ((padding,padding),(padding,padding),(0,0)),
        'constant'
        )
    edgeloss = (imgfilter.shape[0:2] - np.array([1,1]))/2 - np.array([padding, padding])
    # edgeloss = edgeloss.astype(np.int)
    newimage = np.zeros(np.array(screen.shape[0:2] - edgeloss.astype(np.int)))
    for x in range(padded.shape[1] - d1 -1 ):
        for y in range(padded.shape[0] - d0 - 1):
            newimage[y, x] = np.sum(imgfilter * padded[y:y+d0,x:x+d1,:])
    return newimage



# for i in range(120):
keypress = 84
imgfilter = np.full((5,5,3), 1/75)
while(True):
#     # move = np.array([False, False, False, False, False])
#     # print(keypress)
    move = np.copy(input_mapping.get(keypress, np.array([False, False, False, False, False])))
#     # print("Move: {}".format(move))
#     # button = np.random.choice(np.arange(5))
#     # move[buttona] = True
#     move = np.array([False, False, False, False, False])
    screen = tb.tick(move)
    convolved = convolve(screen, imgfilter, None, 2)
    mpl.image.imsave('tetris-board-convolved-{:03}.png'.format(tb.total_frames), convolved)

    # cv2.showimage
#
    if tb.gameover:
        break

    # tb.tick([True, True, True, True, True]) # PRESS ALL THE BUTTONS!
    # if(tb.gameover or keypress == 27):
        # break
# cv2.destroyAllWindows()
