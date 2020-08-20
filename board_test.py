from board import Board


def test_constructor():
    """ Tests the Board constructor"""
    # Test with a board of size 4
    board = Board(800, 4)
    assert board.SIZE == 4
    assert board.WINDOW_SIZE == 800
    assert board.TILE_SPACING == 200
    assert board.BLACK == 0
    assert board.WHITE == 1
    assert board.no_disk_color == -1
    assert board.MIDDLE == 2
    # Check number of rows and columns on board are correct
    assert len(board.disks) == 4
    assert len(board.disks[0]) == 4
    # Check that the correct disks are placed
    # on the board at the beginning of the game.
    num_disks_on_board = 0
    for row in range(len(board.disks)):
        for col in range(len(board.disks[0])):
            if board.disks[row][col].color != -1:
                num_disks_on_board += 1
    assert num_disks_on_board == 4
    assert board.disks[1][1].color == 1
    assert board.disks[1][2].color == 0
    assert board.disks[2][1].color == 0
    assert board.disks[2][2].color == 1

    # Test with a board of size 2
    board = Board(800, 2)
    assert board.SIZE == 2
    assert board.WINDOW_SIZE == 800
    assert board.TILE_SPACING == 400
    assert board.BLACK == 0
    assert board.WHITE == 1
    assert board.no_disk_color == -1
    assert board.MIDDLE == 1
    # Check that the correct disks are placed
    # on the board at the beginning of the game.
    num_disks_on_board = 0
    for row in range(len(board.disks)):
        for col in range(len(board.disks[0])):
            if board.disks[row][col].color != -1:
                num_disks_on_board += 1
    assert num_disks_on_board == 4
    assert board.disks[0][0].color == 1
    assert board.disks[1][0].color == 0
    assert board.disks[0][1].color == 0
    assert board.disks[1][1].color == 1


def test_check_full():
    """Tests the check_full() method of the Board class"""
    board = Board(800, 4)
    assert board.check_full() is False
    # Fill the board with disks and check if method
    # returns True (board is full)
    for row in range(4):
        for col in range(4):
            board.disks[row][col].color = 0
    assert board.check_full() is True


def test_update_score():
    """Tests the update_score() method of the Board class"""
    board = Board(800, 4)
    num_black, num_white = board.update_score()
    assert num_black == 2
    assert num_white == 2
    board.disks[1][1].color = 0
    board.disks[1][0].color = 0
    num_black, num_white = board.update_score()
    assert num_black == 4
    assert num_white == 1
