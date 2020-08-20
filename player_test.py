from player import Player
from board import Board


def test_constructor():
    board = Board(800, 4)
    human = Player(board)
    assert human.board == board
    assert human.legal_moves == {}
    assert human.turn is True
    assert human.color == 0


def test_check_legal():
    """
    Tests the check_legal() method of the Player class
    """
    board = Board(800, 4)
    human = Player(board)
    human.build_legal_moves()
    assert human.check_legal((0, 1)) is True
    assert human.check_legal((1, 0)) is True
    assert human.check_legal((3, 2)) is True
    assert human.check_legal((2, 3)) is True
    assert human.check_legal((3, 3)) is False
    assert human.check_legal((-1, 3)) is False
    assert human.check_legal((0, 4)) is False
    assert human.check_legal((1, 1)) is False
