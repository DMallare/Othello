from opponent import Opponent
from board import Board


def test_constructor():
    board = Board(800, 4)
    computer = Opponent(board)
    assert computer.board == board
    assert computer.legal_moves == {}
    assert computer.color == 1


def test_choose_move():
    """Tests the choose_move() method of the Opponent class"""
    board = Board(800, 4)
    computer = Opponent(board)
    assert computer.choose_move() is None
    computer.legal_moves = {(1, 1): {(1, 1), (1, 2)},
                            (0, 3): {(0, 3), (1, 3), (2, 3), (0, 2), (0, 1)},
                            (0, 0): {(0, 0), (1, 0), (2, 0), (3, 0)}
                            }
    assert computer.choose_move() == (0, 3)
