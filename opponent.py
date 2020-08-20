from game_player import GamePlayer


class Opponent(GamePlayer):
    """A class representing the AI opponent"""
    def __init__(self, board):
        self.board = board
        self.legal_moves = {}
        self.color = 1

    def choose_move(self):
        """
        Chooses the "best" legal move, returns a tuple
        corresponding to the move that turns the
        maxmum number of disks to the computer
        opponent's color"""
        move = None
        for tile in self.legal_moves.keys():
            if ((move is None) or
                (len(self.legal_moves[tile])
                 > len(self.legal_moves[move]))):
                move = tile
        return move
