from abc import ABC, abstractmethod


class BaseMarketProvider(ABC):
    @abstractmethod
    def get_current_price(self, symbol: str) -> float:
        raise NotImplementedError
