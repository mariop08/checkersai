__author__ = 'Mario Pena'
# Simple Checkers game on 5X5 board
# Implemented AI as an opponent
# Assumption: AI will always be the Black Player
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

    def clone(self):
        return copy.copy(self)


def initialize_board():
    board = [["-" for t in range(5)] for p in range(10)]
    for x in range(5):
        for i in range(5):
            if x == 0 and i % 2 == 0 or x == 1 and i % 2 == 1:
                board[x][i] = Piece(x, i, "R")
            if x == 3 and i % 2 == 1 or x == 4 and i % 2 == 0:
                board[x][i] = Piece(x, i, "B")

    return board


class CheckerBoard:
    board = [["-" for t in range(5)] for p in range(5)]

    def __init__(self):
        self.board = initialize_board()
        self.red_pieces = []
        self.black_pieces = []
        self.won = ""
        self.turn = 1  # 1 is player, -1 is AI

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
        return self.board[y][x] == "-"

    def within_boundaries(self, x, y):
        return 0 <= x <= 4 and 0 <= y <= 4

    def clone(self):
        return copy.deepcopy(self)

    def update_pieces(self, player):
        if self.player == "R":
            self.red_pieces = player.pieces
        else:
            self.black_pieces = player.pieces

    def has_won(self):
        if not self.black_pieces:
            self.won = "R"
        if not self.red_pieces:
            self.won = "B"

        count_b = 0
        count_r = 0

        # Check if all pieces are on opposite side of board
        for x, y in self.black_pieces:
            if y == 0:
                count_b += 1
        if count_b == len(self.black_piece):
            self.won = "B"

        for x, y in self.red_pieces:
            if y == 0:
                count_r += 1
        if count_r == len(self.red_piece):
            self.won = "R"

    def generate_moves(self, player):

        retlist = []

        for x, y in player.pieces:
            if player.player == "R":
                t, u = 1, 2
            else:
                t, u = -1, -2

            p1, p2, p3, p4 = (player.clone(), player.clone(), player.clone(), player.clone())
            b1, b2, b3, b4 = (self.clone(), self.clone(), self.clone(), self.clone())

            if p1.move(b1, x, y, x-1, y+t) == 0:
                retlist.append((x, y, x-1, y+t))

            if p2.move(b2, x, y, x+1, y+t) == 0:
                retlist.append((x, y, x+1, y+t))

            if p3.move(b3, x, y, x-2, y+u) == 0:
                retlist.append((x, y, x-2, y+u))

            if p4.move(b4, x, y, x+2, y+u) == 0:
                retlist.append((x, y, x+2, y+u))

        return retlist


def initialize_pieces(player, checker_board):
    if player.player == "R":
        piece_list = {(0, 0): checker_board.board[0][0], (2, 0): checker_board.board[0][2],
                      (4, 0): checker_board.board[0][4], (1, 1): checker_board.board[1][1],
                      (3, 1): checker_board.board[1][3]}
    else:
        piece_list = {(1, 3): checker_board.board[3][1], (3, 3): checker_board.board[3][3],
                      (0, 4): checker_board.board[4][0], (2, 4): checker_board.board[4][2],
                      (4, 4): checker_board.board[4][4]}
    return piece_list


def own_piece(player, x1, y1):
    for x2, y2 in player.pieces:
        if x1 == x2 and y1 == y2:
            return True
    return False


class Player:
    def __init__(self, p, checker_board):
        self.player = p
        self.pieces = initialize_pieces(self, checker_board)
        if self.player == "R":
            checker_board.red_pieces = self.pieces
        else:
            checker_board.black_pieces = self.pieces

    def clone(self):
        return copy.deepcopy(self)

    def update(self, checker_board):
        if self.player == "R":
            self.pieces = checker_board.red_pieces
        else:
            self.pieces = checker_board.black_pieces

    def move(self, checker_board, x1, y1, x2, y2):

        if not checker_board.within_boundaries(x2, y2):
            return "That move is out of boundaries!"
        # Check if space is empty
        if not checker_board.is_empty(x2, y2):
            return "Space is not empty, try another space"
        if not own_piece(self, x1, y1):
            return "That is not your piece or an empty space"

        if self.player == "R":
            # Red Captures a Black Piece (+2,+2)
            if checker_board.is_empty(x2, y2) and y1 + 2 == y2 and x1 + 2 == x2:
                if checker_board.is_empty(x1 + 1, y1 + 1):
                    return "Illegal Move"
                if own_piece(self, x1 + 1, y1 + 1):
                    return "You cannot capture your own piece"

                # Move player piece into space after jumping
                self.pieces[(x2, y2)] = self.pieces[(x1, y1)]
                checker_board.board[y2][x2] = checker_board.board[y1][x1]
                checker_board.board[y1][x1] = "-"
                del checker_board.red_pieces[(x1, y1)]
                checker_board.red_pieces[x2, y2] = checker_board.board[y2][x2]

                # Remove opponent from board and player pieces list
                checker_board.board[y1 + 1][x1 + 1] = "-"
                del checker_board.black_pieces[(x1 + 1, y1 + 1)]

                # Update the pieces in Player object
                self.update(checker_board)

                checker_board.turn *= -1
                return 0

            # Red Captures a Black Piece (-2,+2)
            if checker_board.is_empty(x2, y2) and y1 + 2 == y2 and x1 - 2 == x2:
                if checker_board.is_empty(x1 - 1, y1 + 1):
                    return "Illegal Move"
                if own_piece(self, x1 - 1, y1 + 1):
                    return "You cannot capture your own piece"

                # Move player piece into space after jumping
                checker_board.board[y2][x2] = checker_board.board[y1][x1]
                checker_board.board[y1][x1] = "-"
                del checker_board.red_pieces[(x1, y1)]
                checker_board.red_pieces[x2, y2] = checker_board.board[y2][x2]

                # Remove opponent from board and player pieces list
                checker_board.board[y1 + 1][x1 - 1] = "-"
                del checker_board.black_pieces[(x1 - 1, y1 + 1)]

                # Update the pieces in Player object
                self.update(checker_board)

                checker_board.turn *= -1
                return 0

            # Red move's into an unoccupied space
            if y2 - 1 == y1 and x2 + 1 == x1 or y2 - 1 == y1 and x2 - 1 == x1:
                self.pieces[(x2, y2)] = self.pieces[(x1, y1)]
                checker_board.board[y2][x2] = checker_board.board[y1][x1]
                checker_board.board[y1][x1] = "-"
                del self.pieces[(x1, y1)]

                checker_board.turn *= -1
                return 0
        #################################################################################
        #################################################################################
        if self.player == "B":
            # Black Captures a Red Piece (+2,-2)
            if checker_board.is_empty(x2, y2) and y1 - 2 == y2 and x1 + 2 == x2:
                if checker_board.is_empty(x1 + 1, y1 - 1):
                    return "Illegal Move"
                if own_piece(self, x1 + 1, y1 - 1):
                    return "You cannot capture your own piece"

                # Move player piece into space after jumping
                self.pieces[(x2, y2)] = self.pieces[(x1, y1)]
                checker_board.board[y2][x2] = checker_board.board[y1][x1]
                checker_board.board[y1][x1] = "-"
                del checker_board.black_pieces[(x1, y1)]
                checker_board.black_pieces[x2, y2] = checker_board.board[y2][x2]

                # Remove opponent from board
                checker_board.board[y1 - 1][x1 + 1] = "-"
                del checker_board.red_pieces[(x1 + 1, y1 - 1)]

                # Update the pieces in Player object
                self.update(checker_board)

                checker_board.turn *= -1
                return 0

            # Black Captures a Red Piece (-2,-2)
            if checker_board.is_empty(x2, y2) and y1 - 2 == y2 and x1 - 2 == x2:
                if checker_board.is_empty(x1 - 1, y1 - 1):
                    return "Illegal Move"
                if own_piece(self, x1 - 1, y1 - 1):
                    return "You cannot capture your own piece"

                # Move player piece into space after jumping
                checker_board.board[y2][x2] = checker_board.board[y1][x1]
                checker_board.board[y1][x1] = "-"
                del checker_board.black_pieces[(x1, y1)]
                checker_board.black_pieces[x2, y2] = checker_board.board[y2][x2]

                # Remove opponent from board
                checker_board.board[y1 - 1][x1 - 1] = "-"
                del checker_board.red_pieces[(x1 - 1, y1 - 1)]

                # Update the pieces in Player object
                self.update(checker_board)

                checker_board.turn *= -1
                return 0

            # Black move's into an unoccupied space
            if y2 + 1 == y1 and x2 - 1 == x1 or y2 + 1 == y1 and x2 + 1 == x1:
                self.pieces[(x2, y2)] = self.pieces[(x1, y1)]
                checker_board.board[y2][x2] = checker_board.board[y1][x1]
                checker_board.board[y1][x1] = "-"
                del self.pieces[(x1, y1)]
                # Capture a piece by jumping over it

                checker_board.turn *= -1
                return 0


class Node:
    def __init__(self, checker_board):
        self.current_board = checker_board
        self.children = []

def calc_heuristic(board, player):
    if player.self == "R":
        return 0.2

def print_current_board(board, player1, player2):
    board.print_board()
    print "Red Pieces:   ", player1.pieces.keys()
    print "Black Pieces: ", player2.pieces.keys(), "\n"


def test_run():
    x = CheckerBoard()
    Red = Player("R", x)
    Black = Player("B", x)
    # print "Check if (0,0) is empty:", x.is_empty(0, 0), "\n"
    print_current_board(x, Red, Black)
    Black.move(x, 1, 3, 2, 2)
    print_current_board(x, Red, Black)
    Red.move(x, 3, 1, 1, 3)
    print_current_board(x, Red, Black)
    Black.move(x, 0, 4, 2, 2)
    print_current_board(x, Red, Black)
    Red.move(x, 1, 1, 0, 2)
    print_current_board(x, Red, Black)
    Black.move(x, 2, 2, 1, 1)
    print_current_board(x, Red, Black)
    Red.move(x, 0, 0, 2, 2)
    print_current_board(x, Red, Black)
    print Black.move(x, 4, 4, 3, 3)
    print "\nAttempt to move into an occupied space:", Black.move(x, 3, 3, 2, 2)


print "Welcome to Checkers!"
# Initialize board and player objects
game_board = CheckerBoard()
red = Player("R", game_board)
black = Player("B", game_board)

while (game_board.won == ""):
    # Player's turn
    while (game_board.turn == 1):
        print_current_board(game_board, red, black)
        print game_board.generate_moves(red), "\n"
        my_input = raw_input("Red player enter a move: x1 y1 x2 y2\n")

        x1, y1, x2, y2 = my_input.split()

        retval = red.move(game_board, int(x1), int(y1), int(x2), int(y2))

        if not retval == "C" and not retval == "M":
            print retval, "\n"

    while(game_board.turn == -1):
        print "AI turn!"

        print game_board.generate_moves(black)

        game_board.turn *= -1
