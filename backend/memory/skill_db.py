# memory/skill_db.py

import sqlite3
import os


DB_PATH = os.path.join("memory", "fury.db")


class SkillDB:

    def __init__(self):

        os.makedirs("memory", exist_ok=True)

        self.conn = sqlite3.connect(DB_PATH)

        self.create_table()

    # ---------------------

    def create_table(self):

        cur = self.conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS skilldb (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                data TEXT
            )
            """
        )

        self.conn.commit()

    # ---------------------

    def save_skill(self, name, data):

        cur = self.conn.cursor()

        cur.execute(
            "INSERT INTO skilldb (name, data) VALUES (?, ?)",
            (name, data),
        )

        self.conn.commit()

    # ---------------------

    def get_skills(self):

        cur = self.conn.cursor()

        cur.execute(
            "SELECT name, data FROM skilldb"
        )

        return cur.fetchall()


skill_db = SkillDB()