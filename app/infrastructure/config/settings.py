import os

MARKET_PROVIDER = 'mock'  # mock | yahoo | alphavantage
ALPHAVANTAGE_API_KEY = os.getenv('ALPHAVANTAGE_API_KEY', '')
