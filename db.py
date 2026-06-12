import sqlite3
import json
from typing import List, Dict, Optional


class Database:
    def __init__(self, path: str):
        self.path = path
        self._init()

    def _conn(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init(self):
        with self._conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS bets (
                    uid     INTEGER NOT NULL,
                    bet_id  TEXT NOT NULL,
                    data    TEXT NOT NULL,
                    PRIMARY KEY (uid, bet_id)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    uid  INTEGER PRIMARY KEY,
                    data TEXT NOT NULL
                )
            """)
            conn.commit()

    # ── ставки ──

    def get_bets(self, uid: int) -> List[Dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT data FROM bets WHERE uid=? ORDER BY rowid", (uid,)
            ).fetchall()
        return [json.loads(r["data"]) for r in rows]

    def save_bet(self, uid: int, bet: Dict):
        with self._conn() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO bets (uid, bet_id, data) VALUES (?,?,?)",
                (uid, bet["id"], json.dumps(bet, ensure_ascii=False))
            )
            conn.commit()

    def update_bet(self, uid: int, bet_id: str, bet: Dict) -> bool:
        with self._conn() as conn:
            cur = conn.execute(
                "UPDATE bets SET data=? WHERE uid=? AND bet_id=?",
                (json.dumps(bet, ensure_ascii=False), uid, bet_id)
            )
            conn.commit()
            return cur.rowcount > 0

    def delete_bet(self, uid: int, bet_id: str) -> bool:
        with self._conn() as conn:
            cur = conn.execute(
                "DELETE FROM bets WHERE uid=? AND bet_id=?", (uid, bet_id)
            )
            conn.commit()
            return cur.rowcount > 0

    # ── настройки ──

    def get_settings(self, uid: int) -> Dict:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT data FROM settings WHERE uid=?", (uid,)
            ).fetchone()
        if row:
            return json.loads(row["data"])
        return {"unit": 1, "cur": "у.е.", "balance": None}

    def save_settings(self, uid: int, settings: Dict):
        with self._conn() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO settings (uid, data) VALUES (?,?)",
                (uid, json.dumps(settings, ensure_ascii=False))
            )
            conn.commit()
