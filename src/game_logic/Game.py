from game_logic.Player import Player
from game_logic.Board import Board



class Game:
    def __init__(self):
        self.player_1 = Player("Player 1")
        self.player_2 = Player("Player 2")
        self.round = 1
        self.board = Board(self.player_1, self.player_2)

    def current_player(self):
        """Returns the current player"""
        if self.round % 2 == 1:
            return self.player_1
        else:
            return self.player_2
    

            
    

    def draw(self):
        """Draws everything in a game"""

        # todo: remove this console output code
        print("===========================")

        self.board.draw()

        # todo: remove this console output code
        print("===========================")

        # Todo draw game specific things (E.g. round counter)

    def end_turn(self):
        """Ends the turn"""
        self.check_if_win()
        self.round += 1

    def check_if_win(self):
        """Checks if theres a win/draw"""
        pass
