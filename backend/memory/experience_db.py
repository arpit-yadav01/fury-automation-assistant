import sqlite3
import os

DB = os.path.join("memory", "experience.db")


class ExperienceDB:

    def __init__(self):

        os.makedirs("memory", exist_ok=True)

        self.conn = sqlite3.connect(DB)

        self.create()

    def create(self):

        cur = self.conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS experience (
            id INTEGER PRIMARY KEY,
            task TEXT,
            action TEXT,
            result TEXT,
            success INTEGER
        )
        """)

        self.conn.commit()

    def add(self, task, action, result, success):

        cur = self.conn.cursor()

        cur.execute(
            "INSERT INTO experience (task, action, result, success) VALUES (?, ?, ?, ?)",
            (str(task), str(action), str(result), int(success))
        )

        self.conn.commit()

    def get_all(self):

        cur = self.conn.cursor()

        cur.execute("SELECT * FROM experience")

        return cur.fetchall()


experience_db = ExperienceDB()