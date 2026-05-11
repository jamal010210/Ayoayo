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
                player1_score INTEGER,
                player2_score INTEGER,
                timestamp TEXT
            )
        """)

def save_result(winner, player1_score, player2_score):
    timestamp = datetime.now().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO results (winner, player1_score, player2_score, timestamp) VALUES (?, ?, ?, ?)",
            (winner, player1_score, player2_score, timestamp)
        )

def get_results():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT * FROM results ORDER BY timestamp DESC")
        return cursor.fetchall()
