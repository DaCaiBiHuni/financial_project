from app.infrastructure.db.database import get_connection


class PriceHistoryRepository:
    def add_price_point(self, product_id: int, price: float, recorded_at: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO price_history (product_id, price, recorded_at) VALUES (?, ?, ?)',
            (product_id, price, recorded_at),
        )
        conn.commit()
        conn.close()

    def replace_yearly_history(self, product_id: int, history: list[dict]):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM price_history WHERE product_id = ?', (product_id,))
        for item in history:
            cur.execute(
                'INSERT INTO price_history (product_id, price, recorded_at) VALUES (?, ?, ?)',
                (product_id, item['price'], item['recorded_at']),
            )
        conn.commit()
        conn.close()

    def get_price_history(self, product_id: int, limit: int = 20):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            'SELECT price, recorded_at FROM price_history WHERE product_id = ? ORDER BY recorded_at ASC LIMIT ?',
            (product_id, limit),
        )
        rows = cur.fetchall()
        conn.close()
        return rows
