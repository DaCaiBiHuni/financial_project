from app.infrastructure.db.repositories.product_repository import ProductRepository
from app.infrastructure.db.repositories.position_repository import PositionRepository


class DashboardService:
    def __init__(self):
        self.product_repo = ProductRepository()
        self.position_repo = PositionRepository()

    def get_dashboard_summary(self):
        products = self.product_repo.list_products()
        positions = self.position_repo.list_positions()
        total_cost = sum(p.quantity * p.average_cost for p in positions)
        return {
            'product_count': len(products),
            'position_count': len(positions),
            'total_cost': total_cost,
        }
