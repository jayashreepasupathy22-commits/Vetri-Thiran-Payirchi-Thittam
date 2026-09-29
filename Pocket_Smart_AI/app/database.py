from contextlib import contextmanager
from pathlib import Path
import sqlite3

from .config import settings


DB_PATH = Path(
    settings.DATABASE_URL.replace("sqlite:///", "")
)

DB_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    planner TEXT NOT NULL,
    input_json TEXT NOT NULL,
    result_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);
"""


def init_db():
    with sqlite3.connect(DB_PATH) as connection:
        connection.executescript(SCHEMA)
        connection.commit()


@contextmanager
def get_db():
    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    try:
        yield connection
        connection.commit()

    finally:
        connection.close()