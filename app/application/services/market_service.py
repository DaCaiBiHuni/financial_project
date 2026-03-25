from datetime import datetime

from app.application.services.settings_service import SettingsService
from app.infrastructure.providers.mock_provider import MockMarketProvider
from app.infrastructure.providers.yahoo_provider import YahooMarketProvider
from app.infrastructure.db.repositories.product_repository import ProductRepository
from app.infrastructure.db.repositories.price_history_repository import PriceHistoryRepository


class MarketService:
    def __init__(self):
        self.settings_service = SettingsService()
        self.provider = self._build_provider()
        self.repo = ProductRepository()
        self.history_repo = PriceHistoryRepository()

    def _build_provider(self):
        provider_name = self.settings_service.get_market_provider()
        if provider_name == 'yahoo':
            return YahooMarketProvider()
        return MockMarketProvider()

    def reload_provider(self):
        self.provider = self._build_provider()

    def refresh_product_price(self, product_id: int):
        product = self.repo.get_product(product_id)
        if not product:
            return None
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            price = self.provider.get_current_price(product.symbol)
        except Exception:
            fallback = MockMarketProvider()
            price = fallback.get_current_price(product.symbol)
        self.repo.update_price(product_id, price, now)
        self.history_repo.add_price_point(product_id, price, now)
        return price

    def refresh_all_prices(self):
        self.reload_provider()
        products = self.repo.list_products()
        for product in products:
            self.refresh_product_price(product.id)

    def get_price_history(self, product_id: int, limit: int = 20):
        return self.history_repo.get_price_history(product_id, limit)
