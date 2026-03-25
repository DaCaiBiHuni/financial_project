from dataclasses import dataclass
from typing import Optional


@dataclass
class Position:
    id: Optional[int]
    product_id: int
    product_name: str
    quantity: float
    average_cost: float
