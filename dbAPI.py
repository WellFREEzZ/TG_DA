import sqlite3 as sq
from typing import Union
import config
import os

SQ_STRUCT = {
    'users': {
        'tg_id': 'INTEGER NOT NULL',
        'username': 'TEXT',
        'active_msg_id': 'INTEGER NOT NULL',
        'da_token': 'TEXT',
        'cha_tg_id': 'INTEGER',
        'active': 'BOOLEAN DEFAULT FALSE',
    },
}


class User:
    def __init__(self, par: dict):
        self.tg_id = None
        for k, v in par.items():
            setattr(self, k, v)


class SQLiteAPI:
    def __init__(self):
        self.conn = sq.connect(database=config.SQ_DB_NAME)
        self.conn.row_factory = sq.Row
        self.cur = self.conn.cursor()
        with self.conn:
            for table, params in SQ_STRUCT.items():
                self.cur.execute(f"CREATE TABLE IF NOT EXISTS {table} "
                                 f"({', '.join(f'{k} {v}' for k, v in params.items())})")

    """USERS"""

    def add_user(self, tg_id: int, username: str, active_msg_id: int):
        with self.conn:
            self.cur.execute("INSERT INTO users (tg_id, username, active_msg_id) values (?, ?, ?)",
                             (tg_id, username, active_msg_id))

    def get_user(self, tg_id: int):
        with self.conn:
            result = self.cur.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,)).fetchone()
            try:
                return User(dict(result))
            except TypeError:
                return False

    def update_user(self, user: User):
        with self.conn:
            self.cur.execute(
                f"UPDATE users SET "
                f"{', '.join(f'{k} = ?' for k in user.__dict__.keys())} "
                f"WHERE tg_id = {user.tg_id}", [v for v in user.__dict__.values()])

    def get_all_users(self):
        result = []

        with self.conn:
            for row in self.cur.execute("SELECT * FROM users").fetchall():
                result.append(User(dict(row)))

        return result

    def remove_user(self, user: User):
        with self.conn:
            self.cur.execute("DELETE FROM users WHERE tg_id = ?", (user.tg_id,))


if __name__ == '__main__':
    a = SQLiteAPI()
    print(a.get_user(123))
