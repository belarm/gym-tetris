#!/usr/bin/env python3
# Modified from Tetromino by lusob luis@sobrecueva.com
# http://lusob.com
# Released under a "Simplified BSD" license

import numpy as np
import cv2
# import matplotlib as mpl
# import matplotlib.pyplot as plt
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
    TetrisMove(np.array([[1],[0]]), 0),  # V
    TetrisMove(np.array([[0],[0]]), 1),  # CCW
    TetrisMove(np.array([[0],[0]]), -1), # CW
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
    twopi_rotation = np.array([[-1,  0], [ 0, -1]])

    # We'll iterate over the list of rotations for the active piece, applying each
    # in turn (i % len(rotations[piece]))
    rotations = [
        [identity_rotation, identity_rotation, identity_rotation, identity_rotation],
        [identity_rotation, ccw_rotation, identity_rotation, ccw_rotation],
        [identity_rotation, ccw_rotation, twopi_rotation, cw_rotation],
        [identity_rotation, ccw_rotation, twopi_rotation, cw_rotation],
        [identity_rotation, ccw_rotation, twopi_rotation, cw_rotation],
        [identity_rotation, ccw_rotation, twopi_rotation, cw_rotation],
        [identity_rotation, ccw_rotation, twopi_rotation, cw_rotation],
    ]
    def __init__(self, piece=None, offsetx=0, offsety=6, rot_iter=0):
        if piece is None:
            piece = np.random.choice(np.arange(len(TetrisPiece.pieces)))
        self.piece = piece
        self.translation = np.array([[offsetx],[offsety]])
        self.rotation = 0

    @property
    def points(self):
        return TetrisPiece.rotations[self.piece][self.rotation] @ TetrisPiece.pieces[self.piece] + self.translation


class TetrisBoard(object):
    block_colors = [ # https://en.wikipedia.org/wiki/Tetris#Tetromino_colors : Tetris Company colors
        [1,1,1],[1,1,0],[0,1,1],[0,1,0],[1,0,0],[1,.6,0],[0,0,1],[.5,0,.5],
    ]
    border_colors = [ # https://en.wikipedia.org/wiki/Tetris#Tetromino_colors : Tetris Company colors
        [1,1,1],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
    ]

    def __init__(self,
                 sizex=10,
                 sizey=20,
                 blockwidth=10,
                 blockborder=2,
                 forcedmove=2):
        self.board = np.zeros([sizey, sizex], dtype=np.int8)
        self.newpiece()
        self.blockborder = blockborder
        self.blockwidth = blockwidth
        # YxXxRBG array for the display
        self.screen = np.zeros([blockwidth * sizey, blockwidth * sizex, 3], dtype=np.uint8)
        self.step_counter = 0
        self.total_frames = 0
        self.lines = 0
        self.level = 8
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
        piece = np.random.choice(np.arange(len(TetrisPiece.pieces)))
        self.activepiece = TetrisPiece(piece)
        if not self.isinbounds(self.activepiece.points.T):
            # Waa-wahh
            self.gameover = True
            print("You lose!")

    def movepiece(self, move):
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

    def clearline(self):
        self.lines += 1
        if self.lines % 10 == 0 and self.level < 10:
            self.level += 1

    def draw(self):
        # Should really draw a differential, rather than blitting the whole thing
        self.screen = np.ones([self.board.shape[0] * self.blockwidth,self.board.shape[1] * self.blockwidth,3])
        for x in range(self.board.shape[0]):
            for y in range(self.board.shape[1]):
                # if self.board[x,y] != -1:
                draw_on_grid(
                    self.screen,
                    y, x,
                    self.blockwidth,
                    self.blockborder,
                    TetrisBoard.block_colors[self.board[x,y]],
                    TetrisBoard.border_colors[self.board[x,y]]
                )
        # mpl.image.imsave('tetris-board-frame-{}.png'.format(self.total_frames), self.screen)
        cv2.imshow('Tetris', self.screen)
        # if self.total_frames % 20 == 0:
        cv2.waitKey(1)

    def tick(self, inp):
        self.step_counter += 1
        self.total_frames += 1
        if self.step_counter == 11 - self.level:
            self.step_counter = 0
            inp[2] = True # You are now pressing down.
            # print("Dropping...")
        self.movepiece(inp)
        self.draw()


tb = TetrisBoard()

for i in range(120):
   tb.tick([True, True, True, True, True])
   if(tb.gameover):
       break
