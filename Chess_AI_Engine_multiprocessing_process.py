import random
from multiprocessing import Queue, Process

piece_score = {"K": 500, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
checkmate = 1000
stalemate = 0
DEPTH = 3


def find_best_move(cre_gs: object(), valid_moves: list, queue) -> object():
    # random.shuffle(valid_moves)
    global next_move

    process_1_moves = valid_moves[0: len(valid_moves) // 2]
    process_2_moves = valid_moves[len(valid_moves) // 2::]
    return_queue_1 = Queue()
    return_queue_2 = Queue()

    process_1 = Process(target=find_best_move_process, args=(cre_gs, process_1_moves, return_queue_1))
    process_2 = Process(target=find_best_move_process, args=(cre_gs, process_2_moves, return_queue_2))

    process_1.start()
    process_2.start()
    process_1.join()
    process_2.join()

    move_1 = return_queue_1.get()
    move_2 = return_queue_2.get()

    if not process_1.is_alive() and not process_2.is_alive():
        find_nega_max_move_alpha_beta(cre_gs, DEPTH, [move_1, move_2], 1 if cre_gs.white_to_move else -1, -checkmate, checkmate)
        queue.put(next_move)

def find_best_move_process(cre_gs: object(), valid_moves: list, queue) -> object():
    global next_move
    find_nega_max_move_alpha_beta(cre_gs, DEPTH, valid_moves, 1 if cre_gs.white_to_move else -1, -checkmate, checkmate)
    queue.put(next_move)

def find_nega_max_move_alpha_beta(cre_gs: object(), depth: int, valid_moves: list, turn_multiplier: int, alpha: int, beta: int) -> int:
    global next_move
    if depth == 0:
        return turn_multiplier * score_material(cre_gs)

    max_score = -checkmate
    for move in valid_moves:
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