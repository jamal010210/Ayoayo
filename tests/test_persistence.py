from src import persistence


def _reset_db():
    if persistence.DB_PATH.exists():
        persistence.DB_PATH.unlink()


def test_save_and_get():
    """Tests whether players and results are correctly saved and retrieved."""
    _reset_db()
    persistence.init_db()

    persistence.save_result("Alice", "Bob", 25, 20)

    results = persistence.get_results()
    players = persistence.get_players()

    assert len(results) == 1
    assert len(players) == 2

    alice = next(row for row in players if row[1] == "Alice")
    bob = next(row for row in players if row[1] == "Bob")

    # Alice wins (25 > 20)
    assert alice[2] == 1  # wins
    assert alice[3] == 0  # losses
    assert alice[4] == 0  # draws
    assert alice[5] == 1  # games_played

    assert bob[2] == 0
    assert bob[3] == 1
    assert bob[4] == 0
    assert bob[5] == 1

    print("Test passed: Result saved and player stats updated")


def test_get_player_history():
    """Tests whether match history is correctly saved and retrieved."""
    _reset_db()
    persistence.init_db()

    persistence.save_result("Alice", "Bob", 25, 20)

    player = persistence.get_player_by_name("Alice")
    assert player is not None
    alice_id = player[0]

    history = persistence.get_player_history(alice_id)

    assert len(history) == 1

    row = history[0]

    # New schema (joined fields):
    # (id, player1_name, player2_name, winner_name, loser_name, p1_score, p2_score, timestamp)

    assert row[1] == "Alice"
    assert row[2] == "Bob"
    assert row[3] == "Alice"   # winner
    assert row[5] == 25
    assert row[6] == 20

    print("Test passed: Player history lookup returned correct match data")


if __name__ == "__main__":
    test_save_and_get()
    test_get_player_history()