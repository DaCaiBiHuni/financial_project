import json
import urllib.request

from app.infrastructure.providers.base_provider import BaseMarketProvider


class YahooMarketProvider(BaseMarketProvider):
    def get_current_price(self, symbol: str) -> float:
        url = f'https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}'
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        result = data.get('quoteResponse', {}).get('result', [])
        if not result:
            raise ValueError(f'No market data found for symbol: {symbol}')
        price = result[0].get('regularMarketPrice')
        if price is None:
            raise ValueError(f'No regularMarketPrice for symbol: {symbol}')
        return float(price)
