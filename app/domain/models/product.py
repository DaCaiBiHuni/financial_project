from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    id: Optional[int]
    name: str
    symbol: str
    asset_type: str
    source: str
    currency: str
    current_price: float = 0.0
    last_updated: str = ''
    note: str = ''
