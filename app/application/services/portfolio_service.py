from app.infrastructure.db.repositories.position_repository import PositionRepository


class PortfolioService:
    def __init__(self):
        self.repo = PositionRepository()

    def create_position(self, product_id: int, quantity: float, average_cost: float) -> int:
        return self.repo.add_position(product_id, quantity, average_cost)

    def get_all_positions(self):
        return self.repo.list_positions()

    def get_portfolio_summary(self):
        positions = self.repo.list_positions()
        total_cost = sum(p.quantity * p.average_cost for p in positions)
        return {
            'position_count': len(positions),
            'total_cost': total_cost,
        }
