import sqlite3
from typing import Optional, Dict


class UserRepo:
    def __init__(self, db_path: str = "data.db"):
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self._conn() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL
                )
                """
            )

    def create_user(self, name: str, email: str) -> Dict:
        with self._conn() as conn:
            cur = conn.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                (name, email),
            )
            user_id = cur.lastrowid
            return {"id": user_id, "name": name, "email": email}

    def get_user(self, user_id: int) -> Optional[Dict]:
        with self._conn() as conn:
            cur = conn.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
            row = cur.fetchone()
            if not row:
                return None
            return {"id": row[0], "name": row[1], "email": row[2]}

    def update_user(self, user_id: int, name: Optional[str], email: Optional[str]) -> Optional[Dict]:
        user = self.get_user(user_id)
        if not user:
            return None
        new_name = name if name is not None else user["name"]
        new_email = email if email is not None else user["email"]
        with self._conn() as conn:
            conn.execute(
                "UPDATE users SET name = ?, email = ? WHERE id = ?",
                (new_name, new_email, user_id),
            )
        return {"id": user_id, "name": new_name, "email": new_email}

    def delete_user(self, user_id: int) -> bool:
        with self._conn() as conn:
            cur = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
            return cur.rowcount > 0
