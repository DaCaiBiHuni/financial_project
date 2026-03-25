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
        total_market_value = sum(p.market_value for p in positions)
        total_profit_loss = total_market_value - total_cost
        total_profit_loss_rate = (total_profit_loss / total_cost * 100) if total_cost else 0.0
        return {
            'position_count': len(positions),
            'total_cost': total_cost,
            'total_market_value': total_market_value,
            'total_profit_loss': total_profit_loss,
            'total_profit_loss_rate': total_profit_loss_rate,
        }
