import pygame as p
import Chess_Rules_Engine
import Drawing
import Chess_AI_Engine, Chess_AI_Engine_multiprocessing_process, Chess_AI_Engine_multiprocessing_pool
from multiprocessing import Queue, Process
import time

p.init()
p.display.set_caption("Chess v. 0.9")


def main():
    screen = p.display.set_mode((Drawing.OUTER_FRAME_SIZE + Drawing.LOG_PANEL_WIDTH, Drawing.OUTER_FRAME_SIZE))
    clock = p.time.Clock()
    Drawing.load_images()

    cre_gs = Chess_Rules_Engine.GameState()
    cre_gs.append_pre_en_passant_moves()
    valid_moves = cre_gs.get_valid_moves()
    move_made = False
    running = True
    animation = False

    square_selected = ()
    player_clicks = []

    black_AI = True
    white_AI = True
    AI_thinking = False
    AI_process = None
    Drawing.draw_all(screen, cre_gs)
    
    while running:
        AI_turn = (cre_gs.white_to_move and white_AI) or (not cre_gs.white_to_move and black_AI)

        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

            elif event.type == p.MOUSEBUTTONDOWN:  # take position from mouse click
                location = p.mouse.get_pos()
                column = int((location[0] - Drawing.BOARD_SPACE) // Drawing.SQUARE_SIZE)
                row = int((location[1] - Drawing.BOARD_SPACE) // Drawing.SQUARE_SIZE)

                if column > 7:
                    break

                if square_selected == (row, column):  # if 2 x click on the same square -> remove second click
                    # square_selected = (row, column)
                    player_clicks.pop()
                    pass

                if ((cre_gs.board[row][column][0] == 'b' and cre_gs.white_to_move) or (cre_gs.board[row][column][0] == 'w'
                                                                                       and not cre_gs.white_to_move)) and len(player_clicks) == 0:
                    # if first click on wrong color -> pass
                    break

                if len(player_clicks) != 0 and cre_gs.board[square_selected[0]][square_selected[1]][0] == cre_gs.board[row][column][0]:
                    # if second click on the same color -> delete first click
                    player_clicks = []
                    pass

                if cre_gs.board[row][column] == '--' and len(player_clicks) == 0:
                    # if first click  on empty square -> pass
                    pass

                else:
                    square_selected = (row, column)
                    player_clicks.append(square_selected)

                if len(player_clicks) == 2:
                    move = Chess_Rules_Engine.Move(player_clicks[0], player_clicks[1], cre_gs.board)

                    if move in valid_moves:
                        cre_gs.make_move(move)
                        # cre_gs.after_move_on_board(move)
                        move_made = True
                        animation = True

                    square_selected = []  # after move_made clear square selected
                    player_clicks = []  # after move_made clear player clicks

            elif event.type == p.KEYDOWN:

                if event.key == p.K_BACKSPACE:  # cancel move
                    cre_gs.undo_move()
                    move_made = True

                if event.key == p.K_r:  # board reset
                    cre_gs = Chess_Rules_Engine.GameState()
                    valid_moves = cre_gs.get_valid_moves()
                    square_selected = []
                    player_clicks = []
                    move_made = False

                if event.key == p.K_p:  # game pause
                    stop = True
                    Drawing.draw_pause(screen)
                    p.display.update()

                    while stop:
                        for pause_event in p.event.get():
                            clock.tick(Drawing.FPS)

                            if pause_event.type == p.QUIT:
                                running = False
                                stop = False
                                AI_turn = False

                            if pause_event.type == p.KEYDOWN:

                                if pause_event.key == p.K_c:
                                    stop = False
                                    move_made = True
                                    AI_turn = False

                                if pause_event.key == p.K_BACKSPACE:  # cancel move
                                    cre_gs.undo_move()
                                    move_made = True
                                    Drawing.draw_moves_notation_and_log_panel(screen, cre_gs)
                                    Drawing.get_moves_notation()
                                    Drawing.draw_all(screen, cre_gs)
                                    Drawing.highlight_squares(screen, cre_gs, valid_moves, player_clicks)
                                    p.display.update()

        if AI_turn and not cre_gs.checkmate and not cre_gs.stalemate:
            if not AI_thinking:
                start_time = time.time()
                return_queue = Queue()
                AI_thinking_process = Process(target=Chess_AI_Engine.find_best_move, args=(cre_gs, valid_moves, return_queue))
                AI_thinking_process.start()
                AI_thinking = True

            if not AI_thinking_process.is_alive():
                AI_move = return_queue.get()
                cre_gs.make_move(AI_move)
                move_made = True
                animation = True
                AI_thinking = False
                print(time.time() - start_time)

        if move_made:

            if animation:
                Drawing.animate_move(screen, cre_gs.move_log[-1], cre_gs.board)
            if len(cre_gs.move_log) > 0:
                cre_gs.after_move_on_board(cre_gs.move_log[-1])
                Drawing.draw_moves_notation_and_log_panel(screen, cre_gs)
                Drawing.get_moves_notation()

            valid_moves = cre_gs.get_valid_moves()
            move_made = False
            animation = False

        Drawing.draw_all(screen, cre_gs)
        Drawing.highlight_squares(screen, cre_gs, valid_moves, player_clicks)

        if cre_gs.checkmate or cre_gs.stalemate:
            Drawing.draw_ending_statement(screen, cre_gs)

        clock.tick(Drawing.FPS)
        p.display.update()


if __name__ == "__main__":
    main()
