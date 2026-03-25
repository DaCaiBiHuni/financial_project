import random

from app.infrastructure.providers.base_provider import BaseMarketProvider


class MockMarketProvider(BaseMarketProvider):
    def get_current_price(self, symbol: str) -> float:
        seed = sum(ord(c) for c in symbol.upper())
        random.seed(seed)
        return round(random.uniform(10, 500), 2)
