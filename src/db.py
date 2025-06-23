import sqlite3
from config import DB_PATH

# create table
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS papers(
            id        TEXT PRIMARY KEY,
            title     TEXT,
            authors   TEXT,
            abstract  TEXT,
            published TEXT,
            summary   TEXT
        )
        """
    )
    return conn