import sqlite3
import json

from config import DATABASE


def connect():
    return sqlite3.connect(DATABASE)


def initialize():

    with connect() as db:

        db.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                browser TEXT,
                events TEXT
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS findings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                category TEXT,
                description TEXT,
                timestamp TEXT
            )
        """)


def save_session(timestamp, browser, events):

    with connect() as db:

        cursor = db.execute("""
            INSERT INTO sessions
            (timestamp, browser, events)
            VALUES (?, ?, ?)
        """, (
            timestamp,
            browser,
            json.dumps(events)
        ))

        return cursor.lastrowid


def save_finding(session_id, category, description, timestamp):

    with connect() as db:

        db.execute("""
            INSERT INTO findings
            (session_id, category, description, timestamp)
            VALUES (?, ?, ?, ?)
        """, (
            session_id,
            category,
            description,
            timestamp
        ))


def get_sessions():

    with connect() as db:

        return db.execute("""
            SELECT * FROM sessions ORDER BY id DESC
        """).fetchall()