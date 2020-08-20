
class Disk:
    """An Othello game piece (disk)"""
    def __init__(self, row, column, TILE_SPACING, color):
        self.row = row
        self.column = column
        self.TILE_SPACING = TILE_SPACING
        self.color = color
        self.TOLERANCE = 10

    def display(self):
        """Displays the disk"""
        DARK_GREEN = (0, 0.4, 0)
        if self.color >= 0:
            fill(self.color)
            ellipse(self.row * self.TILE_SPACING + self.TILE_SPACING//2,
                    self.column * self.TILE_SPACING + self.TILE_SPACING//2,
                    self.TILE_SPACING - self.TOLERANCE,
                    self.TILE_SPACING - self.TOLERANCE)
        # Displays disk outline to show legal moves for human player
        elif self.color == -0.5:
            fill(*DARK_GREEN)
            ellipse(self.row * self.TILE_SPACING + self.TILE_SPACING//2,
                    self.column * self.TILE_SPACING + self.TILE_SPACING//2,
                    self.TILE_SPACING - self.TOLERANCE,
                    self.TILE_SPACING - self.TOLERANCE)
        else:
            # If color property is -1, do not display the disk
            return
