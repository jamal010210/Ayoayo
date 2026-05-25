import persistence


class GameSession:
    """
    Handles runtime concerns of a game session:
    - saving results
    - preventing duplicate saves
    """

    def __init__(self, game):
        """Initialize the session with a game instance."""
        self.game = game
        self._saved = False

    def should_save(self) -> bool:
        """Check if the game result should be saved."""
        return self.game.winner is not None and not self._saved

    def save_result(self):
        """Save the game result if it has not been saved yet."""
        if not self.should_save():
            return

        p1_score, p2_score = self.game.get_scores()

        persistence.save_result(
            self.game.player_1.name,
            self.game.player_2.name,
            p1_score,
            p2_score,
        )

        self._saved = True
        self._log_save()

    def _log_save(self):
        """Log the saved game result to stdout."""
        print(
            f"Game saved: Winner {self.game.get_winner_name()}, "
            f"Loser {self.game.get_loser_name()}, "
            f"Scores {self.game.get_scores()}"
        )

    def reset(self, new_game):
        """Reset the session with a new game and clear save state."""
        self.game = new_game
        self._saved = False
