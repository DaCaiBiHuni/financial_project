from datetime import datetime

from app.application.services.settings_service import SettingsService
from app.infrastructure.providers.mock_provider import MockMarketProvider
from app.infrastructure.providers.yahoo_provider import YahooMarketProvider
from app.infrastructure.db.repositories.product_repository import ProductRepository
from app.infrastructure.db.repositories.price_history_repository import PriceHistoryRepository


class MarketService:
    def __init__(self):
        self.settings_service = SettingsService()
        self.provider_name = self.settings_service.get_market_provider()
        self.provider = self._build_provider()
        self.repo = ProductRepository()
        self.history_repo = PriceHistoryRepository()

    def _build_provider(self):
        if self.provider_name == 'yahoo':
            return YahooMarketProvider()
        return MockMarketProvider()

    def reload_provider(self):
        self.provider_name = self.settings_service.get_market_provider()
        self.provider = self._build_provider()

    def refresh_product_price(self, product_id: int):
        product = self.repo.get_product(product_id)
        if not product:
            return {'ok': False, 'message': 'Product not found'}

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            price = self.provider.get_current_price(product.symbol)
            provider_used = self.provider_name
            message = f'{product.symbol} price refreshed via {provider_used}'
        except Exception as exc:
            fallback = MockMarketProvider()
            price = fallback.get_current_price(product.symbol)
            provider_used = 'mock-fallback'
            message = f'{product.symbol} failed on {self.provider_name}, fallback to mock: {exc}'

        self.repo.update_price(product_id, price, now)
        self.history_repo.add_price_point(product_id, price, now)
        return {
            'ok': True,
            'product_id': product_id,
            'symbol': product.symbol,
            'price': price,
            'provider': provider_used,
            'message': message,
        }

    def refresh_all_prices(self):
        self.reload_provider()
        products = self.repo.list_products()
        results = []
        for product in products:
            results.append(self.refresh_product_price(product.id))
        return results

    def get_price_history(self, product_id: int, limit: int = 20):
        return self.history_repo.get_price_history(product_id, limit)

    def get_provider_name(self):
        self.reload_provider()
        return self.provider_name
