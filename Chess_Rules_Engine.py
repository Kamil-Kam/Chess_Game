"""
Gamestate is a class which provides all methods to creating moves according to the rules, and supervising the course of the game.
The chess board is a two-dimensional list.
"""

import re


class GameState:
    def __init__(self):
        self.board = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                      ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
                      ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

        self.white_to_move = True
        self.move_log = []

        self.move_function = {'p': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves,
                              'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}

        self.white_king_position = (7, 4)
        self.black_king_position = (0, 4)
        self.checkmate = False
        self.stalemate = False

        self.pre_en_passant_possible_moves = []
        self.en_passant_moves = []
        self.pre_en_passant = False
        self.pre_en_passant_move_end_position = []

        self.white_queen_castling_mark = 0
        self.white_king_castling_mark = 0
        self.black_queen_castling_mark = 0
        self.black_king_castling_mark = 0
        self.any_castling_mark = self.black_queen_castling_mark * self.black_king_castling_mark \
                                 * self.white_queen_castling_mark * self.white_king_castling_mark

        self.white_queen_castling_currently = True
        self.white_king_castling_currently = True
        self.black_queen_castling_currently = True
        self.black_king_castling_currently = True

    def clear_currently_castlings(self):  # make every castling possible after move, then some functions check castlings possibility
        # before adding castlings to valid moves
        self.black_queen_castling_currently = True
        self.black_king_castling_currently = True
        self.white_queen_castling_currently = True
        self.white_king_castling_currently = True

    def are_castlings_possible(self, move: object(), num: int) -> None:
        # add or subtract castlings mark after each make_move and undo_move. It checks if rocks or king was moved. If castling is possible, castling_mark = 0.
        # This function is required to track castlings possibility while moves are making and undoing.
        if move.start_square == (0, 0) or move.end_square == (0, 0):
            self.black_queen_castling_mark += num
        if move.start_square == (0, 4) or move.end_square == (0, 4):
            self.black_queen_castling_mark += num
            self.black_king_castling_mark += num
        if move.start_square == (0, 7) or move.end_square == (0, 7):
            self.black_king_castling_mark += num

        if move.start_square == (7, 0) or move.end_square == (7, 0):
            self.white_queen_castling_mark += num
        if move.start_square == (7, 4) or move.end_square == (7, 4):
            self.white_queen_castling_mark += num
            self.white_king_castling_mark += num
        if move.start_square == (7, 7) or move.end_square == (7, 7):
            self.white_king_castling_mark += num

    def castling_under_attack(self):  # check castling possibility in a current position, if between king and rook are figures
        # or those squares are under attack or king is under attack -> disable castling
        castlings = [([(7, 2), (7, 3)], 'wQ'), ([(7, 5), (7, 6)], 'wK'),
                     ([(0, 2), (0, 3)], 'bQ'), ([(0, 5), (0, 6)], 'bK')]

        self.clear_currently_castlings()
        self.white_to_move = not self.white_to_move
        opponent_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move

        if not self.king_under_attack():

            for move in opponent_moves:

                if move.end_row == [7] and move.end_column == [4]:
                    self.white_queen_castling_currently = False
                    self.white_king_castling_currently = False

                elif self.board[7][1] != '--':
                    self.white_queen_castling_currently = False

                if move.end_row == 0 and move.end_column == 4:
                    self.black_queen_castling_currently = False
                    self.black_king_castling_currently = False

                elif self.board[0][1] != '--':
                    self.black_queen_castling_currently = False

                for castling in castlings:
                    squares = castling[0]
                    for square in squares:
                        if self.board[square[0]][square[1]] != '--' or (move.end_row == square[0] and move.end_column == square[1]):
                            if castling[1] == 'wQ':
                                self.white_queen_castling_currently = False
                            elif castling[1] == 'wK':
                                self.white_king_castling_currently = False
                            elif castling[1] == 'bQ':
                                self.black_queen_castling_currently = False
                            else:
                                self.black_king_castling_currently = False

    def append_castling_moves(self, moves: list) -> None:  # if castling are possible append castling moves to move list
        if self.white_to_move:
            if self.white_queen_castling_mark == 0 and self.white_queen_castling_currently:
                moves.append(Move((7, 4), (7, 2), self.board))
            if self.white_king_castling_mark == 0 and self.white_king_castling_currently:
                moves.append(Move((7, 4), (7, 6), self.board))
        else:
            if self.black_queen_castling_mark == 0 and self.black_queen_castling_currently:
                moves.append(Move((0, 4), (0, 2), self.board))
            if self.black_king_castling_mark == 0 and self.black_king_castling_currently:
                moves.append(Move((0, 4), (0, 6), self.board))

    @staticmethod
    def get_pawn_promotion() -> str:  # allow player to insert figure name when pawn is promoted
        while not re.match(r'^Q|R|B|N$', piece := input('Insert "Q" - Queen, or "R" - Rook, or "B" - Bishop, or "N" - Knight: \n')):
            pass
        return piece

    def append_pre_en_passant_moves(self) -> None:  # creates all possibly pre-en passant moves, run only one time at start
        row_black, row_white = 1, 6
        for column in range(0, 8):
            self.pre_en_passant_possible_moves.append(Move((row_black, column), (row_black + 2, column), self.board))
            self.pre_en_passant_possible_moves.append(Move((row_white, column), (row_white - 2, column), self.board))

    def is_pre_en_passant(self) -> None:  # if the last move is pre en passant -> allow en_passant moves
        if len(self.move_log) > 0:
            self.pre_en_passant = True if self.move_log[-1] in self.pre_en_passant_possible_moves else False

    def make_move(self, move: object()) -> None:  # make move, updates pieces positions on board, update king position, castling and en_passant flags
        promotion_color = 'w' if self.white_to_move else 'b'
        promotion_row = 0 if self.white_to_move else 7
        self.board[move.start_row][move.start_column] = '--'
        self.board[move.end_row][move.end_column] = move.piece_moved
        if move.piece_moved[1] == 'p' and move.end_row == promotion_row:
            self.board[move.end_row][move.end_column] = f'{promotion_color}Q'
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        if move.piece_moved == 'wK':
            self.white_king_position = (move.end_row, move.end_column)
        elif move.piece_moved == 'bK':
            self.black_king_position = (move.end_row, move.end_column)

        if move.piece_moved[1] == 'K':
            if abs(move.start_column - move.end_column) == 2:
                if move.end_column == 2:
                    self.board[move.end_row][0] = '--'
                    self.board[move.end_row][3] = f'{move.piece_moved[0]}R'
                elif move.end_column == 6:
                    self.board[move.end_row][7] = '--'
                    self.board[move.end_row][5] = f'{move.piece_moved[0]}R'

        if move in self.en_passant_moves:
            self.board[self.pre_en_passant_move_end_position[0]][self.pre_en_passant_move_end_position[1]] = '--'

        if move in self.pre_en_passant_possible_moves:
            self.pre_en_passant_move_end_position = [move.end_row, move.end_column]

        self.are_castlings_possible(move, 1)

    def undo_move(self) -> None:  # cancel move, cancel pieces positions, update king position, castlings and en_passant flags
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_column] = move.piece_moved
            self.board[move.end_row][move.end_column] = move.piece_captured
            self.white_to_move = not self.white_to_move
            if move.piece_moved == 'wK':
                self.white_king_position = (move.start_row, move.start_column)
            elif move.piece_moved == 'bK':
                self.black_king_position = (move.start_row, move.start_column)

            if move.piece_moved[1] == 'K':
                if abs(move.start_column - move.end_column) == 2:
                    if move.end_column == 2:
                        self.board[move.end_row][2] = '--'
                        self.board[move.end_row][3] = '--'
                        self.board[move.end_row][0] = f'{move.piece_moved[0]}R'

                    elif move.end_column == 6:
                        self.board[move.end_row][5] = '--'
                        self.board[move.end_row][7] = f'{move.piece_moved[0]}R'

            if len(self.move_log) > 0:
                premove = self.move_log[-1]
                if premove in self.pre_en_passant_possible_moves:
                    self.pre_en_passant_move_end_position = [premove.end_row, premove.end_column]

            if move in self.en_passant_moves:
                direction = move.end_column - move.start_column
                color = 'b' if self.white_to_move else 'w'
                self.board[move.start_row][move.start_column + direction] = f'{color}p'

            self.are_castlings_possible(move, -1)
            self.checkmate = False
            self.stalemate = False

    def get_valid_moves(self) -> list:  # call functions which add castlings and en_passant moves, check if moves are valid
        moves_list = self.get_all_possible_moves()

        self.en_passant_moves = []
        self.is_pre_en_passant()
        if self.pre_en_passant:
            self.get_pawn_en_passant_moves(moves_list)

        self.castling_under_attack()
        if self.any_castling_mark == 0:
            self.append_castling_moves(moves_list)

        for move_num in range(len(moves_list) - 1, -1, -1):
            self.make_move(moves_list[move_num])
            if self.king_under_attack():
                moves_list.remove(moves_list[move_num])
            self.undo_move()

        if len(moves_list) == 0:
            self.white_to_move = not self.white_to_move
            if self.king_under_attack():
                self.checkmate = True
            else:
                self.stalemate = True
            self.white_to_move = not self.white_to_move

        return moves_list

    def get_all_possible_moves(self) -> list:  # make a list of all possible normal moves (no castlings and en_passant), does not consider if moves are allowed by rules
        moves = []  # after each turn clears moves list
        move_color = 'w' if self.white_to_move else 'b'
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                if move_color == self.board[row][column][0]:
                    piece = self.board[row][column][1]
                    self.move_function[piece](row, column, moves)

        return moves

    def king_under_attack(self) -> bool:  # check if king is under attack
        king_row = self.black_king_position[0] if self.white_to_move else self.white_king_position[0]
        king_column = self.black_king_position[1] if self.white_to_move else self.white_king_position[1]
        opponent_moves = self.get_all_possible_moves()
        for move in opponent_moves:
            if move.end_row == king_row and move.end_column == king_column:
                return True
        return False

    def get_pawn_en_passant_moves(self, moves: list) -> None:  # add en_passant moves to moves list and en_passant_moves list
        moving_piece = 'wp' if self.white_to_move else 'bp'
        row_move_direction = -1 if self.white_to_move else 1
        row = self.pre_en_passant_move_end_position[0]
        column = self.pre_en_passant_move_end_position[1]

        if 0 <= self.pre_en_passant_move_end_position[1] < 7:
            if self.board[row][column + 1] == moving_piece:
                move = Move((row, column + 1), (row + row_move_direction, column), self.board)
                moves.append(move)
                self.en_passant_moves.append(move)

        if 0 < self.pre_en_passant_move_end_position[1] <= 7:
            if self.board[row][column - 1] == moving_piece:
                move = Move((row, column - 1), (row + row_move_direction, column), self.board)
                moves.append(move)
                self.en_passant_moves.append(move)

    def get_pawn_moves(self, row: int, column: int, moves: list) -> None:
        if self.white_to_move:
            if self.board[row - 1][column] == '--':
                moves.append(Move((row, column), (row - 1, column), self.board))
                if row == 6 and self.board[row - 2][column] == '--':
                    moves.append(Move((row, column), (row - 2, column), self.board))
            if column - 1 >= 0:
                if self.board[row - 1][column - 1][0] == 'b':
                    moves.append(Move((row, column), (row - 1, column - 1), self.board))
            if column + 1 <= 7:
                if self.board[row - 1][column + 1][0] == 'b':
                    moves.append(Move((row, column), (row - 1, column + 1), self.board))

        else:
            if self.board[row + 1][column] == '--':
                moves.append(Move((row, column), (row + 1, column), self.board))
                if row == 1 and self.board[row + 2][column] == '--':
                    moves.append(Move((row, column), (row + 2, column), self.board))
            if column - 1 >= 0:
                if self.board[row + 1][column - 1][0] == 'w':
                    moves.append(Move((row, column), (row + 1, column - 1), self.board))
            if column + 1 <= 7:
                if self.board[row + 1][column + 1][0] == 'w':
                    moves.append(Move((row, column), (row + 1, column + 1), self.board))

    def get_rook_moves(self, row: int, column: int, moves: list) -> None:
        directions = ((0, 1), (0, -1), (1, 0), (-1, 0))
        enemy_color = 'b' if self.white_to_move else 'w'
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_column = column + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_column <= 7:
                    end_piece = self.board[end_row][end_column]
                    if end_piece == '--':
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                    elif self.board[end_row][end_column][0] == enemy_color:
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                        break  # no moves behind enemy pieces
                    else:
                        break  # no moves behind our pieces
                else:
                    break  # no moves behind the board

    def get_bishop_moves(self, row: int, column: int, moves: list) -> None:
        directions = ((1, 1), (1, -1), (-1, 1), (-1, -1))
        enemy_color = 'b' if self.white_to_move else 'w'
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_column = column + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_column <= 7:
                    end_piece = self.board[end_row][end_column]
                    if end_piece == '--':
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                    elif self.board[end_row][end_column][0] == enemy_color:
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                        break  # no moves behind enemy pieces
                    else:
                        break  # no moves behind our pieces
                else:
                    break  # no moves behind the board

    def get_knight_moves(self, row: int, column: int, moves: list) -> None:
        directions = ((2, 1), (2, -1), (-2, -1), (-2, 1), (1, 2), (1, -2), (-1, -2), (-1, 2))
        our_color = 'w' if self.white_to_move else 'b'
        for direction in directions:
            end_row = row + direction[0]
            end_column = column + direction[1]
            if 0 <= end_row <= 7 and 0 <= end_column <= 7 and self.board[end_row][end_column][0] != our_color:
                moves.append(Move((row, column), (end_row, end_column), self.board))

    def get_king_moves(self, row: int, column: int, moves: list) -> None:
        directions = ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1))
        enemy_color = 'b' if self.white_to_move else 'w'
        for direction in directions:
            end_row = row + direction[0]
            end_column = column + direction[1]
            if 0 <= end_row <= 7 and 0 <= end_column <= 7:
                if self.board[end_row][end_column] == '--' or self.board[end_row][end_column][0] == enemy_color:
                    moves.append(Move((row, column), (end_row, end_column), self.board))

    def get_queen_moves(self, row: int, column: int, moves: list) -> None:
        self.get_rook_moves(row, column, moves)
        self.get_bishop_moves(row, column, moves)


"""
Moves in the game are Move class objects. Class Move contains methods which provide the chess notation.
"""


class Move:
    rows_to_ranks = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}
    columns_to_ranks = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    def __init__(self, start_square: (int, int), end_square: (int, int), board: list):
        self.start_row = start_square[0]
        self.start_column = start_square[1]
        self.end_row = end_square[0]
        self.end_column = end_square[1]
        self.piece_moved = board[self.start_row][self.start_column]
        self.piece_captured = board[self.end_row][self.end_column]
        self.moveID = self.start_row * 1000 + self.start_column * 100 + self.end_row * 10 + self.end_column
        self.start_square = start_square
        self.end_square = end_square

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def __str__(self):
        if self.piece_moved[1] == 'K' and abs(self.end_column - self.start_column) == 2:
            return 'O-O-O' if self.end_column == 2 else 'O-O'
        return f'{self.piece_moved[1]}{self.get_chess_notation()}'

    def get_chess_notation(self) -> str:
        return self.get_ranks(self.start_row, self.start_column) + ' ' + self.get_ranks(self.end_row, self.end_column)

    def get_ranks(self, row: int, column: int) -> str:
        return self.columns_to_ranks[column] + self.rows_to_ranks[row]
