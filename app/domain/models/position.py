from dataclasses import dataclass
from typing import Optional


@dataclass
class Position:
    id: Optional[int]
    product_id: int
    product_name: str
    quantity: float
    average_cost: float
    current_price: float = 0.0
    market_value: float = 0.0
    profit_loss: float = 0.0
    profit_loss_rate: float = 0.0
