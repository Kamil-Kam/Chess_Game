import random
import multiprocessing
from functools import partial

piece_score = {"K": 500, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
checkmate = 1000
stalemate = 0
DEPTH = 3


def find_best_move(cre_gs, valid_moves, queue):
    global next_move
    # random.shuffle(valid_moves)

    # Define a partial function with some arguments pre-filled
    partial_func = partial(
        find_nega_max_move_alpha_beta,
        cre_gs=cre_gs,
        depth=DEPTH,
        turn_multiplier=1 if cre_gs.white_to_move else -1,
        alpha=-checkmate,
        beta=checkmate
    )

    # Split valid_moves into chunks for parallel processing
    print(multiprocessing.cpu_count() // 2)
    chunk_size = len(valid_moves) // (multiprocessing.cpu_count() // 2) + 1
    chunks = [valid_moves[i:i+chunk_size] for i in range(0, len(valid_moves), chunk_size)]

    # Use pool.map to run the function in parallel on each chunk of valid_moves
    with multiprocessing.Pool() as pool:
        results = pool.map(partial_func, chunks)

    # Find the highest-scoring move among the results and add it to the queue
    max_score = -checkmate
    for score, move in results:
        if score > max_score:
            max_score = score
            next_move = move
    queue.put(next_move)


def find_nega_max_move_alpha_beta(valid_moves, cre_gs=None, depth=None, turn_multiplier=None, alpha=None, beta=None):
    if depth == 0:
        return turn_multiplier * score_material(cre_gs), None

    max_score = -checkmate
    best_move = None
    for move in valid_moves:
        cre_gs.make_move(move)
        next_moves = cre_gs.get_valid_moves()
        score, _ = find_nega_max_move_alpha_beta(
            valid_moves=next_moves,
            cre_gs=cre_gs,
            depth=depth-1,
            turn_multiplier=-turn_multiplier,
            alpha=-beta,
            beta=-alpha
        )
        score = -score
        cre_gs.undo_move()

        if score > max_score:
            max_score = score
            best_move = move

        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break

    return max_score, best_move

def score_material(cre_gs):
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