
class GamePlayer:
    """Contains methods common to the humnan player and the AI opponent"""

    def check_legal_moves_left(self):
        """
        Checks if any legal moves remain, returns
        a Boolean result.
        """
        if self.legal_moves:
            return True
        else:
            return False

    def build_legal_moves(self):
        """Builds a dictionary of legal moves"""
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1),
                      (-1, 0), (-1, -1), (0, -1), (1, -1)]
        self.legal_moves = {}

        # Determine the color of the opposing player
        if self.color == 0:
            opponent_color = 1
        else:
            opponent_color = 0

        for i in range(self.board.SIZE):
            for j in range(self.board.SIZE):
                # At each empty tile on the board, moves in
                # each of the 8 directions checking for legal moves.
                if self.board.disks[i][j].color == -1:
                    for direction in directions:
                        row, column = i, j
                        pathway = [(row, column)]
                        row += direction[0]
                        column += direction[1]
                        # Keep moving in the current direction as long
                        # as we stay on the board and encounter disks
                        # of the opposing player's color.
                        while (self.check_on_board(row, column)
                               and
                               (self.board.disks[row][column].color
                                == opponent_color)):
                            pathway.append((row, column))
                            row += direction[0]
                            column += direction[1]
                        # Make sure after encountering disks of the
                        # other player's color, we encounter whosevers
                        # turns disk color.
                        if (self.check_on_board(row, column)
                           and
                           self.board.disks[row][column].color == self.color):
                            # Once pathway has been built,
                            # add it to legal_moves dictionary
                            if len(pathway) > 1:
                                # If the tile started with has not yet
                                # been added as a key to the dictionary,
                                # make the new key : value pair.
                                if (pathway[0] not in
                                        self.legal_moves.keys()):
                                    self.legal_moves[pathway[0]] = set()
                                # Otherwise, add all tiles from the previously
                                # found legal move set to the set of tiles
                                # associated with the empty tile we
                                # started with.
                                for tile in pathway:
                                    self.legal_moves[pathway[0]].add(tile)

    def check_on_board(self, row, col):
        """
        Given the row and column of a tile, returns
        a Boolean indicating if it is on the board
        """
        if ((row < 0) or (col < 0)
           or (row >= self.board.SIZE)
           or (col >= self.board.SIZE)):
            return False
        else:
            return True

    def make_move(self, row, column):
        """
        Makes a move for a player by turning the appropriate disks
        to their color.
        """
        for move in self.legal_moves.keys():
            self.board.disks[move[0]][move[1]].color = -1
        for tile in self.legal_moves[(row, column)]:
            self.board.disks[tile[0]][tile[1]].color = self.color
