from abc import ABC, abstractmethod


class BaseMarketProvider(ABC):
    @abstractmethod
    def get_current_price(self, symbol: str) -> float:
        raise NotImplementedError

    @abstractmethod
    def get_yearly_monthly_history(self, symbol: str):
        raise NotImplementedError
