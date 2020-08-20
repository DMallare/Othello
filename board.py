from disk import Disk


class Board:
    """Draws a square board and handles disk placement"""
    def __init__(self, WINDOW_SIZE, SIZE):
        self.SIZE = SIZE
        self.WINDOW_SIZE = WINDOW_SIZE
        self.TILE_SPACING = self.WINDOW_SIZE//self.SIZE
        self.BLACK = 0
        self.WHITE = 1
        # Initiate disk color to -1 to indicate play has not yet started
        self.no_disk_color = -1
        # Create the board filled with disks that are not displayed
        # set color property to -1 to ensure disks are not displayed
        self.disks = [
                    [Disk(i, j, self.TILE_SPACING, self.no_disk_color)
                     for i in range(self.SIZE)
                     ]
                    for j in range(self.SIZE)
        ]
        # Change the color of the four middle disks on the board
        self.MIDDLE = self.SIZE//2
        self.disks[self.MIDDLE - 1][self.MIDDLE - 1].color = self.WHITE
        self.disks[self.MIDDLE - 1][self.MIDDLE].color = self.BLACK
        self.disks[self.MIDDLE][self.MIDDLE - 1].color = self.BLACK
        self.disks[self.MIDDLE][self.MIDDLE].color = self.WHITE

    def display(self):
        """Displays the Othello game board and disks"""
        strokeWeight(4)
        # Draw vertical lines
        for i in range(1, self.SIZE):
            line(i * self.TILE_SPACING, 0,
                 i * self.TILE_SPACING, self.WINDOW_SIZE - 1)
        # Draw horizontal lines
        for i in range(1, self.SIZE):
            line(0, i * self.TILE_SPACING,
                 self.WINDOW_SIZE - 1, i * self.TILE_SPACING)
        # Draw disks
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                self.disks[row][col].display()

    def check_full(self):
        """Checks if board is full of colored disks"""
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                # If we find a non-colored disk, immediately return False
                if self.disks[row][col].color == -1:
                    return False
        return True

    def update_score(self):
        """Updates the color count, returns a tuple of number
        of black and white disks on the board respectfully."""
        num_black_disks = 0
        num_white_disks = 0
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if self.disks[i][j].color == self.BLACK:
                    num_black_disks += 1
                if self.disks[i][j].color == self.WHITE:
                    num_white_disks += 1
        return (num_black_disks, num_white_disks)
