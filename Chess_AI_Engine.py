import random

piece_score = {"K": 500, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
checkmate = 1000
stalemate = 0
DEPTH = 2


def get_best_move(cre_gs: object(), valid_moves: list) -> object():
    opponent_min_max_score = checkmate
    turn_multiplier = 1 if cre_gs.white_to_move else -1
    AI_best_move = None
    random.shuffle(valid_moves)

    for AI_move in valid_moves:
        cre_gs.make_move(AI_move)
        opponents_moves = cre_gs.get_valid_moves()
        opponent_max_score = -checkmate

        for opponent_move in opponents_moves:
            cre_gs.make_move(opponent_move)
            if cre_gs.checkmate:
                score = -turn_multiplier * checkmate
            elif cre_gs.stalemate:
                score = stalemate
            else:
                score = -turn_multiplier * score_material(cre_gs)

            if score > opponent_max_score:
                opponent_max_score = score
            cre_gs.undo_move()

        if opponent_min_max_score > opponent_max_score:
            opponent_min_max_score = opponent_max_score
            AI_best_move = AI_move
        cre_gs.undo_move()

    return AI_best_move


def find_best_move(cre_gs: object(), valid_moves: list) -> object():
    random.shuffle(valid_moves)
    global next_move
    find_nega_max_move_alpha_beta(cre_gs, DEPTH, valid_moves, 1 if cre_gs.white_to_move else -1, -checkmate, checkmate)
    return next_move


def find_min_max_move(cre_gs: object(), depth: int, valid_moves: list) -> int:
    global next_move
    if depth == 0:
        return score_material(cre_gs)

    if cre_gs.white_to_move:
        max_score = -checkmate
        for move in valid_moves:
            cre_gs.make_move(move)
            next_moves = cre_gs.get_valid_moves()
            score = find_min_max_move(cre_gs, depth - 1, next_moves)

            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    next_move = move
            cre_gs.undo_move()
        return max_score

    else:
        min_score = checkmate
        for move in valid_moves:
            cre_gs.make_move(move)
            next_moves = cre_gs.get_valid_moves()
            score = find_min_max_move(cre_gs, depth - 1, next_moves)

            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            cre_gs.undo_move()
        return min_score


def find_nega_max_move(cre_gs: object(), depth: int, valid_moves: list, turn_multiplier: int) -> int:
    global next_move
    if depth == 0:
        return turn_multiplier * score_material(cre_gs)

    max_score = -checkmate
    for move in valid_moves:
        cre_gs.make_move(move)
        next_moves = cre_gs.get_valid_moves()
        score = find_nega_max_move(cre_gs, depth - 1, next_moves, -turn_multiplier)

        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        cre_gs.undo_move()
    return max_score


def find_nega_max_move_alpha_beta(cre_gs: object(), depth: int, valid_moves: list, turn_multiplier: int, alpha: int,
                                  beta: int) -> int:
    global next_move
    if depth == 0:
        return turn_multiplier * score_material(cre_gs)

    max_score = -checkmate
    for move in valid_moves:
        cre_gs.make_move(move)
        next_moves = cre_gs.get_valid_moves()
        score = -find_nega_max_move_alpha_beta(cre_gs, depth - 1, next_moves, -turn_multiplier, -beta, -alpha)

        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        cre_gs.undo_move()
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
