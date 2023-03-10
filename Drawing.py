"""
Parameters describing board and text,
functions to drawing board, pieces and text,
functions animating moves
"""

from typing import Final
import pygame as p

p.init()

BOARD_WIDTH: Final[int] = 704
BOARD_HEIGHT: Final[int] = 704
INNER_FRAME_SIZE: Final[int] = 710
OUTER_FRAME_SIZE: Final[int] = 740
FRAME_SPACE = ((OUTER_FRAME_SIZE - INNER_FRAME_SIZE) / 2)
BOARD_SPACE = ((OUTER_FRAME_SIZE - BOARD_WIDTH) / 2)
LOG_PANEL_HEIGHT: Final[int] = BOARD_HEIGHT
LOG_PANEL_WIDTH: Final[int] = 160

DIMENSION: Final[int] = 8
SQUARE_SIZE = BOARD_WIDTH // DIMENSION

FPS: Final[int] = 25
IMAGES = {}

FRAME_MARKS_FONT = p.font.SysFont('arial', 15, True, False)
CENTRAL_BOARD_STATEMENT_FONT = p.font.SysFont('arial', 40, True, False)
LOG_PANEL_FONT = p.font.SysFont('arial', 14, False, False)

BRIGHT_SQUARES_COLOR = "antiquewhite"
DARK_SQUARES_COLOR = "burlywood3"
OUTER_FRAME_COLOR = BRIGHT_SQUARES_COLOR
INNER_FRAME_COLOR = 'black'
FRAME_MARKS_COLOR = 'burlywood4'
LOG_PANEL_COLOR = 'black'
LOG_PANEL_FONT_COLOR = 'white'
ENDING_STATEMENT_FONT_SHADOW_COLOR = "antiquewhite"
ENDING_STATEMENT_FONT_COLOR = 'black'
MARKED_SQUARE_COLOR = 'green'
POSSIBLE_MOVES_SQUARES_COLOR = 'yellow'
ENEMY_PIECE_SQUARE_COLOR = 'red'
LAST_MOVE_SQUARES_COLOR = 'steelblue3'

def draw_starting_screen(screen) -> None:
    starting_screen = p.transform.smoothscale(p.image.load("images/chess_image.jpg"), (OUTER_FRAME_SIZE + LOG_PANEL_WIDTH, OUTER_FRAME_SIZE))
    screen.blit(starting_screen, (0, 0))


def load_images() -> None:  # load images to the IMAGES dictionary
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wp']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"images/{piece}.png"), (SQUARE_SIZE, SQUARE_SIZE))


def draw_all(screen, cre_gs: object(), valid_moves, player_clicks) -> None:  # run some functions drawing surround, board and pieces
    draw_moves_notation_and_log_panel(screen, cre_gs)
    draw_surround(screen)
    draw_board(screen)
    draw_pieces(screen, cre_gs.board)
    highlight_squares(screen, cre_gs, valid_moves, player_clicks)


def draw_board(screen) -> None:  # draw color on each square
    global colors
    colors = [p.Color(BRIGHT_SQUARES_COLOR), p.Color(DARK_SQUARES_COLOR)]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE + BOARD_SPACE, row * SQUARE_SIZE + BOARD_SPACE, SQUARE_SIZE, SQUARE_SIZE))


def draw_surround(screen) -> None:  # draw surrounds and marks around chess board
    font = FRAME_MARKS_FONT
    p.draw.rect(screen, OUTER_FRAME_COLOR, p.Rect(0, 0, OUTER_FRAME_SIZE, OUTER_FRAME_SIZE))
    p.draw.rect(screen, INNER_FRAME_COLOR, p.Rect(FRAME_SPACE, FRAME_SPACE, INNER_FRAME_SIZE, INNER_FRAME_SIZE))

    LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    X = FRAME_SPACE + SQUARE_SIZE // 2
    Y = FRAME_SPACE + SQUARE_SIZE // 2

    for num in range(DIMENSION):
        frame_marks_rect = p.Rect(0, 0, INNER_FRAME_SIZE, INNER_FRAME_SIZE)

        text_object = font.render(str(LETTERS[num]), True, p.Color(FRAME_MARKS_COLOR))

        for Y_coordinate in [0, INNER_FRAME_SIZE + FRAME_SPACE]:
            text_location = frame_marks_rect.move(X, Y_coordinate)
            screen.blit(text_object, text_location)

        text_object = font.render(str(8 - num), True, p.Color(FRAME_MARKS_COLOR))

        for X_coordinate in [3, 3 + INNER_FRAME_SIZE + FRAME_SPACE]:
            text_location = frame_marks_rect.move(X_coordinate, Y - 4)
            screen.blit(text_object, text_location)

        X += SQUARE_SIZE
        Y += SQUARE_SIZE


def draw_pieces(screen, board: list) -> None:  # draw pieces on the board
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]

            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(column * SQUARE_SIZE + BOARD_SPACE, row * SQUARE_SIZE + BOARD_SPACE, SQUARE_SIZE, SQUARE_SIZE))


def draw_moves_notation_and_log_panel(screen, cre_gs: object()) -> None:  # draw log panel ont the right side and chess notation on the log panel
    global moves_notation
    moves_notation = ''

    font = LOG_PANEL_FONT
    move_log = cre_gs.move_log
    Y = 0
    turn_num = 1

    lines_number = (len(move_log) // 2) + 1
    line_height = font.get_height()
    text_size_rectangle = (LOG_PANEL_WIDTH, lines_number * line_height)
    text_surface = p.Surface(text_size_rectangle, p.SRCALPHA)

    for move_num in range(len(move_log)):
        log_text = ''
        X = 0

        if move_num == 0:
            log_text += f'{turn_num}. {move_log[move_num]}'
            turn_num += 1
        elif move_num > 0 and move_num % 2 == 0:
            Y += text_object.get_height()
            log_text += f'{turn_num}. {move_log[move_num]}'
            turn_num += 1
            moves_notation += '   '
        else:
            X = text_object.get_width()
            log_text += f'   {move_log[move_num]}'

        if move_num == 0:
            text_location = (0, 0)
        elif move_num > 0 and move_num % 2 == 0:
            text_location = (0, Y)
        else:
            text_location = (X, Y)

        text_object = font.render(str(log_text), True, p.Color(LOG_PANEL_FONT_COLOR))
        text_surface.blit(text_object, text_location)
        moves_notation += log_text

    log_panel_rect = p.Rect(OUTER_FRAME_SIZE, 0, LOG_PANEL_WIDTH, LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color(LOG_PANEL_COLOR), log_panel_rect)
    height_difference = text_surface.get_height() - LOG_PANEL_HEIGHT
    scroll = 1.0

    if height_difference > 0:
        text_off_screen_Y = int(height_difference * scroll)
        subsurface_rect = p.Rect(0, text_off_screen_Y, LOG_PANEL_WIDTH, LOG_PANEL_HEIGHT)
        subsurface_text_surface = text_surface.subsurface(subsurface_rect)
        screen.blit(subsurface_text_surface, log_panel_rect)

    else:
        screen.blit(text_surface, log_panel_rect)


def get_moves_notation() -> None:  # print all moves notation
    global moves_notation
    print(moves_notation)


def draw_ending_statement(screen, cre_gs: object()) -> None:  # draw a statement if game is over
    font = CENTRAL_BOARD_STATEMENT_FONT

    text = ("GAME OVER BLACK WINS" if cre_gs.white_to_move else "GAME OVER WHITE WINS") if cre_gs.checkmate else "STALEMATE"
    text_object = font.render(text, False, p.Color(ENDING_STATEMENT_FONT_SHADOW_COLOR))
    text_location = p.Rect(0, 0, OUTER_FRAME_SIZE, OUTER_FRAME_SIZE).move(OUTER_FRAME_SIZE / 2 - text_object.get_width() / 2,
                                                                          OUTER_FRAME_SIZE / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, p.Color(ENDING_STATEMENT_FONT_COLOR))
    screen.blit(text_object, text_location.move(2, 2))


def draw_pause(screen) -> None:   # draw a pause statement if game is stopped
    font = CENTRAL_BOARD_STATEMENT_FONT

    text_list = ['PAUSE', 'press "c" to continue']
    text_height = font.get_height() // 2

    for text in text_list:
        text_object = font.render(text, False, p.Color(ENDING_STATEMENT_FONT_SHADOW_COLOR))
        text_location = p.Rect(0, 0, OUTER_FRAME_SIZE, OUTER_FRAME_SIZE).move(OUTER_FRAME_SIZE / 2 - text_object.get_width() / 2,
                                                                              OUTER_FRAME_SIZE / 2 - text_object.get_height() / 2 - text_height)
        screen.blit(text_object, text_location)
        text_object = font.render(text, False, p.Color(ENDING_STATEMENT_FONT_COLOR))
        screen.blit(text_object, text_location.move(2, 2))
        text_height = -text_height


def highlight_squares(screen, cre_gs: object(), valid_moves: list, selected_square: list) -> None:  # highlight possible moves squares
    if len(selected_square) == 1:
        row, column = selected_square[0]

        if cre_gs.board[row][column][0] == ('w' if cre_gs.white_to_move else 'b'):
            square = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            square.set_alpha(50)
            square.fill(p.Color(MARKED_SQUARE_COLOR))
            screen.blit(square, (column * SQUARE_SIZE + BOARD_SPACE, row * SQUARE_SIZE + BOARD_SPACE))

            for move in valid_moves:
                if move.start_row == row and move.start_column == column:

                    if cre_gs.board[move.end_row][move.end_column][0] == ('b' if cre_gs.white_to_move else 'w'):
                        square.fill(p.Color(ENEMY_PIECE_SQUARE_COLOR))
                        screen.blit(square, (move.end_column * SQUARE_SIZE + BOARD_SPACE, move.end_row * SQUARE_SIZE + BOARD_SPACE))
                    else:
                        square.fill(p.Color(POSSIBLE_MOVES_SQUARES_COLOR))
                        screen.blit(square, (move.end_column * SQUARE_SIZE + BOARD_SPACE, move.end_row * SQUARE_SIZE + BOARD_SPACE))

    if len(cre_gs.move_log) > 0:
        square = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
        square.set_alpha(90)
        square.fill(p.Color(LAST_MOVE_SQUARES_COLOR))
        screen.blit(square, (cre_gs.move_log[-1].start_column * SQUARE_SIZE + BOARD_SPACE,
                             cre_gs.move_log[-1].start_row * SQUARE_SIZE + BOARD_SPACE))
        screen.blit(square, (cre_gs.move_log[-1].end_column * SQUARE_SIZE + BOARD_SPACE,
                             cre_gs.move_log[-1].end_row * SQUARE_SIZE + BOARD_SPACE))

    draw_pieces(screen, cre_gs.board)


def animate_move(screen, move: object(), board: list) -> None:  # animate moves
    global colors
    row_difference = move.end_row - move.start_row
    column_difference = move.end_column - move.start_column
    frames_count = int(1.2 * FPS + ((abs(row_difference) + abs(column_difference)) * 2))

    for frame in range(frames_count + 1):
        row = (move.start_row + row_difference * frame / frames_count)
        column = (move.start_column + column_difference * frame / frames_count)
        draw_board(screen)
        draw_pieces(screen, board)
        color = colors[(move.end_row + move.end_column) % 2]
        end_square = p.Rect(move.end_column * SQUARE_SIZE + BOARD_SPACE, move.end_row * SQUARE_SIZE + BOARD_SPACE, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(screen, color, end_square)

        if move.piece_captured != '--':
            screen.blit(IMAGES[move.piece_captured], end_square)

        screen.blit(IMAGES[move.piece_moved], p.Rect(column * SQUARE_SIZE + BOARD_SPACE, row * SQUARE_SIZE + BOARD_SPACE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.update()
