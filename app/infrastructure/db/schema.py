from app.infrastructure.db.database import get_connection


def init_database():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            symbol TEXT NOT NULL,
            asset_type TEXT NOT NULL,
            source TEXT NOT NULL,
            currency TEXT NOT NULL,
            note TEXT DEFAULT ''
        )
        '''
    )
    conn.commit()
    conn.close()
