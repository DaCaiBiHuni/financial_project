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
            return {'ok': False, 'message': 'Product not found', 'provider': self.provider_name}

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if self.provider_name == 'mock':
            price = self.provider.get_current_price(product.symbol)
            history = self.provider.get_yearly_monthly_history(product.symbol)
            self.repo.update_price(product_id, price, now)
            self.history_repo.replace_yearly_history(product_id, history)
            return {
                'ok': True,
                'product_id': product_id,
                'symbol': product.symbol,
                'price': price,
                'provider': 'mock',
                'message': f'{product.symbol} refreshed via mock provider',
            }

        try:
            price = self.provider.get_current_price(product.symbol)
            history = self.provider.get_yearly_monthly_history(product.symbol)
            self.repo.update_price(product_id, price, now)
            self.history_repo.replace_yearly_history(product_id, history)
            return {
                'ok': True,
                'product_id': product_id,
                'symbol': product.symbol,
                'price': price,
                'provider': self.provider_name,
                'message': f'{product.symbol} refreshed via {self.provider_name}',
            }
        except Exception as exc:
            return {
                'ok': False,
                'product_id': product_id,
                'symbol': product.symbol,
                'provider': self.provider_name,
                'message': f'{product.symbol} refresh failed on {self.provider_name}: {exc}',
            }

    def refresh_all_prices(self):
        self.reload_provider()
        products = self.repo.list_products()
        return [self.refresh_product_price(product.id) for product in products]

    def get_price_history(self, product_id: int, limit: int = 12):
        return self.history_repo.get_price_history(product_id, limit)

    def get_provider_name(self):
        self.reload_provider()
        return self.provider_name
