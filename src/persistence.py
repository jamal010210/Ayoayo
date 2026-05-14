import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("game_results.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY,
                winner TEXT,
                loser TEXT,
                player1_score INTEGER,
                player2_score INTEGER,
                timestamp TEXT
            )
        """)
        cursor = conn.execute("PRAGMA table_info(results)")
        columns = [row[1] for row in cursor.fetchall()]
        if "loser" not in columns:
            conn.execute("ALTER TABLE results ADD COLUMN loser TEXT")


def save_result(winner, loser, player1_score, player2_score):
    timestamp = datetime.now().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO results (winner, loser, player1_score, player2_score, timestamp) VALUES (?, ?, ?, ?, ?)",
            (winner, loser, player1_score, player2_score, timestamp)
        )

def get_results():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT * FROM results ORDER BY timestamp DESC")
        return cursor.fetchall()
