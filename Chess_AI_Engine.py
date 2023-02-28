"""
Parameters and functions responsible for finding best move by AI.
"""

import random

piece_score = {"K": 500, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
checkmate = 1000
stalemate = 0
DEPTH = 3

knight_scores = [[0.0, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.0],
                 [0.1, 0.2, 0.3, 0.3, 0.3, 0.3, 0.2, 0.1],
                 [0.1, 0.3, 0.4, 0.4, 0.4, 0.4, 0.3, 0.1],
                 [0.1, 0.3, 0.4, 0.4, 0.4, 0.4, 0.3, 0.1],
                 [0.1, 0.3, 0.4, 0.4, 0.4, 0.4, 0.3, 0.1],
                 [0.1, 0.3, 0.4, 0.4, 0.4, 0.4, 0.3, 0.1],
                 [0.1, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.1],
                 [0.0, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.0]]

bishop_scores = [[0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.3, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.3],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

rook_scores = [[0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
               [0.5, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.5],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
               [0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2]]

queen_scores = [[0.2, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.2],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.1, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.1]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.6, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.6],
               [0.4, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.4],
               [0.2, 0.2, 0.3, 0.4, 0.4, 0.3, 0.2, 0.2],
               [0.1, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.1],
               [0.1, 0.1, 0.1, 0.2, 0.2, 0.1, 0.1, 0.1],
               [0.1, 0.2, 0.2, 0.1, 0.1, 0.2, 0.2, 0.1],
               [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

king_scores = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
               [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
               [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
               [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
               [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
               [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
               [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
               [0.0, 0.4, 0.4, 0.0, 0.1, 0.0, 0.4, 0.0]]

piece_position_scores = {"wN": knight_scores, "bN": knight_scores[::-1], "wB": bishop_scores, "bB": bishop_scores[::-1], "wQ": queen_scores,
                         "bQ": queen_scores[::-1], "wR": rook_scores, "bR": rook_scores[::-1], "wp": pawn_scores, "bp": pawn_scores[::-1],
                         "wK": king_scores, "bK": king_scores[::-1]}


def find_best_move(cre_gs: object(), valid_moves: list, queue) -> object():
    random.shuffle(valid_moves)
    global next_move
    find_nega_max_move_alpha_beta(cre_gs, DEPTH, valid_moves, 1 if cre_gs.white_to_move else -1, -checkmate, checkmate)
    queue.put(next_move)


def find_nega_max_move_alpha_beta(cre_gs: object(), depth: int, valid_moves: list, turn_multiplier: int, alpha: int, beta: int) -> int:
    global next_move
    if depth == 0:
        return turn_multiplier * score_material(cre_gs)

    moves_priority_list = get_moves_priority_list(cre_gs, valid_moves)
    max_score = -checkmate

    for move, _ in moves_priority_list:
        cre_gs.make_move(move)
        next_moves = cre_gs.get_valid_moves()
        random.shuffle(next_moves)
        score = -find_nega_max_move_alpha_beta(cre_gs, depth - 1, next_moves, -turn_multiplier, -beta, -alpha)
        cre_gs.undo_move()

        if score >= max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move

        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break

    return max_score


def get_moves_priority_list(cre_gs: object(), valid_moves: list) -> list:  # Create a list of moves with their priorities
    moves_with_priorities = []
    for move in valid_moves:
        priority = 0

        if cre_gs.board[move.start_row][move.start_column][1] == 'K':  # Prioritize King moves
            priority = 10
        elif cre_gs.board[move.start_row][move.start_column][1] == 'Q':  # Prioritize Queen moves
            priority = 8
        elif cre_gs.board[move.start_row][move.start_column][1] == 'p':  # Prioritize pawn moves that may promote to a queen
            if (cre_gs.white_to_move and move.end_row == 0) or (not cre_gs.white_to_move and move.end_row == 7):
                priority = 10

        if cre_gs.board[move.end_row][move.end_column] != '--':  # Prioritize captures
            captured_piece_value = piece_score[cre_gs.board[move.end_row][move.end_column][1]]
            priority = captured_piece_value + 2

        moves_with_priorities.append((move, priority))

    moves_with_priorities.sort(key=lambda x: x[1], reverse=True)  # Sort the moves by priority
    return moves_with_priorities


def score_material(cre_gs: object()) -> int:
    if cre_gs.checkmate:
        if cre_gs.white_to_move:
            return checkmate
        else:
            return -checkmate
    elif cre_gs.stalemate:
        return 0

    score = 0
    for row in range(len(cre_gs.board)):
        for column in range(len(cre_gs.board[row])):
            piece = cre_gs.board[row][column]
            if piece != "--":
                piece_multiplier = 1 if piece[0] == 'w' else -1
                score += piece_multiplier * piece_score[piece[1]]  # count all pieces values on the board
                score += piece_multiplier * piece_position_scores[piece][row][column]  # add values for good positions

    return score
