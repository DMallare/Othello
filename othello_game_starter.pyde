from board import Board
from disk import Disk
from game_controller import GameController

SIZE = 8
WINDOW_SIZE = 800
DARK_GREEN = (0, 0.4, 0)
board = Board(WINDOW_SIZE, SIZE)
game_controller = GameController(board)


def setup():
    size(WINDOW_SIZE, WINDOW_SIZE)
    colorMode(RGB, 1)
    game_controller.start_game()


def draw():
    background(*DARK_GREEN)
    board.display()
    game_controller.display_message()


def mousePressed():
    if mousePressed:
        game_controller.mouse_control(mouseX, mouseY)
