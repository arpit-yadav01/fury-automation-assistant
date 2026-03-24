# memory/memory_db.py

import sqlite3
import os


DB_PATH = os.path.join("memory", "fury.db")


class MemoryDB:

    def __init__(self):

        os.makedirs("memory", exist_ok=True)

        self.conn = sqlite3.connect(DB_PATH)

        self.create_tables()

    # ---------------------

    def create_tables(self):

        cur = self.conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT,
                action TEXT,
                result TEXT
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                data TEXT
            )
            """
        )

        self.conn.commit()

    # ---------------------

    def save_history(self, command, action, result):

        cur = self.conn.cursor()

        cur.execute(
            "INSERT INTO history (command, action, result) VALUES (?, ?, ?)",
            (command, action, result),
        )

        self.conn.commit()

    # ---------------------

    def get_history(self, limit=5):

        cur = self.conn.cursor()

        cur.execute(
            "SELECT command, action, result FROM history ORDER BY id DESC LIMIT ?",
            (limit,),
        )

        return cur.fetchall()


memory_db = MemoryDB()