__author__ = 'Mario Pena'
# Simple Checkers game on 5X5 board
# Implemented AI as an opponent

import copy

class Piece:
    def __init__(self, x, y, p):
        self.position = (x, y)
        self.state = 1
        self.player = p

    def get_position(self):
        return self.position

    def get_player(self):
        return self.player


def initialize_board():
    board = [["-" for t in range(5)]for p in range(10)]
    for x in range(5):
        for i in range(5):
            if x == 0 and i % 2 == 0 or x == 1 and i % 2 == 1:
                board[x][i] = Piece(x, i, "R")
            if x == 3 and i % 2 == 1 or x == 4 and i % 2 == 0:
                board[x][i] = Piece(x, i, "B")

    return board


class CheckerBoard:

    board = [["-" for t in range(5)]for p in range(5)]

    def __init__(self):
        self.board = initialize_board()
        self.hasWon = -1 # 0 for Black, 1 for Red, 2 for draw

    def print_board(self):
        for i in range(5):
            if i == 0:
                print "   ",
                print i,
            else:
                print " ",
                print i,
        print "\n"

        for x in range(5):
            for i in range(5):
                if self.board[x][i] == "-":
                    if i == 0:
                        print x,
                        print "| -",
                    elif i == 4:
                        print "| - |",
                    else:
                        print "| -",
                else:
                    if i == 0:
                        print x,
                        print "| " + self.board[x][i].get_player(),
                    elif i == 4:
                        print "| " + self.board[x][i].get_player() + " |",
                    else:
                        print "| " + self.board[x][i].get_player(),

            print "\n"

    def is_empty(self, x, y):
        return self.board[x][y] == "-"

    def within_boundaries(self, x, y):
        return 0 <= x <= 5 and 0 <= y <= 5

    def clone(self):
        return copy.copy(self)


def initialize_pieces(player, checker_board):
    if player.player == "R":
        list = {(0, 0): checker_board.board[0][0], (2, 0): checker_board.board[0][2],
                (4, 0): checker_board.board[0][4], (1, 1): checker_board.board[1][1], (3, 1): checker_board.board[1][3]}
    else:
        list = {(1, 3): checker_board.board[3][1], (3, 3): checker_board.board[3][3],
                (0, 4): checker_board.board[4][0], (2, 4): checker_board.board[4][2], (4, 4): checker_board.board[4][4]}
    return list

def piece_found(Player, x, y):

    retval = False;
    for cord, pieces in Player.pieces.iteritems():
        if cord == (x,y):
            #print cord
            retval = True;
    return retval

class Player:

    def __init__(self, p, checker_board):
        self.player = p
        self.pieces = initialize_pieces(self, checker_board)


    def move(self, checker_board, x1, y1, x2, y2):
        # Check if space is empty
        if checker_board.within_boundaries(x2, y2):
            if(piece_found(self, x1, y1) == False):
                print "You are trying to move a non-piece or an opponents piece."
            else:
                print "Legal Move"

        else:
            print "Illegal Move: Out of Bounds"


x = CheckerBoard()
red = Player("R", x)
black = Player("B", x)
x.print_board()
print x.is_empty(0, 1)
black.move(x, 4, 0, 1, 1)
black.move(x, 2, 0, 1, 1)
red.move(x, 2, 4, 1, 1)
red.move(x, 0, 0, 1, 1)
print "Red Pieces: ",
print red.pieces.keys()
print "Black Pieces: ",
print black.pieces.keys()
