

def after_move_on_board(self, move: object()) -> None:  # executed when move on board is made, enable pawn promotion
    color = 'b' if self.white_to_move else 'w'
    promotion_row = 7 if self.white_to_move else 0

    if move.piece_moved == f'{color}p' and move.end_row == promotion_row:  # run pawn promotion
        piece = self.get_pawn_promotion()
        self.board[promotion_row][move.end_column] = color + piece



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

            if move.end_row == [7] and move.end_column == [4]:
                self.white_queen_castling_currently = False
                self.white_king_castling_currently = False

            elif self.board[7][1] != '--':
                self.white_queen_castling_currently = False

            # for square in white_queen_side:
            #     if self.board[square[0]][square[1]] != '--' or (move.end_row == square[0] and move.end_column == square[1]):
            #         self.white_queen_castling_currently = False
            #         print(square, self.white_queen_castling_currently)
            #
            # for square in white_king_side:
            #     if self.board[square[0]][square[1]] != '--' or (move.end_row == square[0] and move.end_column == square[1]):
            #         self.white_king_castling_currently = False
            #         print(square, self.white_king_castling_currently)

            if move.end_row == 0 and move.end_column == 4:
                self.black_queen_castling_currently = False
                self.black_king_castling_currently = False

            elif self.board[0][1] != '--':
                self.black_queen_castling_currently = False

            # for square in black_queen_side:
            #     if self.board[square[0]][square[1]] != '--' or (move.end_row == square[0] and move.end_column == square[1]):
            #         self.black_queen_castling_currently = False
            #         print(square, self.black_queen_castling_currently)
            #
            # for square in black_king_side:
            #     if self.board[square[0]][square[1]] != '--' or (move.end_row == square[0] and move.end_column == square[1]):
            #         self.black_king_castling_currently = False
            #         print(square, self.black_queen_castling_currently)

            print(self.black_queen_castling_currently, self.black_king_castling_currently, self.white_queen_castling_currently, self.white_king_castling_currently)



def get_list_of_possible_invalid_move(self) -> list:
    king_position = self.white_king_position if self.white_to_move else self.black_king_position
    row = king_position[0]
    column = king_position[1]
    lists_moves_to_check = [king_position]

    for i in range(-7, 8):
        if 0 <= row + i <= 7:
            lists_moves_to_check.append((row + i, column))
        if 0 <= column + i <= 7:
            lists_moves_to_check.append((row, column + i))
        if 0 <= column + i <= 7 and 0 <= row + i <= 7:
            lists_moves_to_check.append((row + i, column + i))
            lists_moves_to_check.append((row + i, column - i))
            lists_moves_to_check.append((row - i, column + i))
            lists_moves_to_check.append((row - i, column - i))

    return lists_moves_to_check

def get_board_hash(self):
    # Create a FEN string from the current board position
    fen = ""
    empty_count = 0
    for row in self.board:
        for square in row:
            if square == '--':
                empty_count += 1
            else:
                if empty_count > 0:
                    fen += str(empty_count)
                    empty_count = 0
                fen += square
        if empty_count > 0:
            fen += str(empty_count)
            empty_count = 0
        fen += "/"

    # Add side to move, castling rights, and en passant square to the FEN string
    fen += " w " if self.white_to_move else " b "
    fen += "-"  # No castling rights for now
    fen += " -"  # No en passant square for now

    return hash(fen)