import json
import os

DB_PATH = "memory/app_db.json"


def load_db():

    if not os.path.exists(DB_PATH):
        return {}

    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except:
        return {}


def save_db(data):

    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)


def add_app(name, data):

    db = load_db()

    db[name] = data

    save_db(db)


def get_app(name):

    db = load_db()

    return db.get(name)