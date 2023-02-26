import random

piece_score = {"K": 500, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
checkmate = 1000
stalemate = 0
DEPTH = 3

def find_best_move(cre_gs: object(), valid_moves: list, queue) -> object():
    # random.shuffle(valid_moves)
    global next_move
    find_nega_max_move_alpha_beta(cre_gs, DEPTH, valid_moves, 1 if cre_gs.white_to_move else -1, -checkmate, checkmate)
    queue.put(next_move)

def get_moves_priority_list(cre_gs, valid_moves):
    # Create a list of moves with their priorities
    moves_with_priorities = []
    for move in valid_moves:
        priority = 0
        if cre_gs.board[move.start_row][move.start_column][1] == 'p':
            # Prioritize pawn moves that promote to a queen
            if (cre_gs.white_to_move and move.end_row == 0) or (not cre_gs.white_to_move and move.end_row == 7):
                priority = 10
            # Prioritize pawn captures
            elif cre_gs.board[move.end_row][move.end_column] != '--':
                priority = 5
        elif cre_gs.board[move.start_row][move.start_column][1] == 'k':
            # Prioritize castling moves
            if abs(move.end_column - move.start_column) > 1:
                priority = 8
        else:
            # Prioritize capturing moves
            if cre_gs.board[move.end_row][move.end_column] != '--':
                captured_piece_value = piece_score[cre_gs.board[move.end_row][move.end_column][1]]
                priority = captured_piece_value - piece_score[cre_gs.board[move.start_row][move.start_column][1]]

        moves_with_priorities.append((move, priority))

    # Sort the moves by priority
    moves_with_priorities.sort(key=lambda x: x[1], reverse=True)
    return moves_with_priorities


def find_nega_max_move_alpha_beta(cre_gs: object(), depth: int, valid_moves: list, turn_multiplier: int, alpha: int, beta: int) -> int:
    global next_move

    if depth == 0:
        return turn_multiplier * score_material(cre_gs)

    moves_priority_list = get_moves_priority_list(cre_gs, valid_moves)

    max_score = -checkmate
    for move, _ in moves_priority_list:
        cre_gs.make_move(move)
        next_moves = cre_gs.get_valid_moves()
        score = -find_nega_max_move_alpha_beta(cre_gs, depth - 1, next_moves, -turn_multiplier, -beta, -alpha)
        cre_gs.undo_move()

        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move

        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break

    return max_score


def score_material(cre_gs: object()) -> int:
    if cre_gs.checkmate:
        if cre_gs.white_to_move:
            return checkmate
        else:
            return -checkmate
    score = 0
    for row in cre_gs.board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]
            elif square[0] == 'b':
                score -= piece_score[square[1]]
    return score
