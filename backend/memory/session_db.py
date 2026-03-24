# memory/session_db.py

import sqlite3
import os


DB = "memory/session.db"


class SessionDB:

    def __init__(self):

        os.makedirs("memory", exist_ok=True)

        self.conn = sqlite3.connect(DB)

        self.create()

    # -----------------

    def create(self):

        cur = self.conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY,
                key TEXT,
                value TEXT
            )
            """
        )

        self.conn.commit()

    # -----------------

    def save(self, key, value):

        cur = self.conn.cursor()

        cur.execute(
            "INSERT INTO sessions (key,value) VALUES (?,?)",
            (key, value),
        )

        self.conn.commit()

    # -----------------

    def load_all(self):

        cur = self.conn.cursor()

        cur.execute("SELECT key,value FROM sessions")

        return cur.fetchall()


session_db = SessionDB()