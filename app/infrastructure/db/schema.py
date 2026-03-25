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
            current_price REAL NOT NULL DEFAULT 0,
            last_updated TEXT DEFAULT '',
            note TEXT DEFAULT ''
        )
        '''
    )

    columns = [row[1] for row in cur.execute("PRAGMA table_info(products)").fetchall()]
    if 'current_price' not in columns:
        cur.execute("ALTER TABLE products ADD COLUMN current_price REAL NOT NULL DEFAULT 0")
    if 'last_updated' not in columns:
        cur.execute("ALTER TABLE products ADD COLUMN last_updated TEXT DEFAULT ''")

    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS portfolio_positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity REAL NOT NULL,
            average_cost REAL NOT NULL,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
        '''
    )

    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            price REAL NOT NULL,
            recorded_at TEXT NOT NULL,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
        '''
    )

    conn.commit()
    conn.close()
