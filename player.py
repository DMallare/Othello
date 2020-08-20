from game_player import GamePlayer


class Player(GamePlayer):
    """A class representing the human player"""
    def __init__(self, board):
        # The human placing the black disks begins play
        self.board = board
        self.legal_moves = {}
        self.turn = True
        self.color = 0

    def check_legal(self, move):
        if move in self.legal_moves.keys():
            return True
        else:
            return False
