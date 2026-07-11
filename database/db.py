import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent.parent / "users.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            form_name TEXT,
            age INTEGER
        )
        """
    )

    connection.commit()
    connection.close()


def save_user(
    telegram_id: int,
    username: str | None,
    first_name: str | None,
    form_name: str,
    age: int,
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users (
            telegram_id,
            username,
            first_name,
            form_name,
            age
        )
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(telegram_id) DO UPDATE SET
            username = excluded.username,
            first_name = excluded.first_name,
            form_name = excluded.form_name,
            age = excluded.age
        """,
        (
            telegram_id,
            username,
            first_name,
            form_name,
            age,
        ),
    )

    connection.commit()
    connection.close()


def get_user(telegram_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT telegram_id, username, first_name, form_name, age
        FROM users
        WHERE telegram_id = ?
        """,
        (telegram_id,),
    )

    user = cursor.fetchone()

    connection.close()

    return user

def count_users() -> int:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")

    count = cursor.fetchone()[0]

    connection.close()

    return count

def get_users(limit: int = 5, offset: int = 0):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT telegram_id, username, first_name, form_name, age
        FROM users
        ORDER BY telegram_id DESC
        LIMIT ? OFFSET ?
        """,
        (limit, offset),
    )

    users = cursor.fetchall()

    connection.close()

    return users