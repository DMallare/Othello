from board import Board
from game_controller import GameController
from player import Player
from opponent import Opponent
import re


WINDOW_SIZE = 800
SIZE = 4


def test_constructor():
    board = Board(WINDOW_SIZE, SIZE)
    gc = GameController(board)
    assert gc.WINDOW_SIZE == 800
    assert gc.SIZE == 4
    assert gc.TILE_SPACING == 200
    assert type(gc.human) is Player
    assert type(gc.computer) is Opponent
    assert gc.num_times_no_legal_moves == 0
    assert gc.MESSAGE_DISPLAY_LENGTH == 60
    assert gc.TURN_DISPLAY_TIMER == 60
    assert gc.NO_LEGAL_MOVES_DISPLAY_TIMER == -1
    assert gc.ASK_FOR_INFO_TIMER == -1
    assert gc.NUM_OF_NO_LEGAL_MOVES_LEFT_TO_END_GAME == 2
    assert gc.game_over is False
    assert gc.need_information is False


def test_set_turn():
    """
    Tests the set_turn() method of the GameController class
    """
    board = Board(WINDOW_SIZE, SIZE)
    gc = GameController(board)
    gc.set_turn()
    assert gc.human.turn is False
    gc.set_turn()
    assert gc.human.turn is True


def test_start_game():
    """
    Tests the start_game() method of the GameController class
    """
    board = Board(WINDOW_SIZE, SIZE)
    gc = GameController(board)
    gc.TURN_DISPLAY_TIMER = -1
    gc.start_game()
    assert len(gc.human.legal_moves.keys()) == 4
    assert len(gc.computer.legal_moves.keys()) == 0
    legal_move_disk_count = 0
    for row in range(SIZE):
        for col in range(SIZE):
            if board.disks[row][col].color == -0.5:
                legal_move_disk_count += 1
    assert legal_move_disk_count == 4


def test_prepare_for_turn():
    """
    Tests the prepare_for_turn() method of the GameController class
    """
    board = Board(WINDOW_SIZE, SIZE)
    gc = GameController(board)
    legal_moves_left = gc.prepare_for_turn(gc.human)
    assert len(gc.human.legal_moves.keys()) == 4
    assert len(gc.computer.legal_moves.keys()) == 0
    assert legal_moves_left is True


def test_start_turn():
    """
    Tests the start_turn() method of the GameController class
    """
    board = Board(WINDOW_SIZE, SIZE)
    gc = GameController(board)
    gc.human.legal_moves = {(0, 1): {(0, 1), (0, 2), (0, 3)},
                            (1, 0): {(1, 0), (2, 1)}}
    gc.start_turn()
    assert gc.num_times_no_legal_moves == 0
    assert gc.TURN_DISPLAY_TIMER == 60
    assert board.disks[0][1].color == -0.5
    assert board.disks[1][0].color == -0.5

    # Test to ensure no disk outlines for suggested moves are
    # displayed when there are no legal moves.
    board = Board(WINDOW_SIZE, SIZE)
    gc = GameController(board)
    gc.human.legal_moves = {}
    gc.human.turn = True
    gc.start_turn()
    suggested_moves = 0
    for row in range(gc.board.SIZE):
        for col in range(gc.board.SIZE):
            if gc.board.disks[row][col].color == -0.5:
                suggested_moves += 1
    assert suggested_moves == 0

    # Test to ensure no disk outlines for suggested moves are
    # displayed when it is not the human player's turn.
    board = Board(WINDOW_SIZE, SIZE)
    gc = GameController(board)
    gc.human.legal_moves = {(0, 1): {(0, 1), (0, 2), (0, 3)},
                            (1, 0): {(1, 0), (2, 1)}}
    gc.human.turn = False
    gc.start_turn()
    suggested_moves = 0
    for row in range(gc.board.SIZE):
        for col in range(gc.board.SIZE):
            if gc.board.disks[row][col].color == -0.5:
                suggested_moves += 1
    assert suggested_moves == 0


def test_computer_take_turn():
    """
    Tests the computer_take_turn() method of the GameController class
    """
    WHITE = 1
    board = Board(WINDOW_SIZE, SIZE)
    gc = GameController(board)
    gc.computer.build_legal_moves()
    gc.computer_take_turn()
    num_computer_disks = 0
    for row in range(SIZE):
        for col in range(SIZE):
            if board.disks[row][col].color == WHITE:
                num_computer_disks += 1
    assert num_computer_disks == 4

    # When computer has no legal moves to make, check that
    # a move is not made
    board = Board(WINDOW_SIZE, SIZE)
    gc = GameController(board)
    gc.computer.legal_moves = {}
    gc.computer_take_turn()
    num_computer_disks = 0
    for row in range(SIZE):
        for col in range(SIZE):
            if board.disks[row][col].color == WHITE:
                num_computer_disks += 1
    # Only the white disks placed at the beginning of the game
    # should be on the board.
    assert num_computer_disks == 2


def test_no_legal_moves_available():
    """
    Tests the no_legal_moves_available() method of the GameController class
    """
    board = Board(WINDOW_SIZE, SIZE)
    gc = GameController(board)
    gc.num_times_no_legal_moves = 1
    gc.no_legal_moves_available()
    assert gc.ASK_FOR_INFO_TIMER == -1
    assert gc.game_over is False

    gc.num_times_no_legal_moves = 2
    gc.no_legal_moves_available()
    assert gc.ASK_FOR_INFO_TIMER == 60
    assert gc.game_over is True


def test_record_results():
    """
    Tests the record_results() method of the GameController class
    """
    board = Board(WINDOW_SIZE, SIZE)
    gc = GameController(board)
    # Add a high score
    gc.human.score = 100
    gc.record_results("Sakura")
    with open("scores.txt", "r") as f:
        first_line = f.readline()
    assert first_line == "Sakura 100\n"

    # Add a low score
    gc.human.score = -100
    gc.record_results("Naruto")
    with open("scores.txt", "r") as f:
        contents = f.read().split("\n")
    assert contents[-2] == "Naruto -100"

    # Add a typical score for a size 4 board
    gc.human.score = 11
    gc.record_results("Tsunade")
    with open("scores.txt", "r") as f:
        contents = f.read().split("\n")
    assert contents[-2] == "Tsunade 11"


def test_mouse_control():
    """
    Tests the mouse_control() method of the GameController class
    """
    BLACK = 0
    board = Board(WINDOW_SIZE, SIZE)
    gc = GameController(board)
    gc.human.legal_moves = {(0, 1): {(0, 1), (0, 2), (0, 3)},
                            (1, 0): {(1, 0), (2, 1)}}
    gc.mouse_control(225, 50)
    assert gc.board.disks[0][1].color == BLACK
    assert gc.board.disks[0][2].color == BLACK
    assert gc.board.disks[0][3].color == BLACK

    # Test if the game responds correctly when a player clicks
    # at a tile border
    gc.human.turn = True
    gc.human.legal_moves = {(2, 1): {(2, 1), (2, 2), (2, 3)},
                            (1, 2): {(1, 2), (1, 3)}}
    gc.mouse_control(200, 400)
    assert gc.board.disks[2][1].color == BLACK
    assert gc.board.disks[2][2].color == BLACK
    assert gc.board.disks[2][3].color == BLACK


def test_update():
    """ Tests the update() method fot the GameController class"""
    board = Board(WINDOW_SIZE, SIZE)
    gc = GameController(board)
    # Check method works correctly when game board is not full
    gc.human.turn = False
    gc.update()
    assert gc.human.turn is True
    assert len(gc.human.legal_moves.keys()) > 0

    gc.human.turn = True
    gc.update()
    assert gc.human.turn is False
    assert len(gc.computer.legal_moves.keys()) > 0

    # Check method works correctly when board is not full and
    # there are no legal moves left for the current player
    for row in range(SIZE):
        for col in range(SIZE):
            if row <= SIZE/2:
                gc.board.disks[row][col].color = 0
    gc.update()
    assert gc.num_times_no_legal_moves == 1
    assert gc.NO_LEGAL_MOVES_DISPLAY_TIMER == 60

    # Check method works correctly when game board is full
    for row in range(SIZE):
        for col in range(SIZE):
            gc.board.disks[row][col].color = 0
    gc.update()
    assert gc.ASK_FOR_INFO_TIMER == 60
    assert gc.game_over is True


def test_display_no_legal_moves_available():
    """
    Tests the display_no_legal_moves_available() method
    of the GameController class. Only tests the portion
    of the method that does not include Processing
    display functions.
    """
    board = Board(WINDOW_SIZE, SIZE)
    gc = GameController(board)
    gc.NO_LEGAL_MOVES_DISPLAY_TIMER == 0
    gc.display_no_legal_moves_available()
    assert gc.NO_LEGAL_MOVES_DISPLAY_TIMER == -1


def test_display_turn():
    """
    Tests the display_turn() method of the GameController class.
    Only tests the portion of the method that does not
    include Processing display functions.
    """
    board = Board(WINDOW_SIZE, SIZE)
    gc = GameController(board)
    gc.TURN_DISPLAY_TIMER = 0
    gc.display_turn()
    assert gc.TURN_DISPLAY_TIMER == -1
