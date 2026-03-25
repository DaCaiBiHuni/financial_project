from app.domain.models.product import Product
from app.infrastructure.db.database import get_connection


class ProductRepository:
    def add_product(self, product):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO products (name, symbol, asset_type, source, currency, current_price, last_updated, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (
                product.name,
                product.symbol,
                product.asset_type,
                product.source,
                product.currency,
                product.current_price,
                product.last_updated,
                product.note,
            ),
        )
        conn.commit()
        product_id = cur.lastrowid
        conn.close()
        return product_id

    def list_products(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, name, symbol, asset_type, source, currency, current_price, last_updated, note FROM products ORDER BY id DESC')
        rows = cur.fetchall()
        conn.close()
        return [
            Product(
                id=row[0],
                name=row[1],
                symbol=row[2],
                asset_type=row[3],
                source=row[4],
                currency=row[5],
                current_price=row[6] or 0.0,
                last_updated=row[7] or '',
                note=row[8] or '',
            )
            for row in rows
        ]

    def get_product(self, product_id: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            'SELECT id, name, symbol, asset_type, source, currency, current_price, last_updated, note FROM products WHERE id = ?',
            (product_id,),
        )
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        return Product(
            id=row[0],
            name=row[1],
            symbol=row[2],
            asset_type=row[3],
            source=row[4],
            currency=row[5],
            current_price=row[6] or 0.0,
            last_updated=row[7] or '',
            note=row[8] or '',
        )

    def get_by_symbol(self, symbol: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            'SELECT id, name, symbol, asset_type, source, currency, current_price, last_updated, note FROM products WHERE UPPER(symbol) = UPPER(?)',
            (symbol,),
        )
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        return Product(
            id=row[0],
            name=row[1],
            symbol=row[2],
            asset_type=row[3],
            source=row[4],
            currency=row[5],
            current_price=row[6] or 0.0,
            last_updated=row[7] or '',
            note=row[8] or '',
        )

    def update_price(self, product_id: int, price: float, updated_at: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            'UPDATE products SET current_price = ?, last_updated = ? WHERE id = ?',
            (price, updated_at, product_id),
        )
        conn.commit()
        conn.close()
