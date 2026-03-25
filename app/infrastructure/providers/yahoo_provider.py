import json
import urllib.request
from datetime import datetime

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

    def get_yearly_monthly_history(self, symbol: str):
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=1y&interval=1mo'
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        result = data.get('chart', {}).get('result', [])
        if not result:
            raise ValueError(f'No chart data found for symbol: {symbol}')
        result = result[0]
        timestamps = result.get('timestamp', [])
        closes = result.get('indicators', {}).get('quote', [{}])[0].get('close', [])
        history = []
        for ts, close in zip(timestamps, closes):
            if close is None:
                continue
            recorded_at = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            history.append({'price': float(close), 'recorded_at': recorded_at})
        return history
