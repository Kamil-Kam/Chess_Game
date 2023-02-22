import re


class GameState:
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]
        self.white_to_move = True
        self.move_log = []

        self.move_function = {'p': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves,
                              'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}

        self.white_king = (7, 4)
        self.black_king = (0, 4)
        self.checkmate = False
        self.stalemate = False

        self.pre_en_passant_possible_moves = []
        self.en_passant_moves = []
        self.pre_en_passant = False
        self.pre_en_passant_move_end_position = []

        self.black_queen_castling_mark = 0
        self.black_king_castling_mark = 0
        self.white_queen_castling_mark = 0
        self.white_king_castling_mark = 0
        self.any_castling_mark = self.black_queen_castling_mark * self.black_king_castling_mark \
                                 * self.white_queen_castling_mark * self.white_king_castling_mark

        self.black_queen_castling_currently = True
        self.black_king_castling_currently = True
        self.white_queen_castling_currently = True
        self.white_king_castling_currently = True

    def clear_currently_castlings(self):  # make every castling possible after move, then it`s verifying
        self.black_queen_castling_currently = True
        self.black_king_castling_currently = True
        self.white_queen_castling_currently = True
        self.white_king_castling_currently = True

    def are_castlings_possible(self, move: object(), num: int) -> None:
        # add or subtract castlings possibility after each make_move and undo_move
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

    def after_move_on_board(self, move: object()) -> None:  # executed when move on board is made, pawn promotion
        color = 'b' if self.white_to_move else 'w'
        promotion_row = 7 if self.white_to_move else 0

        if move.piece_moved == f'{color}p' and move.end_row == promotion_row:  # run pawn promotion
            piece = self.get_pawn_promotion()
            self.board[promotion_row][move.end_column] = color + piece


    def castling_under_attack(self):  # if between king and rook are figures or those squares are under attack,
        # or king is under attack -> disable castling
        self.clear_currently_castlings()
        white_queen_side = [[7, 2], [7, 3]]
        white_king_side = [[7, 5], [7, 6]]
        black_queen_side = [[0, 2], [0, 3]]
        black_king_side = [[0, 5], [0, 6]]
        self.white_to_move = not self.white_to_move
        opponent_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move

        if not self.in_check():

            for move in opponent_moves:

                if move.end_row == [7] and move.end_column == [4]:
                    self.white_queen_castling_currently = False
                    self.white_king_castling_currently = False

                if self.board[7][1] != '--':
                    self.white_queen_castling_currently = False

                for square in white_queen_side:
                    if self.board[square[0]][square[1]] != '--':
                        self.white_queen_castling_currently = False
                    elif move.end_row == square[0] and move.end_column == square[1]:
                        self.white_queen_castling_currently = False

                for square in white_king_side:
                    if self.board[square[0]][square[1]] != '--':
                        self.white_king_castling_currently = False
                    elif move.end_row == square[0] and move.end_column == square[1]:
                        self.white_king_castling_currently = False

                if move.end_row == 0 and move.end_column == 4:
                    self.black_queen_castling_currently = False
                    self.black_king_castling_currently = False

                if self.board[0][1] != '--':
                    self.black_queen_castling_currently = False

                for square in black_queen_side:
                    if self.board[square[0]][square[1]] != '--':
                        self.black_queen_castling_currently = False
                    elif move.end_row == square[0] and move.end_column == square[1]:
                        self.black_queen_castling_currently = False

                for square in black_king_side:
                    if self.board[square[0]][square[1]] != '--':
                        self.black_king_castling_currently = False
                    elif move.end_row == square[0] and move.end_column == square[1]:
                        self.black_king_castling_currently = False

    def append_castling_moves(self, moves: list) -> None:  # append castling moves to move list
        if self.white_queen_castling_mark == 0 and self.white_queen_castling_currently:
            moves.append(Move((7, 4), (7, 2), self.board))
        if self.white_king_castling_mark == 0 and self.white_king_castling_currently:
            moves.append(Move((7, 4), (7, 6), self.board))
        if self.black_queen_castling_mark == 0 and self.black_queen_castling_currently:
            moves.append(Move((0, 4), (0, 2), self.board))
        if self.black_king_castling_mark == 0 and self.black_king_castling_currently:
            moves.append(Move((0, 4), (0, 6), self.board))

    @staticmethod
    def get_pawn_promotion() -> str:  # allow player to insert figure name when pawn is promoted
        while not re.match(r'^Q|R|B|N$', piece := input('Insert "Q" - Queen, or "R" - Rook, or "B" - Bishop, or "N" - Knight: \n')):
            pass
        return piece

    def append_pre_en_passant_moves(self) -> None:  # creates all possibly pre-en passant moves, run only one time
        row_black, row_white = 1, 6
        for column in range(0, 8):
            self.pre_en_passant_possible_moves.append(Move((row_black, column), (row_black + 2, column), self.board))
            self.pre_en_passant_possible_moves.append(Move((row_white, column), (row_white - 2, column), self.board))

    def is_pre_en_passant(self) -> None:  # if the last move is pre en passant -> allow en_passant moves
        if len(self.move_log) > 0:
            self.pre_en_passant = True if self.move_log[-1] in self.pre_en_passant_possible_moves else False

    def make_move(self, move: object()) -> None:  # updates pieces positions
        self.board[move.start_row][move.start_column] = '--'
        self.board[move.end_row][move.end_column] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        if move.piece_moved == 'wK':
            self.white_king = (move.end_row, move.end_column)
        elif move.piece_moved == 'bK':
            self.black_king = (move.end_row, move.end_column)

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

    def undo_move(self) -> None:  # cancel move, cancel pieces positions
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_column] = move.piece_moved
            self.board[move.end_row][move.end_column] = move.piece_captured
            self.white_to_move = not self.white_to_move
            if move.piece_moved == 'wK':
                self.white_king = (move.start_row, move.start_column)
            elif move.piece_moved == 'bK':
                self.black_king = (move.start_row, move.start_column)

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

    def get_valid_moves(self) -> list:  # add some special moves and delete moves where king is attacked
        moves = self.get_all_possible_moves()

        self.en_passant_moves = []
        self.is_pre_en_passant()
        if self.pre_en_passant:
            self.get_pawn_en_passant_moves(moves)

        self.castling_under_attack()
        if self.any_castling_mark == 0:
            self.append_castling_moves(moves)

        for i in range(len(moves) - 1, -1, -1):
            self.make_move(moves[i])
            if self.in_check():
                moves.remove(moves[i])
            self.undo_move()

        if len(moves) == 0:
            self.white_to_move = not self.white_to_move
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
            self.white_to_move = not self.white_to_move

        return moves

    def get_all_possible_moves(self) -> list:  # make list of all possible moves, does not consider checks
        moves = []  # after each turn clears moves list
        move_color = 'w' if self.white_to_move else 'b'
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                if move_color == self.board[row][column][0]:
                    piece = self.board[row][column][1]
                    self.move_function[piece](row, column, moves)

        return moves

    def in_check(self) -> bool:  # check if king is under attack
        if self.white_to_move:
            return self.king_under_attack(self.black_king[0], self.black_king[1])
        else:
            return self.king_under_attack(self.white_king[0], self.white_king[1])

    def king_under_attack(self, king_row: int, king_column: int) -> bool:  # check if king is under attack
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
                if self.board[end_row][end_column] == '--':
                    moves.append(Move((row, column), (end_row, end_column), self.board))
                elif self.board[end_row][end_column][0] == enemy_color:
                    moves.append(Move((row, column), (end_row, end_column), self.board))

    def get_queen_moves(self, row: int, column: int, moves: list) -> None:
        self.get_rook_moves(row, column, moves)
        self.get_bishop_moves(row, column, moves)


class Move:
    rows_to_ranks = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}
    columns_to_ranks = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    def __init__(self, start_square: [int, int], end_square: [int, int], board: list):
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
        return self.get_ranks(self.start_row, self.start_column) + ' ' + self.get_ranks(self.end_row,
                                                                                        self.end_column)

    def get_ranks(self, row: int, column: int) -> str:
        return self.columns_to_ranks[column] + self.rows_to_ranks[row]

