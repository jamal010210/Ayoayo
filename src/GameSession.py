import persistence


class GameSession:
    """
    Handles runtime concerns of a game session:
    - saving results
    - preventing duplicate saves
    """

    def __init__(self, game):
        """Initializes a game session tied to a Game instance."""
        self.game = game
        self._saved = False

    def should_save(self) -> bool:
        """Checks whether the current game result should be saved."""
        return self.game.winner is not None and not self._saved

    def save_result(self):
        """Saves the game result to persistence if not already saved."""
        if not self.should_save():
            return

        persistence.save_result(
            self.game.player_1.name,
            self.game.player_2.name,
            self.game.get_winner_name(),
            self.game.get_loser_name(),
            *self.game.get_scores(),
        )

        self._saved = True
        self._log_save()

    def _log_save(self):
        """Logs the saved game result to the console."""
        print(
            f"Game saved: Winner {self.game.get_winner_name()}, "
            f"Loser {self.game.get_loser_name()}, "
            f"Scores {self.game.get_scores()}"
        )

    def reset(self, new_game):
        """Resets the session with a new game instance."""
        self.game = new_game
        self._saved = False
