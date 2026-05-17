from src import persistence


def _reset_db():
    if persistence.DB_PATH.exists():
        persistence.DB_PATH.unlink()


def test_save_and_get():
    _reset_db()
    persistence.init_db()
    persistence.save_result("Alice", "Bob", "Alice", "Bob", 25, 20)

    results = persistence.get_results()
    players = persistence.get_players()

    assert len(results) == 1
    assert len(players) == 2

    alice = next(row for row in players if row[1] == "Alice")
    bob = next(row for row in players if row[1] == "Bob")

    assert alice[2] == 1
    assert alice[3] == 0
    assert alice[4] == 0
    assert alice[5] == 1

    assert bob[2] == 0
    assert bob[3] == 1
    assert bob[4] == 0
    assert bob[5] == 1

    print("Test passed: Result saved and player statistics created")


def test_get_player_history():
    _reset_db()
    persistence.init_db()
    persistence.save_result("Alice", "Bob", "Alice", "Bob", 25, 20)

    player = persistence.get_player_by_id(1)
    assert player is not None
    assert player[1] == "Alice"

    history = persistence.get_player_history(1)
    assert len(history) == 1
    assert history[0][3] == "Alice"
    assert history[0][7] == 25
    assert history[0][8] == 20

    print("Test passed: Player history lookup returned the saved game")

if __name__ == "__main__":
    test_save_and_get()
    test_get_player_history()
