from player import Player
from opponent import Opponent
from board import Board
import re


class GameController:
    """Maintains the state of the game"""
    def __init__(self, board):
        self.board = board
        self.WINDOW_SIZE = board.WINDOW_SIZE
        self.SIZE = board.SIZE
        self.TILE_SPACING = self.WINDOW_SIZE//self.SIZE

        self.human = Player(self.board)
        self.computer = Opponent(self.board)
        self.num_times_no_legal_moves = 0
        self.MESSAGE_DISPLAY_LENGTH = 60
        self.TURN_DISPLAY_TIMER = self.MESSAGE_DISPLAY_LENGTH
        self.NO_LEGAL_MOVES_DISPLAY_TIMER = -1
        self.ASK_FOR_INFO_TIMER = -1
        self.NUM_OF_NO_LEGAL_MOVES_LEFT_TO_END_GAME = 2
        self.game_over = False
        self.need_information = False

    def set_turn(self):
        """Sets whose turn it is"""
        self.human.turn = not self.human.turn

    def start_game(self):
        """
        Start the game by announcing the human player's turn,
        building the legal moves dictionary for the human player, and
        displaying all possible legal moves for the human player.
        """
        self.display_turn()
        self.human.build_legal_moves()
        for move in self.human.legal_moves.keys():
            self.board.disks[move[0]][move[1]].color = -0.5

    def update(self):
        """
        Checks game status, updates whose turn it is,
        and prepares for whosever's turn it is.
        """
        # Check if the board is full, if it is end the game
        if not self.game_over:
            board_full = self.board.check_full()
            if board_full:
                self.ASK_FOR_INFO_TIMER = self.MESSAGE_DISPLAY_LENGTH
                self.game_over = True
                return
            # Continue update if the board is not full
            # Set the turn and continue game play based on whose turn it is
            self.set_turn()
            if self.human.turn:
                legal_moves_left = \
                                 self.prepare_for_turn(self.human)
            else:
                legal_moves_left = \
                                self.prepare_for_turn(self.computer)
            # If legal moves are found allow the player
            # (human or computer) to take their turn
            if legal_moves_left:
                self.start_turn()
            # If there are no legal moves left decide to switch turns
            # or end the game
            else:
                self.num_times_no_legal_moves += 1
                self.NO_LEGAL_MOVES_DISPLAY_TIMER = self.MESSAGE_DISPLAY_LENGTH

    def prepare_for_turn(self, player):
        """
        Prepares for a player (human or AI) to take their turn,
        builds their legal_moves dictionary and checks if there
        are any legal moves. Returns Boolean value result
        of checking for legal moves.
        """
        player.build_legal_moves()
        legal_moves_left = player.check_legal_moves_left()
        return legal_moves_left

    def start_turn(self):
        """ Allows a player to begin their turn (human or AI)"""
        self.num_times_no_legal_moves = 0
        self.TURN_DISPLAY_TIMER = self.MESSAGE_DISPLAY_LENGTH
        if self.human.turn:
            for move in self.human.legal_moves.keys():
                self.board.disks[move[0]][move[1]].color = -0.5

    def computer_take_turn(self):
        """
        Allows the AI to take their turn by choosing the best
        move and making the move (if there is one).
        """
        best_move = self.computer.choose_move()
        if best_move:
            row, column = best_move
            self.computer.make_move(row, column)
            self.update()

    def display_message(self):
        """Displays the various in game messages"""
        if self.NO_LEGAL_MOVES_DISPLAY_TIMER >= 0:
            self.display_no_legal_moves_available()
        if self.TURN_DISPLAY_TIMER >= 0:
            self.display_turn()
        if self.game_over:
            self.display_end_of_game_message()

    def display_no_legal_moves_available(self):
        """
        Displays there are no legal moves for the current player
        and decrements the no legal moves message timer.
        """
        if self.NO_LEGAL_MOVES_DISPLAY_TIMER > 0:
            fill(1, 0, 0)
            textSize(self.WINDOW_SIZE//12)
            textAlign(CENTER, CENTER)
            if self.human.turn:
                message = "You are out of moves!"
            else:
                message = "The computer has no\nmoves to make"
            # Display the message
            text(message, self.WINDOW_SIZE//2, self.WINDOW_SIZE//4)
            # Decrement display timer and call display method recursively
            self.NO_LEGAL_MOVES_DISPLAY_TIMER -= 1

        elif self.NO_LEGAL_MOVES_DISPLAY_TIMER == 0:
            # End display and decide next steps
            self.NO_LEGAL_MOVES_DISPLAY_TIMER -= 1
            self.no_legal_moves_available()

    def no_legal_moves_available(self):
        """
        Decides a course of action when a player has no
        legal moves to make.
        """
        # If there have been two consecuutive turns where
        # player did not have any legal moves, end the game.
        if (self.num_times_no_legal_moves ==
                self.NUM_OF_NO_LEGAL_MOVES_LEFT_TO_END_GAME):
            self.ASK_FOR_INFO_TIMER = self.MESSAGE_DISPLAY_LENGTH
            self.game_over = True
        # Othewise, allow the game to continue
        else:
            self.update()

    def display_turn(self):
        """Displays whose turn it is"""
        if self.TURN_DISPLAY_TIMER > 0:
            fill(1, 0, 0)
            textSize(self.WINDOW_SIZE//12)
            textAlign(CENTER)
            # Determine whose turn it is and display the
            # appropriate message.
            if self.human.turn:
                message = "Your turn!"
            else:
                message = "It's the computer's turn"
            text(message, self.WINDOW_SIZE//2,
                 self.WINDOW_SIZE//4)
            self.TURN_DISPLAY_TIMER -= 1

        # When turn message is finished displaying (timer is at 0),
        # if its the AI's turn, let it make its move, otherwise wait
        # for the human player to make their move.
        if self.TURN_DISPLAY_TIMER == 0:
            self.TURN_DISPLAY_TIMER -= 1
            if not self.human.turn:
                self.computer_take_turn()

    def display_end_of_game_message(self):
        """Displays end of game message with scores"""
        # Compute final scores
        if self.game_over:
            scores = self.board.update_score()
            self.human.score = scores[0]
            self.computer.score = scores[1]
            fill(1, 0, 0)
            textSize(self.WINDOW_SIZE//10)
            textAlign(CENTER, CENTER)
            # Determine who won
            if (self.human.score > self.computer.score):
                message = "YOU WIN!"
            elif (self.human.score < self.computer.score):
                message = "YOU LOSE"
            else:
                message = "TIE GAME!"
            # Display who won
            text(message, self.WINDOW_SIZE//2,
                 self.WINDOW_SIZE//4)
            # Display final scores
            textAlign(CENTER, TOP)
            textSize(self.WINDOW_SIZE//10)
            text("Final Score:\nYou: " + str(self.human.score) +
                 "\nComputer: " + str(self.computer.score),
                 self.WINDOW_SIZE//2, self.WINDOW_SIZE//2)
            self.ASK_FOR_INFO_TIMER -= 1

            if self.ASK_FOR_INFO_TIMER == 0:
                # Write human player's name and results to scores file
                name = self.get_player_name()
                self.record_results(name)

    def input_name(self, message=''):
        """Prompts the player for their name"""
        from javax.swing import JOptionPane
        return JOptionPane.showInputDialog(frame, message)

    def get_player_name(self):
        """
        Prompts the player for their name and stores this information.
        If the player hits cancel, their name is stored as "Anonymous."
        """
        try:
            name = self.input_name("Please enter your name: ")
            name = name.strip().replace(" ", "_")
            name = name.title()
            return name
        except AttributeError:
            return "Anonymous"

    def record_results(self, name):
        """
        Prompts user for their name and adds their name
        and score to the scores.txt file. If the score exceeds
        the score at the top line of the file (the high score) then this
        record is added to the top line of the file. Otherwise, the record
        is added to the bottom of the file.
        """
        game_results = name + " " + str(self.human.score) + "\n"
        try:
            # Determine if current score exceeds the top score
            with open("scores.txt", "r") as f1:
                first_line = f1.readline()
                contents = f1.read()
            with open("scores.txt", "w+") as f2:
                if (self.human.score
                        > int(re.findall(r"\s(\d+)", first_line)[-1])):
                    f2.write(game_results + first_line + contents)
                else:
                    f2.write(first_line + contents + game_results)
        except IOError:
            # If scores.txt has not yet been created
            f1 = open("scores.txt", "w+")
            f1.write(game_results)
            f1.close()

    def mouse_control(self, x, y):
        """Handles when a player clicks the mouse"""
        if self.human.turn:
            # Determine what row and column on the board player has clicked
            column = x//self.TILE_SPACING
            row = y//self.TILE_SPACING
            # Check if the tile selected corresponds to a legal move
            # If it corresponds to a legal move, make the move and update
            if self.human.check_legal((row, column)):
                self.human.make_move(row, column)
                self.update()
            else:
                returns
