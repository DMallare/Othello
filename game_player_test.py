from game_player import GamePlayer
from player import Player
from opponent import Opponent
from board import Board


WINDOW_SIZE = 800
SIZE = 4


def test_check_on_board():
    """
    Tests the check_on_board() method of the GamePlayer class
    """
    board = Board(WINDOW_SIZE, SIZE)
    gp = Player(board)
    result1 = gp.check_on_board(0, 3)
    assert result1 is True
    result2 = gp.check_on_board(-1, 2)
    assert result2 is False
    result3 = gp.check_on_board(1, 4)


def test_make_move():
    """
    Tests the make_move() method of the GamePlayer class
    """
    board = Board(WINDOW_SIZE, SIZE)
    human_player = Player(board)
    # Create legal moves dictionary
    human_player.legal_moves = {(0, 1): {(0, 1), (0, 2), (0, 3)},
                                (1, 0): {(1, 0), (2, 1)},
                                (0, 2): {(0, 2), (0, 3)}}
    # Have player call make_move() with a legal move
    # and check we get the desired results
    human_player.make_move(0, 2)
    assert board.disks[0][2].color == human_player.color
    assert board.disks[0][3].color == human_player.color
    # Check legal move suggestion disks have been reset to
    # empty tiles
    assert board.disks[0][1].color == -1
    assert board.disks[1][0].color == -1


def test_check_legal_moves_left():
    """
    Tests the check_legal_moves_left() method
    of the GamePlayer class
    """
    board = Board(WINDOW_SIZE, SIZE)
    player1 = Player(board)
    player2 = Opponent(board)
    player1.legal_moves = {}
    player2.legal_moves = {(0, 1): {(0, 1), (0, 2), (0, 3)},
                           (1, 0): {(1, 0), (2, 1)}}
    result1 = player1.check_legal_moves_left()
    assert result1 is False
    result2 = player2.check_legal_moves_left()
    assert result2 is True


def test_build_legal_moves():
    """
    Tests the build_legal_moves() method
    of the GamePlayer class
    """
    board = Board(WINDOW_SIZE, SIZE)
    player1 = Player(board)
    player1.build_legal_moves()
    # Check that the beginning of the game move sets are correct
    assert ((player1.board.MIDDLE - 2, player1.board.MIDDLE - 1)
            in player1.legal_moves.keys())
    assert ((player1.board.MIDDLE + 1, player1.board.MIDDLE)
            in player1.legal_moves.keys())
    assert ((player1.board.MIDDLE - 1, player1.board.MIDDLE - 2)
            in player1.legal_moves.keys())
    assert ((player1.board.MIDDLE, player1.board.MIDDLE + 1)
            in player1.legal_moves.keys())
    assert len(player1.legal_moves.keys()) == 4
