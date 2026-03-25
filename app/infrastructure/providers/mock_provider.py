import random
from datetime import datetime

from app.infrastructure.providers.base_provider import BaseMarketProvider


class MockMarketProvider(BaseMarketProvider):
    def get_current_price(self, symbol: str) -> float:
        seed = sum(ord(c) for c in symbol.upper())
        random.seed(seed)
        return round(random.uniform(10, 500), 2)

    def get_yearly_monthly_history(self, symbol: str):
        seed = sum(ord(c) for c in symbol.upper())
        random.seed(seed)
        base = random.uniform(50, 300)
        data = []
        now = datetime.now()
        for i in range(11, -1, -1):
            month = now.month - i
            year = now.year
            while month <= 0:
                month += 12
                year -= 1
            while month > 12:
                month -= 12
                year += 1
            price = round(base + random.uniform(-20, 20) + (11 - i) * random.uniform(-3, 5), 2)
            data.append({'price': price, 'recorded_at': f'{year}-{month:02d}-01 00:00:00'})
        return data
