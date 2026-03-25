import json
import urllib.parse
import urllib.request
from datetime import datetime

from app.infrastructure.config.settings import ALPHAVANTAGE_API_KEY
from app.infrastructure.providers.base_provider import BaseMarketProvider


class AlphaVantageProvider(BaseMarketProvider):
    def _ensure_key(self):
        if not ALPHAVANTAGE_API_KEY:
            raise ValueError('ALPHAVANTAGE_API_KEY is not configured')

    def get_current_price(self, symbol: str) -> float:
        self._ensure_key()
        params = urllib.parse.urlencode({
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': ALPHAVANTAGE_API_KEY,
        })
        url = f'https://www.alphavantage.co/query?{params}'
        with urllib.request.urlopen(url, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
        quote = data.get('Global Quote', {})
        price = quote.get('05. price')
        if not price:
            raise ValueError(f'No price returned for symbol: {symbol}')
        return float(price)

    def get_yearly_monthly_history(self, symbol: str):
        self._ensure_key()
        params = urllib.parse.urlencode({
            'function': 'TIME_SERIES_MONTHLY',
            'symbol': symbol,
            'apikey': ALPHAVANTAGE_API_KEY,
        })
        url = f'https://www.alphavantage.co/query?{params}'
        with urllib.request.urlopen(url, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
        series = data.get('Monthly Time Series', {})
        if not series:
            note = data.get('Note') or data.get('Information') or data
            raise ValueError(f'No monthly history returned for symbol: {symbol}; details: {note}')
        rows = []
        for date_str in sorted(series.keys())[-12:]:
            close_price = series[date_str].get('4. close')
            if close_price is None:
                continue
            rows.append({'price': float(close_price), 'recorded_at': f'{date_str} 00:00:00'})
        return rows
