import sqlite3
import os


DB = os.path.join("memory", "knowledge.db")


class KnowledgeDB:

    def __init__(self):

        os.makedirs("memory", exist_ok=True)

        self.conn = sqlite3.connect(DB)

        self.create()

    # -----------------

    def create(self):

        cur = self.conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY,
                key TEXT,
                value TEXT
            )
            """
        )

        self.conn.commit()

    # -----------------

    def add(self, key, value):

        cur = self.conn.cursor()

        cur.execute(
            "INSERT INTO knowledge (key,value) VALUES (?,?)",
            (key, value),
        )

        self.conn.commit()

    # -----------------

    def get(self, key):

        cur = self.conn.cursor()

        cur.execute(
            "SELECT value FROM knowledge WHERE key=?",
            (key,),
        )

        row = cur.fetchone()

        if row:
            return row[0]

        return None


knowledge_db = KnowledgeDB()