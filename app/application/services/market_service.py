from datetime import datetime

from app.infrastructure.providers.mock_provider import MockMarketProvider
from app.infrastructure.db.repositories.product_repository import ProductRepository


class MarketService:
    def __init__(self):
        self.provider = MockMarketProvider()
        self.repo = ProductRepository()

    def refresh_product_price(self, product_id: int):
        product = self.repo.get_product(product_id)
        if not product:
            return None
        price = self.provider.get_current_price(product.symbol)
        self.repo.update_price(product_id, price, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return price

    def refresh_all_prices(self):
        products = self.repo.list_products()
        for product in products:
            self.refresh_product_price(product.id)
