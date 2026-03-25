from app.domain.models.product import Product
from app.infrastructure.db.database import get_connection


class ProductRepository:
    def add_product(self, product: Product) -> int:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO products (name, symbol, asset_type, source, currency, note) VALUES (?, ?, ?, ?, ?, ?)',
            (product.name, product.symbol, product.asset_type, product.source, product.currency, product.note),
        )
        conn.commit()
        product_id = cur.lastrowid
        conn.close()
        return product_id

    def list_products(self) -> list[Product]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, name, symbol, asset_type, source, currency, note FROM products ORDER BY id DESC')
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
                note=row[6] or '',
            )
            for row in rows
        ]
