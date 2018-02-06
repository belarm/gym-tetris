#!/usr/bin/env python3
# Modified from Tetromino by lusob luis@sobrecueva.com
# http://lusob.com
# Released under a "Simplified BSD" license

# import random, time, pygame, sys
# from pygame.locals import *
import numpy as np
import cv2
# from pynput import keyboard
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
    # TetrisMove(np.matrix[0,-1], np.eye(2)),
]
moveCount = len(moveList)
moveSpace = np.arange(moveCount)
# moveLeft = np.matrix([ # <- (-y)
#             [1,0,0],
#             [0,1,-1],
#             [0,0,1]])
# moveRight = np.matrix([ # -> (+y)
#             [1,0,0],
#             [0,1,1],
#             [0,0,1]])
# moveDown = np.matrix([ # | (+x)
#             [1,0,0],   # V
#             [0,1,1],
#             [0,0,1]])
# CCWRotation = np.matrix([ # CCW rotation
#             [0,-1,0],
#             [1,0,0],
#             [0,0,1]])
# CWRotation = np.matrix([ # CW rotation
#             [0,1,0],
#             [-1,0,0],
#             [0,0,1]])
# NoMove = np.eye(3) # 3x3 identity matrix

# TetrisPiece = namedtuple('TetrisPiece', 'name points moves')
# pieces = {
#     'O': TetrisPiece('O',
#         np.array([[0,0,1],[1,0,1],[1,-1,1],[0,-1,1]]),
#         [NoMove]),
#     'I': TetrisPiece('O',
#         np.array([[0,0,1],[0,1,1],[0,-1,1],[0,-2,1]]),
#         [CCWRotation, CWRotation]),
#     'S': TetrisPiece('S',
#         np.array([[0,0,1],[0,1,1],[1,0,1],[1,-1,1]]),
#         [CCWRotation]),
#     'Z': TetrisPiece('Z',
#         np.array([[0,0,1],[0,-1,1],[1,0,1],[1,1,1]]),
#         [CCWRotation]),
#     'L': TetrisPiece('L',
#         np.array([[0,0,1],[0,-1,1],[0,1,1],[1,-1,1]]),
#         [CCWRotation]),
#     'J': TetrisPiece('J',
#         np.array([[0,0,1],[0,-1,1],[0,1,1],[1,1,1]]),
#         [CCWRotation]),
#     'T': TetrisPiece('T',
#         np.array([[0,0,1],[0,-1,1],[0,1,1],[1,0,1]]),
#         [CCWRotation]),
# }
# block_colors = { # https://en.wikipedia.org/wiki/Tetris#Tetromino_colors : Tetris Company colors
#     'O': [1,1,0],
#     'I': [0,1,1],
#     'S': [0,1,0],
#     'Z': [1,0,0],
#     'L': [1,.6,0],
#     'J': [0,0,1],
#     'T': [.5,0,.5],
# }

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
        # self.translation = offsetx
        self.translation = np.array([[offsetx],[offsety]])
        # self.points=TetrisPiece.pieces[piece]
        # self.rotations = TetrisPiece.rotations[piece]
        # self.rotation = self.rotations[0]
        self.rotation = 0

    # def calc_rotation(self):
    #     rot = (self.rot_iter + 1) % 4 # number of rotations
    #     return rot, self.rotations[rot] @ self.points
    #     # return rot, np.vstack([TetrisPiece.rotations[self.piece][rot] @ p for p in self.points])
    #
    #
    # def do_rotation(self, direction):
    #     self.rot_iter
    #     self.rot_iter, self.points = self.calc_rotation()
    #     # self.rot_iter = (self.rot_iter + 1) % len(TetrisPiece.rotations[self.piece])

    @property
    def points(self):
        return TetrisPiece.rotations[self.piece][self.rotation] @ TetrisPiece.pieces[self.piece] + self.translation
        # return

#
# class TetrisPiece(object):
#     # 0, I, S, Z, L, J, T
#
#     def __init__(self, piece=None, offsetx=0, offsety=6, rot_iter=0):
#         if piece is None:
#             piece = np.random.choice(np.arange(len(TetrisPiece.pieces)))
#         self.piece = piece
#         self.points=TetrisPiece.pieces[piece]
#         self.rotations = TetrisPiece.rotations[piece]
#         self.rot_iter = 0
#         self.offsetx = offsetx
#         self.offsety = offsety
#         self.color = TetrisPiece.block_colors[piece]
#
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

        # self.update()

    def isinbounds(self,point):
        # Really? Cool.
        # return 0 <= x < self.board.shape[0] and 0 <= y < self.board.shape[1]
        # Slightly cooler:
        return (np.array([0,0]) <= point) * (point < self.board.shape)

    def newpiece(self):
        piece = np.random.choice(np.arange(len(TetrisPiece.pieces)))
        self.activepiece = TetrisPiece(piece)
        # self.rot_iter = 0

    def movepiece(self, move):
        # print("MOVE: {}".format(move))
        translation = np.array([[0],[0]])
        rotation = 0
        oldpoints = self.activepiece.points
        lockpiece = False
        for i, bit in enumerate(move):
            # print(bit)
            # print(moveList[i].translation)
            # print(bit * moveList[i].translation)
            self.activepiece.translation += bit * moveList[i].translation
            self.activepiece.rotation += bit * moveList[i].rotation
            if not self.isinbounds(self.activepiece.points.T).all():
                if i == self.forcedmove:
                    lockpiece = True
                self.activepiece.translation -= bit * moveList[i].translation
                self.activepiece.rotation -= bit * moveList[i].rotation
            # print(translation, rotation)
        # print(oldpoints)
        # Erase piece
        self.board[oldpoints[0,:],oldpoints[1,:]] = 0
        # self.activepiece.translation += translation
        # self.activepiece.rotation += rotation
        newpoints = self.activepiece.points
        # if not self.isinbounds(newpoints.T).all():
            # Undo the move
            # self.activepiece.translation -= translation
            # self.activepiece.rotation -= rotation
            # newpoints = oldpoints
        # Draw the piece
        self.board[newpoints[0,:],newpoints[1,:]] = self.activepiece.piece + 1
        # for x,y,_ in self.activepiece.points:
        #     self.board[x,y] = -1
        # newpoints = move @ self.activepiece.points.T

        #
        # self.delpiece()
        # x, y, r = TetrisBoard.moves[move]
        # self.move = 0 # 'Consume' a movement
        # if r:
        #     _, points = self.activepiece.calc_rotation()
        # else:
        #     points = self.activepiece.points
        # for p in points:
        #     px = self.activepiece.offsetx + x + p[0]
        #     py = self.activepiece.offsety + y + p[1]
        #
        #     if not self.isinbounds(px,py) or self.board[px,py] != -1:
        #         # Invalid move
        #         # print(self.board[px,py],self.isinbounds(px,py))
        #         self.putpiece()
        #         print("Couldn't execute move {}".format((x,y,r)))
        #         if x == 1: # If we were trying to moving down...
        #             self.newpiece() # then place & spawn a new piece
        #         return False
        # if r:
        #     self.activepiece.do_rotation()
        # self.activepiece.offsetx += x
        # self.activepiece.offsety += y
        # self.putpiece()
        # return True


    def putpiece(self):
        points = self.activepiece.points
        self.board[points[0,:],points[1,:]] = TetrisBoard.block_colors[self.activepiece.piece + 1]

    def delpiece(self):
        points = self.activepiece.points
        self.board[points[0,:],points[1,:]] = TetrisBoard.block_colors[0]

        # for p in self.activepiece.points:
        #     x = self.activepiece.offsetx + p[0]
        #     y = self.activepiece.offsety + p[1]
        #     self.board[x,y] = self.activepiece.piece # blocks keep the color of their piece

    def clearline(self):
        self.lines += 1
        if self.lines % 10 == 0 and self.level < 10:
            self.level += 1
    #
    # def delpiece(self):
    #     for p in self.activepiece.points:
    #         x = self.activepiece.offsetx + p[0]
    #         y = self.activepiece.offsety + p[1]
    #         self.board[x,y] = -1

    def draw(self):
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
        # for p in self.activepiece.points:
        #     draw_on_grid(self.screen, p[1] + self.activepiece.offsety, p[0] + self.activepiece.offsetx, self.blockwidth, self.blockborder, self.activepiece.color, [0,0,0])
        # mpl.image.imsave('tetris-board-frame-{}.png'.format(self.total_frames), self.screen)
        cv2.imshow('Tetris', self.screen)
        cv2.waitKey(1)

    def tick(self, inp):
        self.step_counter += 1
        self.total_frames += 1
        # self.move = inp
        if self.step_counter == 11 - self.level:
            self.step_counter = 0
            inp[2] = True # You are now pressing down.
            print("Dropping...")
        # transform = np.eye(3)
        # for button, move in zip(inp, TetrisBoard.affineMoves):
        #     if button:
        #         transform = transform @ move

        self.movepiece(inp)
        self.draw()


tb = TetrisBoard()

for i in range(120):
   tb.tick([True, False, False, False, False])
