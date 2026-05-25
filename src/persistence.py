import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("game_results.db")


def _timestamp():
    return datetime.now().isoformat()


def init_db():
    """Initialize database."""
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

        # Removed redundant winner/loser TEXT columns
        conn.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY,
                player1_id INTEGER,
                player2_id INTEGER,
                winner_id INTEGER,
                loser_id INTEGER,
                player1_score INTEGER,
                player2_score INTEGER,
                timestamp TEXT,
                FOREIGN KEY(player1_id) REFERENCES players(id),
                FOREIGN KEY(player2_id) REFERENCES players(id),
                FOREIGN KEY(winner_id) REFERENCES players(id),
                FOREIGN KEY(loser_id) REFERENCES players(id)
            )
        """)


def _get_player_id(conn, name):
    """Get existing player ID or create player."""
    cursor = conn.execute(
        "SELECT id FROM players WHERE LOWER(name) = LOWER(?)",
        (name,),
    )

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
    """Update player statistics."""
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


def save_result(player1_name, player2_name, player1_score, player2_score):
    """Save match result."""
    with sqlite3.connect(DB_PATH) as conn:
        player1_id = _get_player_id(conn, player1_name)
        player2_id = _get_player_id(conn, player2_name)

        winner_id = None
        loser_id = None

        if player1_score > player2_score:
            winner_id = player1_id
            loser_id = player2_id

            _update_player_stats(conn, player1_id, wins=1)
            _update_player_stats(conn, player2_id, losses=1)

        elif player2_score > player1_score:
            winner_id = player2_id
            loser_id = player1_id

            _update_player_stats(conn, player2_id, wins=1)
            _update_player_stats(conn, player1_id, losses=1)

        else:
            _update_player_stats(conn, player1_id, draws=1)
            _update_player_stats(conn, player2_id, draws=1)

        conn.execute(
            """
            INSERT INTO results (
                player1_id,
                player2_id,
                winner_id,
                loser_id,
                player1_score,
                player2_score,
                timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                player1_id,
                player2_id,
                winner_id,
                loser_id,
                player1_score,
                player2_score,
                _timestamp(),
            ),
        )


def get_results():
    """Return all match results."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
            SELECT
                r.id,
                p1.name AS player1_name,
                p2.name AS player2_name,
                w.name AS winner_name,
                l.name AS loser_name,
                r.player1_score,
                r.player2_score,
                r.timestamp
            FROM results r
            LEFT JOIN players p1 ON r.player1_id = p1.id
            LEFT JOIN players p2 ON r.player2_id = p2.id
            LEFT JOIN players w ON r.winner_id = w.id
            LEFT JOIN players l ON r.loser_id = l.id
            ORDER BY r.timestamp DESC
            """
        )

        return cursor.fetchall()


def get_players():
    """Return all players."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
            SELECT
                id,
                name,
                wins,
                losses,
                draws,
                games_played,
                last_played
            FROM players
            ORDER BY wins DESC, games_played DESC
            """
        )

        return cursor.fetchall()


def get_player_by_id(player_id):
    """Return player by ID."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
            SELECT
                id,
                name,
                wins,
                losses,
                draws,
                games_played,
                last_played
            FROM players
            WHERE id = ?
            """,
            (player_id,),
        )

        return cursor.fetchone()


def get_player_by_name(name):
    """Return player by name."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
            SELECT
                id,
                name,
                wins,
                losses,
                draws,
                games_played,
                last_played
            FROM players
            WHERE LOWER(name) = LOWER(?)
            LIMIT 1
            """,
            (name,),
        )

        return cursor.fetchone()


def get_player_suggestions(name_query):
    """Return matching player suggestions."""
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
            WHERE name LIKE ? COLLATE NOCASE
               OR name LIKE ? COLLATE NOCASE
            ORDER BY
                name LIKE ? COLLATE NOCASE DESC,
                games_played DESC,
                name ASC
            LIMIT 5
            """,
            (prefix, contains, prefix),
        )

        return cursor.fetchall()


def get_player_history(player_id):
    """Return match history for player."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
            SELECT
                r.id,
                p1.name AS player1_name,
                p2.name AS player2_name,
                w.name AS winner_name,
                l.name AS loser_name,
                r.player1_score,
                r.player2_score,
                r.timestamp
            FROM results r
            LEFT JOIN players p1 ON r.player1_id = p1.id
            LEFT JOIN players p2 ON r.player2_id = p2.id
            LEFT JOIN players w ON r.winner_id = w.id
            LEFT JOIN players l ON r.loser_id = l.id
            WHERE r.player1_id = ?
               OR r.player2_id = ?
            ORDER BY r.timestamp DESC
            """,
            (player_id, player_id),
        )

        return cursor.fetchall()