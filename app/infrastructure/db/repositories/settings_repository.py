from app.infrastructure.db.database import get_connection


class SettingsRepository:
    def get(self, key: str, default: str = '') -> str:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT value FROM settings WHERE key = ?', (key,))
        row = cur.fetchone()
        conn.close()
        return row[0] if row else default

    def set(self, key: str, value: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            '''
            INSERT INTO settings (key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
            ''',
            (key, value),
        )
        conn.commit()
        conn.close()
