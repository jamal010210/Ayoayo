from game_logic.Player import Player
from game_logic.Board import Board


class Game:
    def __init__(self):
        self.player_1 = Player("Player 1")
        self.player_2 = Player("Player 2")
        self.board = Board(self.player_1, self.player_2)
        self.winner = None
        self.board_history = [self.board.clone_deep()]

    def current_player(self):
        """Returns the current player"""
        if self.current_round() % 2 == 1:
            return self.player_1
        else:
            return self.player_2

    def end_turn(self):
        """Ends the turn"""
        self.check_if_win()
        self.board_history.append(self.board.clone_deep())

    def undo_turn(self):
        """Reverts the last turn"""
        if self.current_round() < 2:
            return

        if self.winner is not None:
            return

        self.board_history.pop()
        self.board = self.board_history[-1].clone_deep()

    def current_round(self) -> int:
        """Get the current round"""
        return len(self.board_history)


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
