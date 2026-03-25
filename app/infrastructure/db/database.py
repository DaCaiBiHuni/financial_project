from pathlib import Path
import sqlite3


DB_PATH = Path(__file__).resolve().parents[3] / 'data' / 'app.db'


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)
