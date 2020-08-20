from disk import Disk


def test_constructor():
    """ Tests the Disk constructor """
    d = Disk(1, 3, 50, 1)
    assert d.row == 1
    assert d.column == 3
    assert d.TILE_SPACING == 50
    assert d.color == 1
    assert d.TOLERANCE == 10
