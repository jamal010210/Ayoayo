import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("game_results.db")


def _timestamp():
    return datetime.now().isoformat()


def init_db():
    """Initializes the database"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                draws INTEGER DEFAULT 0,
                games_played INTEGER DEFAULT 0,
                last_played TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY,
                player1_id INTEGER,
                player2_id INTEGER,
                winner_id INTEGER,
                loser_id INTEGER,
                winner TEXT,
                loser TEXT,
                player1_score INTEGER,
                player2_score INTEGER,
                timestamp TEXT,
                FOREIGN KEY(player1_id) REFERENCES players(id),
                FOREIGN KEY(player2_id) REFERENCES players(id),
                FOREIGN KEY(winner_id) REFERENCES players(id),
                FOREIGN KEY(loser_id) REFERENCES players(id)
            )
        """)

        cursor = conn.execute("PRAGMA table_info(results)")
        columns = [row[1] for row in cursor.fetchall()]
        for column, column_type in [
            ("player1_id", "INTEGER"),
            ("player2_id", "INTEGER"),
            ("winner_id", "INTEGER"),
            ("loser_id", "INTEGER"),
            ("winner", "TEXT"),
            ("loser", "TEXT"),
        ]:
            if column not in columns:
                conn.execute(f"ALTER TABLE results ADD COLUMN {column} {column_type}")


def _get_player_id(conn, name):
    cursor = conn.execute("SELECT id FROM players WHERE name = ?", (name,))
    row = cursor.fetchone()
    if row:
        player_id = row[0]
        conn.execute(
            "UPDATE players SET last_played = ? WHERE id = ?",
            (_timestamp(), player_id),
        )
        return player_id

    cursor = conn.execute(
        "INSERT INTO players (name, last_played) VALUES (?, ?)",
        (name, _timestamp()),
    )
    return cursor.lastrowid


def _update_player_stats(conn, player_id, wins=0, losses=0, draws=0):
    conn.execute(
        """
            UPDATE players
            SET wins = wins + ?,
                losses = losses + ?,
                draws = draws + ?,
                games_played = games_played + 1,
                last_played = ?
            WHERE id = ?
        """,
        (wins, losses, draws, _timestamp(), player_id),
    )


# pylint: disable=too-many-arguments, too-many-positional-arguments
def save_result(
    player1_name, player2_name, winner_name, loser_name, player1_score, player2_score
):
    """Saves the result of a run into the database"""
    timestamp = _timestamp()
    with sqlite3.connect(DB_PATH) as conn:
        player1_id = _get_player_id(conn, player1_name)
        player2_id = _get_player_id(conn, player2_name)

        winner_id = None
        loser_id = None
        if winner_name != "Draw":
            if winner_name == player1_name:
                winner_id, loser_id = player1_id, player2_id
            elif winner_name == player2_name:
                winner_id, loser_id = player2_id, player1_id
            else:
                # fallback if winner/loser names are passed differently
                if loser_name == player1_name:
                    winner_id, loser_id = player2_id, player1_id
                else:
                    winner_id, loser_id = player1_id, player2_id

        if winner_name == "Draw":
            _update_player_stats(conn, player1_id, draws=1)
            _update_player_stats(conn, player2_id, draws=1)
        else:
            _update_player_stats(conn, winner_id, wins=1)
            _update_player_stats(conn, loser_id, losses=1)

        conn.execute(
            """
                INSERT INTO results (
                    player1_id,
                    player2_id,
                    winner_id,
                    loser_id,
                    winner,
                    loser,
                    player1_score,
                    player2_score,
                    timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                player1_id,
                player2_id,
                winner_id,
                loser_id,
                winner_name,
                loser_name,
                player1_score,
                player2_score,
                timestamp,
            ),
        )


def get_results():
    """Returns all results recorded thus far"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT * FROM results ORDER BY timestamp DESC")
        return cursor.fetchall()


def get_players():
    """Returns all player data"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """SELECT id, name, wins, losses, draws, games_played, last_played
            FROM players
            ORDER BY wins DESC, games_played DESC"""
        )
        return cursor.fetchall()


def get_player_by_id(player_id):
    """Returns the player data by ID"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """SELECT id, name, wins, losses, draws, games_played, last_played
            FROM players
            WHERE id = ?""",
            (player_id,),
        )
        return cursor.fetchone()


def get_player_by_name(name):
    """Returns the player ID by name"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """SELECT id, name, wins, losses, draws, games_played, last_played
            FROM players
            WHERE LOWER(name) = LOWER(?) LIMIT 1""",
            (name,),
        )
        return cursor.fetchone()


def get_player_suggestions(name_query):
    """Returns the suggestions (possible players) for a given player name pattern"""
    query = name_query.strip()
    if not query:
        return []
    prefix = f"{query}%"
    contains = f"%{query}%"
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
                SELECT id, name
                FROM players
                WHERE name LIKE ? COLLATE NOCASE OR name LIKE ? COLLATE NOCASE
                ORDER BY
                    name LIKE ? COLLATE NOCASE DESC,
                    name LIKE ? COLLATE NOCASE DESC,
                    games_played DESC,
                    name ASC
                LIMIT 5
            """,
            (prefix, contains, prefix, contains),
        )
        return cursor.fetchall()


def get_player_history(player_id):
    """Returns the history for a given player ID"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
                SELECT
                    r.id,
                    r.player1_id,
                    r.player2_id,
                    p1.name AS player1_name,
                    p2.name AS player2_name,
                    r.winner,
                    r.loser,
                    r.player1_score,
                    r.player2_score,
                    r.timestamp
                FROM results AS r
                LEFT JOIN players AS p1 ON r.player1_id = p1.id
                LEFT JOIN players AS p2 ON r.player2_id = p2.id
                WHERE r.player1_id = ? OR r.player2_id = ?
                ORDER BY r.timestamp DESC
            """,
            (player_id, player_id),
        )
        return cursor.fetchall()
