from game_logic.Player import Player
from game_logic.Board import Board


class Game:
    def __init__(self):
        self.player_1 = Player("Player 1")
        self.player_2 = Player("Player 2")
        self.round = 1
        self.board = Board(self.player_1, self.player_2)
        self.winner = None

    def current_player(self):
        """Returns the current player"""
        if self.round % 2 == 1:
            return self.player_1
        else:
            return self.player_2

    def end_turn(self):
        """Ends the turn"""
        self.check_if_win()
        self.round += 1

    def check_if_win(self):
        """Checks if theres a win/draw"""
        if self.board.bank[self.player_1] >= 25:
            self.winner = self.player_1
        elif self.board.bank[self.player_2] >= 25:
            self.winner = self.player_2
        elif (
            self.board.bank[self.player_1] == 24
            and self.board.bank[self.player_2] == 24
        ):
            self.winner = "draw"

        # both players have no valid moves left
        elif not self.board.field_collection.has_valid_moves(
            self.player_1
        ) and not self.board.field_collection.has_valid_moves(self.player_2):
            if self.board.bank[self.player_1] > self.board.bank[self.player_2]:
                self.winner = self.player_1
            elif self.board.bank[self.player_1] < self.board.bank[self.player_2]:
                self.winner = self.player_2
            else:
                self.winner = "draw"

    def get_winner_name(self):
        if self.winner == "draw":
            return "Draw"
        elif self.winner:
            return self.winner.name
        return None

    def get_loser_name(self):
        if self.winner == "draw":
            return "Draw"
        elif self.winner == self.player_1:
            return self.player_2.name
        elif self.winner == self.player_2:
            return self.player_1.name
        return None

    def get_scores(self):
        return self.board.bank[self.player_1], self.board.bank[self.player_2]

    def set_player_names(self, player_1_name: str, player_2_name: str):
        self.player_1.name = player_1_name
        self.player_2.name = player_2_name

