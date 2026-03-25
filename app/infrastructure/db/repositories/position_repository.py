from app.domain.models.position import Position
from app.infrastructure.db.database import get_connection


class PositionRepository:
    def add_position(self, product_id: int, quantity: float, average_cost: float) -> int:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO portfolio_positions (product_id, quantity, average_cost) VALUES (?, ?, ?)',
            (product_id, quantity, average_cost),
        )
        conn.commit()
        position_id = cur.lastrowid
        conn.close()
        return position_id

    def list_positions(self) -> list[Position]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            '''
            SELECT p.id, p.product_id, pr.name, p.quantity, p.average_cost
            FROM portfolio_positions p
            JOIN products pr ON p.product_id = pr.id
            ORDER BY p.id DESC
            '''
        )
        rows = cur.fetchall()
        conn.close()
        return [
            Position(
                id=row[0],
                product_id=row[1],
                product_name=row[2],
                quantity=row[3],
                average_cost=row[4],
            )
            for row in rows
        ]
