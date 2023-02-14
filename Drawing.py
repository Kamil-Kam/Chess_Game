"""
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Functions to drawing board and pieces, and to drawing text,
parameters describing board and text,
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
LOG_PANEL_WIDTH: Final[int] = 120

DIMENSION: Final[int] = 8
SQUARE_SIZE = BOARD_WIDTH // DIMENSION

FPS: Final[int] = 25
IMAGES = {}

FRAME_MARKS_FONT = p.font.SysFont('arial', 15, True, False)
END_STATEMENT_FONT = p.font.SysFont('arial', 35, True, False)
LOG_PANEL_FONT = p.font.SysFont('arial', 12, False, False)

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

"""
draw images on the board
"""


def load_images() -> None:
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wp']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"images/{piece}.png"), (SQUARE_SIZE, SQUARE_SIZE))


"""
run some functions drawing screen, frame, board and log_panel
"""


def draw_all(screen, cre_gs: object()) -> None:
    draw_surround(screen)
    draw_board(screen)
    draw_pieces(screen, cre_gs.board)
    draw_moves_notation_on_log_panel(screen, cre_gs)


"""
draw color on each square
"""


def draw_board(screen) -> None:
    global colors
    colors = [p.Color(BRIGHT_SQUARES_COLOR), p.Color(DARK_SQUARES_COLOR)]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE + BOARD_SPACE, row * SQUARE_SIZE + BOARD_SPACE, SQUARE_SIZE, SQUARE_SIZE))


"""
draw surrounds and marks around chess board
"""


def draw_surround(screen) -> None:
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


"""
draw pieces on the board
"""


def draw_pieces(screen, board: list) -> None:
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]

            if piece != "--":
                screen.blit(IMAGES[piece],
                            p.Rect(column * SQUARE_SIZE + BOARD_SPACE, row * SQUARE_SIZE + BOARD_SPACE, SQUARE_SIZE, SQUARE_SIZE))


"""
draw log panel at the right side and chess notation on log panel
"""


def draw_moves_notation_on_log_panel(screen, cre_gs: object()) -> None:
    global moves_notation
    moves_notation = ''

    font = LOG_PANEL_FONT
    log_panel_rect = p.Rect(OUTER_FRAME_SIZE, 0, LOG_PANEL_WIDTH, LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color(LOG_PANEL_COLOR), log_panel_rect)
    move_log = cre_gs.move_log
    Y = 0
    turn_num = 1

    for num in range(len(move_log)):
        log_text = ''
        X = 0

        if num == 0:
            log_text += f'{turn_num}. {move_log[num]}'
            turn_num += 1
        elif num > 0 and num % 2 == 0:
            Y += text_object.get_height()
            log_text += f'{turn_num}. {move_log[num]}'
            turn_num += 1
            moves_notation += '   '
        else:
            X = text_object.get_width()
            log_text += f'   {move_log[num]}'

        if num == 0:
            text_location = log_panel_rect.move(0, 0)
        elif num > 0 and num % 2 == 0:
            text_location = log_panel_rect.move(0, Y)
        else:
            text_location = log_panel_rect.move(X, Y)

        text_object = font.render(str(log_text), True, p.Color(LOG_PANEL_FONT_COLOR))
        screen.blit(text_object, text_location)
        moves_notation += log_text


"""
get all moves notation
"""


def get_moves_notation():
    global moves_notation
    print(moves_notation)



"""
draw a statement if game is over
"""


def draw_ending_statement(screen, cre_gs: object()) -> None:
    font = END_STATEMENT_FONT

    text = ("GAME OVER BLACK WINS" if cre_gs.white_to_move else "GAME OVER WHITE WINS") if cre_gs.checkmate else "STALEMATE"
    text_object = font.render(text, False, p.Color(ENDING_STATEMENT_FONT_SHADOW_COLOR))
    text_location = p.Rect(0, 0, OUTER_FRAME_SIZE, OUTER_FRAME_SIZE).move(OUTER_FRAME_SIZE / 2 - text_object.get_width() / 2, OUTER_FRAME_SIZE / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, p.Color(ENDING_STATEMENT_FONT_COLOR))
    screen.blit(text_object, text_location.move(2, 2))


"""
highlight possible moves squares
"""


def highlight_squares(screen, cre_gs: object(), valid_moves: list, selected_square: list) -> None:
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


"""
animating moves
"""


def animate_move(screen, move: object(), board: list) -> None:
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
